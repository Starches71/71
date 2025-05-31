
import cv2
import mediapipe as mp

INPUT_PATH = "Screen_Recording_20250508-143207_Chrome.mp4"
OUTPUT_PATH = "output_blurred.mp4"

# Initialize MediaPipe face detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Open input video
cap = cv2.VideoCapture(INPUT_PATH)
if not cap.isOpened():
    raise IOError("Error opening video file.")

# Get video properties
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# Process each frame
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)

        if results.detections:
            for det in results.detections:
                bbox = det.location_data.relative_bounding_box
                x, y, w, h = int(bbox.xmin * width), int(bbox.ymin * height), \
                             int(bbox.width * width), int(bbox.height * height)

                # Apply blur to face area
                face_roi = frame[y:y+h, x:x+w]
                if face_roi.size > 0:
                    blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
                    frame[y:y+h, x:x+w] = blurred_face

        out.write(frame)

cap.release()
out.release()
print("✅ Finished blurring faces.")
