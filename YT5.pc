import cv2
import numpy as np
import mediapipe as mp
import os
import sys
import subprocess
import time

def convert_to_mp4(input_path, output_path):
    print(f"[INFO] Converting video to MP4 for compatibility: {input_path}")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-c:v", "libx264", "-c:a", "aac", output_path
        ], check=True)
        print(f"[✓] Converted to: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"[❌] FFmpeg conversion failed: {e}")
        sys.exit(1)

# --- Detect and Prepare Video File ---
video_dir = "Vid"
input_path = None
for file in os.listdir(video_dir):
    if file.startswith("video.") and file.endswith((".webm", ".mp4", ".mkv")):
        input_path = os.path.join(video_dir, file)
        break

if not input_path:
    print("❌ No video file found in Vid/")
    sys.exit(1)

# Convert WebM/VP9 to MP4 if needed
if input_path.endswith(".webm") or input_path.endswith(".mkv"):
    temp_path = os.path.join(video_dir, "converted.mp4")
    input_path = convert_to_mp4(input_path, temp_path)

output_path = os.path.join(video_dir, "blur.webm")

print(f"[INFO] Using input: {input_path}")
print(f"[INFO] Output will be saved to: {output_path}")

# --- Load MediaPipe Models ---
print("[INFO] Loading MediaPipe models...")
mp_face = mp.solutions.face_detection
mp_selfie = mp.solutions.selfie_segmentation

face_det = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.6)
selfie_seg = mp_selfie.SelfieSegmentation(model_selection=1)
print("[✓] MediaPipe models loaded.")

# --- Open Video ---
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    sys.exit(1)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"[INFO] Resolution: {width}x{height}, FPS: {fps}, Total Frames: {frame_count}")

# --- Setup Video Writer ---
fourcc = cv2.VideoWriter_fourcc(*'VP90')  # Use VP90 only if output format is .webm
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# --- Process Video Frame-by-Frame ---
print("[INFO] Starting video processing...")
start_time = time.time()
processed_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] End of video stream.")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    seg_result = selfie_seg.process(rgb)
    seg_mask = (seg_result.segmentation_mask > 0.3).astype(np.uint8) * 255

    face_result = face_det.process(rgb)
    head_mask = np.zeros((height, width), dtype=np.uint8)

    if face_result.detections:
        for detection in face_result.detections:
            box = detection.location_data.relative_bounding_box
            x = int(box.xmin * width)
            y = int(box.ymin * height)
            w = int(box.width * width)
            h = int(box.height * height)

            x = max(x - 20, 0)
            y = max(y - 40, 0)
            w = min(w + 40, width - x)
            h = min(h + 80, height - y)

            head_mask[y:y+h, x:x+w] = 255

    head_only_mask = cv2.bitwise_and(seg_mask, head_mask)

    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_inv = cv2.bitwise_not(head_only_mask)
    head_blur = cv2.bitwise_and(blurred, blurred, mask=head_only_mask)
    body = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final = cv2.add(head_blur, body)

    out.write(final)

    processed_frames += 1
    if processed_frames % 100 == 0:
        print(f"[INFO] Processed {processed_frames}/{frame_count} frames...")

cap.release()
out.release()

duration = time.time() - start_time
print(f"[✓] Done. Processed {processed_frames} frames in {duration:.2f} seconds.")
print(f"[✓] Head-blurred video saved as {output_path}")
