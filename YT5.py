
import cv2
import numpy as np
import mediapipe as mp
import os
import sys

# --- Auto-detect input video file ---
video_dir = "Vid"
input_path = None
for file in os.listdir(video_dir):
    if file.startswith("video.") and file.endswith((".webm", ".mp4", ".mkv")):
        input_path = os.path.join(video_dir, file)
        break

if not input_path:
    print("❌ No video file found in Vid/")
    sys.exit(1)

# Set output path (always .webm for consistency)
output_path = os.path.join(video_dir, "blur.webm")

# Ensure Vid folder exists
os.makedirs(video_dir, exist_ok=True)

# Initialize MediaPipe models
mp_face = mp.solutions.face_detection
mp_selfie = mp.solutions.selfie_segmentation

face_det = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.6)
selfie_seg = mp_selfie.SelfieSegmentation(model_selection=1)

# Open input video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    sys.exit(1)

# Get video properties
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

# Define video writer codec
fourcc = cv2.VideoWriter_fourcc(*'VP90')  # VP90 for .webm
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Process each frame
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Person segmentation
    seg_result = selfie_seg.process(rgb)
    seg_mask = (seg_result.segmentation_mask > 0.3).astype(np.uint8) * 255

    # Face detection
    face_result = face_det.process(rgb)
    head_mask = np.zeros((height, width), dtype=np.uint8)

    if face_result.detections:
        for detection in face_result.detections:
            box = detection.location_data.relative_bounding_box
            x = int(box.xmin * width)
            y = int(box.ymin * height)
            w = int(box.width * width)
            h = int(box.height * height)

            # Expand bounding box
            x = max(x - 20, 0)
            y = max(y - 40, 0)
            w = min(w + 40, width - x)
            h = min(h + 80, height - y)

            head_mask[y:y+h, x:x+w] = 255

    # Combine segmentation and face mask
    head_only_mask = cv2.bitwise_and(seg_mask, head_mask)

    # Apply blur to head region only
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_inv = cv2.bitwise_not(head_only_mask)
    head_blur = cv2.bitwise_and(blurred, blurred, mask=head_only_mask)
    body = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final = cv2.add(head_blur, body)

    out.write(final)

cap.release()
out.release()

# Done
if os.path.exists(output_path):
    print(f"✅ Done! Head-blurred video saved as {output_path}")
else:
    print("❌ Failed to save output video.")
