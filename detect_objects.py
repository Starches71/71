
import cv2
import torch

def detect_objects_in_video(video_path, interval_sec=1):
    # Load YOLOv8 model (use yolov8n for speed or yolov8m for accuracy)
    model = torch.hub.load('ultralytics/yolov8', 'yolov8n', pretrained=True)
    
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    
    results_summary = []
    frame_index = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process every interval_sec seconds
        if frame_index % int(frame_rate * interval_sec) == 0:
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(img_rgb)
            
            detected_objs = []
            for *box, conf, cls in results.xyxy[0].tolist():
                if conf > 0.5:
                    detected_objs.append(model.names[int(cls)])
            
            timestamp = frame_index / frame_rate
            results_summary.append({
                "time_sec": timestamp,
                "objects": list(set(detected_objs))
            })
        
        frame_index += 1
    
    cap.release()
    return results_summary

if __name__ == "__main__":
    video_file = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
    summary = detect_objects_in_video(video_file, interval_sec=1)
    for entry in summary:
        print(f"At {entry['time_sec']:.1f}s: Detected objects: {entry['objects']}")
