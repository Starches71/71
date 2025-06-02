
import cv2
import numpy as np
import mediapipe as mp
import os

# Input and output paths
input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_v4.avi"  # Using MJPG to avoid codec error

# Initialize MediaPipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
mp_hands = mp.solutions.hands

selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6)

# Load video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    exit(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

def exclude_expanded_hand_area(mask, hand_landmarks, width, height):
    points = [(int(lm.x * width), int(lm.y * height)) for lm in hand_landmarks.landmark]
    if len(points) >= 3:
        hull = cv2.convexHull(np.array(points))
        # Create black mask with only hand region white
        hand_mask = np.zeros((height, width), dtype=np.uint8)
        cv2.fillConvexPoly(hand_mask, hull, 255)
        # Dilate hand mask to enlarge area
        kernel = np.ones((70, 70), np.uint8)  # increase size for more safety
        dilated_hand_mask = cv2.dilate(hand_mask, kernel, iterations=1)
        # Remove hand area from blur mask
        mask[dilated_hand_mask == 255] = 0

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Step 1: Person segmentation
    seg_result = selfie_segmentation.process(rgb)
    seg_mask = (seg_result.segmentation_mask > 0.1).astype(np.uint8) * 255

    # Step 2: Detect and preserve hands
    hand_result = hands.process(rgb)
    if hand_result.multi_hand_landmarks:
        for hand_landmarks in hand_result.multi_hand_landmarks:
            exclude_expanded_hand_area(seg_mask, hand_landmarks, width, height)

    # Step 3: Apply selective blur
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_inv = cv2.bitwise_not(seg_mask)
    blurred_part = cv2.bitwise_and(blurred, blurred, mask=seg_mask)
    original_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_frame = cv2.add(blurred_part, original_part)

    out.write(final_frame)

cap.release()
out.release()

if os.path.exists(output_path):
    print(f"✅ Done! Output saved as {output_path}")
else:
    print(f"❌ Failed to write {output_path}")
