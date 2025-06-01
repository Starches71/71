
import cv2
import numpy as np
import mediapipe as mp

input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_selfie_segmentation.mp4"

mp_selfie_segmentation = mp.solutions.selfie_segmentation
mp_hands = mp.solutions.hands

# Initialize models
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

cap = cv2.VideoCapture(input_path)
width, height = int(cap.get(3)), int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

def draw_palm(mask, hand_landmarks, width, height, erase=True):
    # Palm landmark indices based on Mediapipe Hands
    palm_indices = [0, 1, 2, 5, 9, 13, 17]  # Wrist + base of fingers
    points = [(int(hand_landmarks.landmark[i].x * width),
               int(hand_landmarks.landmark[i].y * height)) for i in palm_indices]
    if len(points) >= 3:
        hull = cv2.convexHull(np.array(points))
        cv2.fillConvexPoly(mask, hull, 0 if erase else 255)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Step 1: Get full-body mask
    seg_results = selfie_segmentation.process(rgb)
    seg_mask = (seg_results.segmentation_mask > 0.1).astype(np.uint8) * 255

    # Step 2: Detect hands and remove palms from mask
    hand_results = hands.process(rgb)
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            draw_palm(seg_mask, hand_landmarks, width, height, erase=True)

    # Step 3: Blur and apply mask
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_3c = cv2.merge([seg_mask] * 3)
    final_frame = np.where(mask_3c == 255, blurred, frame)

    out.write(final_frame)

cap.release()
out.release()
print("✅ Done! Full body blurred, palms excluded.")
