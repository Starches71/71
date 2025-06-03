
import cv2
import numpy as np
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

# Convert to .mp4 if not already
if input_path.endswith((".webm", ".mkv")):
    temp_path = os.path.join(video_dir, "converted.mp4")
    input_path = convert_to_mp4(input_path, temp_path)

output_path = os.path.join(video_dir, "blurred_output.mp4")

print(f"[INFO] Using input: {input_path}")
print(f"[INFO] Output will be saved to: {output_path}")

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
if face_cascade.empty():
    print("❌ Failed to load Haar cascade classifier.")
    sys.exit(1)

# Open video capture
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    sys.exit(1)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"[INFO] Resolution: {width}x{height}, FPS: {fps}, Total Frames: {frame_count}")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print("[INFO] Starting video processing...")
start_time = time.time()
processed_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] End of video stream.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Expand box to cover head better
        x1 = max(x - int(0.3 * w), 0)
        y1 = max(y - int(0.6 * h), 0)
        x2 = min(x + w + int(0.3 * w), width)
        y2 = min(y + h + int(0.6 * h), height)

        roi = frame[y1:y2, x1:x2]

        # Blur ROI
        blurred_roi = cv2.GaussianBlur(roi, (99, 99), 30)

        # Create elliptical mask
        mask = np.zeros((y2 - y1, x2 - x1), dtype=np.uint8)
        center = ((x2 - x1) // 2, (y2 - y1) // 2)
        axes = (int((x2 - x1) / 2), int((y2 - y1) / 2))
        cv2.ellipse(mask, center, axes, angle=0, startAngle=0, endAngle=360, color=255, thickness=-1)

        mask_3ch = cv2.merge([mask, mask, mask])

        # Blend blurred ROI and original using mask
        roi = np.where(mask_3ch == 255, blurred_roi, roi)

        # Place blended ROI back into frame
        frame[y1:y2, x1:x2] = roi

    out.write(frame)
    processed_frames += 1

    if processed_frames % 100 == 0:
        print(f"[INFO] Processed {processed_frames}/{frame_count} frames...")

cap.release()
out.release()

duration = time.time() - start_time
print(f"[✓] Done. Processed {processed_frames} frames in {duration:.2f} seconds.")
print(f"[✓] Head-blurred video saved as {output_path}")
