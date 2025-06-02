
import cv2
import numpy as np
import mediapipe as mp
import os

# Paths
input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_v4.avi"

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6)

# Open video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    exit(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Video writer (MJPG is broadly compatible)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

def get_hand_mask(rgb_frame, width, height):
    mask = np.zeros((height, width), dtype=np.uint8)
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            points = [(int(lm.x * width), int(lm.y * height)) for lm in hand_landmarks.landmark]
            if len(points) >= 3:
                hull = cv2.convexHull(np.array(points))
                temp_mask = np.zeros_like(mask)
                cv2.fillConvexPoly(temp_mask, hull, 255)
                kernel = np.ones((70, 70), np.uint8)
                temp_mask = cv2.dilate(temp_mask, kernel, iterations=1)
                mask = cv2.bitwise_or(mask, temp_mask)
    return mask

# Process frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_mask = get_hand_mask(rgb, width, height)

    # Blur full frame
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)

    # Keep hand areas unblurred
    hand_area = cv2.bitwise_and(frame, frame, mask=hand_mask)
    background_area = cv2.bitwise_and(blurred, blurred, mask=cv2.bitwise_not(hand_mask))
    final = cv2.add(hand_area, background_area)

    out.write(final)

# Cleanup
cap.release()
out.release()

if os.path.exists(output_path):
    print(f"✅ Done! Output saved as {output_path}")
else:
    print(f"❌ Failed to write {output_path}")
