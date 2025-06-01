
import cv2
import numpy as np
import mediapipe as mp
import os

# Input and output paths
input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_v4.mp4"

# Initialize MediaPipe solutions
mp_selfie_segmentation = mp.solutions.selfie_segmentation
mp_hands = mp.solutions.hands

selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

# Load video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    exit(1)

width, height = int(cap.get(3)), int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

def draw_palm(mask, hand_landmarks, width, height):
    # Use key palm landmarks (excluding fingers)
    palm_indices = [0, 1, 2, 5, 9, 13, 17]
    points = [(int(hand_landmarks.landmark[i].x * width),
               int(hand_landmarks.landmark[i].y * height)) for i in palm_indices]
    if len(points) >= 3:
        hull = cv2.convexHull(np.array(points))
        cv2.fillConvexPoly(mask, hull, 0)  # Remove palm from blur mask

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Step 1: Segment the person
    seg_results = selfie_segmentation.process(rgb)
    seg_mask = (seg_results.segmentation_mask > 0.1).astype(np.uint8) * 255

    # Step 2: Detect hands and erase palms from blur mask
    hand_results = hands.process(rgb)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            draw_palm(seg_mask, hand_landmarks, width, height)

    # Step 3: Apply blur to body (excluding palms)
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_inv = cv2.bitwise_not(seg_mask)
    blurred_only = cv2.bitwise_and(blurred, blurred, mask=seg_mask)
    original_only = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_frame = cv2.add(blurred_only, original_only)

    out.write(final_frame)

# Finalize
cap.release()
out.release()

# Confirm success
if os.path.exists(output_path):
    print(f"✅ Done! Output saved as {output_path}")
else:
    print(f"❌ Failed to write {output_path}")
