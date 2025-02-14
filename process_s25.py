import cv2
import torch
import numpy as np
from ultralytics import YOLO
from rembg import remove

# Load YOLOv8 model (pretrained)
model = YOLO("yolov8n.pt")  # Use "yolov8x.pt" for better accuracy

# Load the video
video_path = "downloaded_video.mp4"
cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

# Define labels for Samsung S25 (custom-trained model needed for best accuracy)
s25_labels = ["Samsung S25", "Samsung phone", "S25"]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects
    results = model(frame)

    # Process detections
    mask = np.zeros_like(frame, dtype=np.uint8)

    for result in results.xyxy[0]:  # Bounding boxes
        x1, y1, x2, y2, conf, cls = result.tolist()
        label = model.names[int(cls)]

        if label in s25_labels:
            # Extract the detected S25 region
            s25_region = frame[int(y1):int(y2), int(x1):int(x2)]

            # Remove background
            s25_no_bg = remove(s25_region)

            # Replace the S25 region in the original frame
            frame[int(y1):int(y2), int(x1):int(x2)] = s25_no_bg

        else:
            # Turn objects touching S25 to black (shiny black effect)
            obj_mask = np.zeros_like(frame)
            cv2.rectangle(obj_mask, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 0), thickness=cv2.FILLED)
            frame = cv2.addWeighted(frame, 1, obj_mask, 0.5, 0)

    out.write(frame)

cap.release()
out.release()

print("Processing completed. Saved as output.mp4")
