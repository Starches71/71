
import cv2
import numpy as np
import mediapipe as mp
import os

# Input and output paths
input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_v4.avi"

# Initialize MediaPipe
mp_selfie_seg = mp.solutions.selfie_segmentation
mp_face = mp.solutions.face_detection

selfie_seg = mp_selfie_seg.SelfieSegmentation(model_selection=1)
face_det = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.6)

# Open video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    exit(1)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out    = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Step 1: Get selfie segmentation mask
    seg_result = selfie_seg.process(rgb)
    seg_mask = (seg_result.segmentation_mask > 0.3).astype(np.uint8) * 255

    # Step 2: Detect face bounding box
    face_result = face_det.process(rgb)
    face_mask = np.zeros((height, width), dtype=np.uint8)

    if face_result.detections:
        for detection in face_result.detections:
            box = detection.location_data.relative_bounding_box
            x = int(box.xmin * width)
            y = int(box.ymin * height)
            w = int(box.width * width)
            h = int(box.height * height)

            # Expand slightly for forehead and hair
            x = max(x - 10, 0)
            y = max(y - 20, 0)
            w = min(w + 20, width - x)
            h = min(h + 40, height - y)

            face_mask[y:y+h, x:x+w] = 255

    # Step 3: Combine face and segmentation mask
    combined_mask = cv2.bitwise_and(seg_mask, face_mask)

    # Step 4: Blur only the head region
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_inv = cv2.bitwise_not(combined_mask)

    head_blurred = cv2.bitwise_and(blurred, blurred, mask=combined_mask)
    rest = cv2.bitwise_and(frame, frame, mask=mask_inv)

    result = cv2.add(head_blurred, rest)
    out.write(result)

cap.release()
out.release()

if os.path.exists(output_path):
    print(f"✅ Done! Head blurred video saved as {output_path}")
else:
    print("❌ Failed to save output video.")
