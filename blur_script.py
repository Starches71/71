
import cv2
import numpy as np
import mediapipe as mp

input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_v4.mp4"

mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(static_image_mode=False)

cap = cv2.VideoCapture(input_path)
width, height = int(cap.get(3)), int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Key face landmark indices to include entire head/hair boundary
# Includes jawline + forehead + side of face for better hair coverage
FACE_HULL_IDS = [
    10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377,
    152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109, 10
]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(rgb)

    mask = np.zeros((height, width), dtype=np.uint8)
    body_points = []

    # Pose: torso & legs
    if results.pose_landmarks:
        for i in range(11, 24):
            lm = results.pose_landmarks.landmark[i]
            body_points.append((int(lm.x * width), int(lm.y * height)))

    # Face: dense landmarks to capture full head including hair
    if results.face_landmarks:
        face_landmarks = results.face_landmarks.landmark
        face_points = []
        for idx in FACE_HULL_IDS:
            lm = face_landmarks[idx]
            face_points.append((int(lm.x * width), int(lm.y * height)))
        body_points.extend(face_points)

    # Final hull over body + head
    if body_points:
        hull = cv2.convexHull(np.array(body_points))
        cv2.fillConvexPoly(mask, hull, 255)

    # Exclude hands
    for hand_landmarks in [results.left_hand_landmarks, results.right_hand_landmarks]:
        if hand_landmarks:
            hand_points = [(int(p.x * width), int(p.y * height)) for p in hand_landmarks.landmark]
            if hand_points:
                hand_hull = cv2.convexHull(np.array(hand_points))
                cv2.fillConvexPoly(mask, hand_hull, 0)

    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_3c = cv2.merge([mask] * 3)
    final_frame = np.where(mask_3c == 255, blurred, frame)

    out.write(final_frame)

cap.release()
out.release()
print("✅ Done! Entire head and body blurred, hands excluded.")
