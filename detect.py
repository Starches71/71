
from ikomia.dataprocess.workflow import Workflow
import os

video_path = "iPhone_16_Pro_Max_VS_S24_Ultra_-_Ultimate_selfie_test!(360p).mp4"
output_dir = "outputs"

# Create workflow
wf = Workflow()

# Add YOLOv7 detection task
yolo_task = wf.add_task("infer_yolo_v7")

# Optional: configure task
yolo_task.set_parameters({"conf_thres": 0.3})  # confidence threshold

# Run detection on video
wf.run_on(video_path)

# Export video with detections
os.makedirs(output_dir, exist_ok=True)
wf.save_video(os.path.join(output_dir, "detected.mp4"))
