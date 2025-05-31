
import cv2
import mediapipe as mp

INPUT_PATH = "Screen_Recording_20250508-143207_Chrome.mp4"
OUTPUT_PATH = "output_blurred.mp4"

mp_face_detection = mp.solutions.face_detection
cap = cv2.VideoCapture(INPUT_PATH)

if not cap.isOpened():
    raise IOError("❌ Could not open video.")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)

        if results.detections:
            for det in results.detections:
                bbox = det.location_data.relative_bounding_box
                x = int(bbox.xmin * width)
                y = int(bbox.ymin * height)
                w = int(bbox.width * width)
                h = int(bbox.height * height)

                # Expand the bounding box to include more of the head
                pad_x = int(w * 0.3)
                pad_y_top = int(h * 0.6)
                pad_y_bottom = int(h * 0.3)

                x1 = max(0, x - pad_x)
                y1 = max(0, y - pad_y_top)
                x2 = min(width, x + w + pad_x)
                y2 = min(height, y + h + pad_y_bottom)

                face_roi = frame[y1:y2, x1:x2]
                if face_roi.size > 0:
                    blurred = cv2.GaussianBlur(face_roi, (99, 99), 30)
                    frame[y1:y2, x1:x2] = blurred

        out.write(frame)

cap.release()
out.release()
print("✅ Finished blurring full head.")
