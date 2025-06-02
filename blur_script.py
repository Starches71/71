
import cv2
import numpy as np
import mediapipe as mp
import os

# Input and output paths
input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_v4.mp4"

# Initialize MediaPipe
mp_selfie_segmentation = mp.solutions.selfie_segmentation
mp_hands = mp.solutions.hands

selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

# Load video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    exit(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Use higher-quality encoding
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

def exclude_full_hand_from_mask(mask, hand_landmarks, width, height):
    points = [(int(lm.x * width), int(lm.y * height)) for lm in hand_landmarks.landmark]
    if len(points) >= 3:
        hull = cv2.convexHull(np.array(points))
        cv2.fillConvexPoly(mask, hull, 0)

        # Expand the hand region slightly to ensure complete exclusion
        hand_mask = np.zeros_like(mask)
        cv2.fillConvexPoly(hand_mask, hull, 255)
        hand_mask = cv2.dilate(hand_mask, np.ones((30, 30), np.uint8), iterations=1)
        mask[hand_mask == 255] = 0

# Process frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Person segmentation
    seg_result = selfie_segmentation.process(rgb)
    seg_mask = (seg_result.segmentation_mask > 0.1).astype(np.uint8) * 255

    # Hand detection
    hand_result = hands.process(rgb)
    if hand_result.multi_hand_landmarks:
        for hand_landmarks in hand_result.multi_hand_landmarks:
            exclude_full_hand_from_mask(seg_mask, hand_landmarks, width, height)

    # Apply blur to person area (excluding hands)
    blurred = cv2.GaussianBlur(frame, (31, 31), 15)
    mask_inv = cv2.bitwise_not(seg_mask)
    blurred_part = cv2.bitwise_and(blurred, blurred, mask=seg_mask)
    original_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_frame = cv2.add(blurred_part, original_part)

    out.write(final_frame)

# Cleanup
cap.release()
out.release()

# Confirmation
if os.path.exists(output_path):
    print(f"✅ Done! Output saved as {output_path}")
else:
    print(f"❌ Failed to write {output_path}")
