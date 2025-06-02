
import cv2
import numpy as np
import mediapipe as mp
import os

# Input & output paths
input_path = os.path.join("Vid", "video.webm")
output_path = os.path.join("Vid", "blur.webm")  # You can change this to .mp4 if preferred

# Ensure Vid folder exists
os.makedirs("Vid", exist_ok=True)

# Initialize MediaPipe models
mp_face = mp.solutions.face_detection
mp_selfie = mp.solutions.selfie_segmentation

face_det = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.6)
selfie_seg = mp_selfie.SelfieSegmentation(model_selection=1)

# Open input video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    exit(1)

# Video properties
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

# Use appropriate codec for webm or mp4
if output_path.endswith(".webm"):
    fourcc = cv2.VideoWriter_fourcc(*'VP90')  # For webm
else:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For mp4

out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Step 1: Get person segmentation mask
    seg_result = selfie_seg.process(rgb)
    seg_mask = (seg_result.segmentation_mask > 0.3).astype(np.uint8) * 255

    # Step 2: Get face bounding box
    face_result = face_det.process(rgb)
    head_mask = np.zeros((height, width), dtype=np.uint8)

    if face_result.detections:
        for detection in face_result.detections:
            box = detection.location_data.relative_bounding_box
            x = int(box.xmin * width)
            y = int(box.ymin * height)
            w = int(box.width * width)
            h = int(box.height * height)

            # Expand bounding box for better head coverage
            x = max(x - 20, 0)
            y = max(y - 40, 0)
            w = min(w + 40, width - x)
            h = min(h + 80, height - y)

            head_mask[y:y+h, x:x+w] = 255

    # Step 3: Combine selfie mask and head mask
    head_only_mask = cv2.bitwise_and(seg_mask, head_mask)

    # Step 4: Apply blur to the head region
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_inv = cv2.bitwise_not(head_only_mask)
    head_blur = cv2.bitwise_and(blurred, blurred, mask=head_only_mask)
    body = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final = cv2.add(head_blur, body)

    out.write(final)

cap.release()
out.release()

# Confirm output
if os.path.exists(output_path):
    print(f"✅ Done! Head-blurred video saved as {output_path}")
else:
    print("❌ Failed to save output video.")
