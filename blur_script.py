import cv2
import numpy as np
import mediapipe as mp
import os

# Input and output paths
input_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_path = "blurred_v4.mp4"

# Initialize MediaPipe Selfie Segmentation
mp_selfie_seg = mp.solutions.selfie_segmentation
selfie_seg = mp_selfie_seg.SelfieSegmentation(model_selection=1)

# Open video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print(f"❌ Could not open video: {input_path}")
    exit(1)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

# MP4 writer using H.264 codec (must have ffmpeg installed)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    seg_result = selfie_seg.process(rgb)
    
    # Get segmentation mask and threshold it
    seg_mask = (seg_result.segmentation_mask > 0.3).astype(np.uint8) * 255

    # Estimate head region: take top portion of the mask (assume head is top 30% of person)
    person_coords = cv2.findNonZero(seg_mask)
    head_mask = np.zeros((height, width), dtype=np.uint8)

    if person_coords is not None:
        y_min = np.min(person_coords[:,0,1])
        y_max = np.max(person_coords[:,0,1])
        head_height = int((y_max - y_min) * 0.35)

        head_mask[y_min:y_min+head_height, :] = seg_mask[y_min:y_min+head_height, :]

    # Blur only head region
    blurred = cv2.GaussianBlur(frame, (61, 61), 51)
    mask_inv = cv2.bitwise_not(head_mask)

    head_blurred = cv2.bitwise_and(blurred, blurred, mask=head_mask)
    rest = cv2.bitwise_and(frame, frame, mask=mask_inv)

    result = cv2.add(head_blurred, rest)
    out.write(result)

cap.release()
out.release()

if os.path.exists(output_path):
    print(f"✅ Done! Head-blurred (shape-based) video saved as {output_path}")
else:
    print("❌ Failed to save output video.")
