
import cv2
import torch
import numpy as np
import os
from ultralytics import YOLO
from rembg import remove

# Load YOLOv8 model (pretrained)
model = YOLO("yolov8n.pt")

# Load the video
video_path = "downloaded_video.mp4"

if not os.path.exists(video_path):
    print(f"Error: Video file '{video_path}' not found!")
    exit(1)

cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))

if fps == 0:
    print("Error: Unable to retrieve FPS from video. Exiting...")
    exit(1)

out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

# Define labels for Samsung S25
s25_labels = ["Samsung S25", "Samsung phone", "S25"]

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    print(f"Processing frame {frame_count}")

    results = model(frame)

    for result in results.xyxy[0]:  # Bounding boxes
        x1, y1, x2, y2, conf, cls = result.tolist()
        label = model.names[int(cls)]

        if label in s25_labels:
            s25_region = frame[int(y1):int(y2), int(x1):int(x2)]
            s25_no_bg = remove(s25_region)
            frame[int(y1):int(y2), int(x1):int(x2)] = s25_no_bg

    out.write(frame)

cap.release()
out.release()

if os.path.exists("output.mp4"):
    print("Processing completed. Saved as output.mp4")
else:
    print("Error: Output file was not generated!")
