import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

# 1. Ensure the model path points to the assets folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

model_path = os.path.join(PROJECT_ROOT, 'assets', 'face_landmarker.task')

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Please download 'face_landmarker.task' and place it in: {model_path}")

# 2. MediaPipe Tasks API Configuration
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

# 3. Detector Initialization
detector = vision.FaceLandmarker.create_from_options(options)

def is_head_tilted_down(image_bgr):
    """
    Receives 1 image frame, checks the face using Tasks API, and returns True if tilting down.
    """
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    
    detection_result = detector.detect(mp_image)

    if not detection_result.face_landmarks:
        return False

    face_landmarks = detection_result.face_landmarks[0]

    # Get Y coordinates
    y_nose = face_landmarks[1].y
    y_forehead = face_landmarks[10].y
    y_chin = face_landmarks[152].y

    # Calculate distances
    dist_forehead_to_nose = y_nose - y_forehead
    dist_nose_to_chin = y_chin - y_nose

    # Trigger logic
    if dist_nose_to_chin < (dist_forehead_to_nose * 0.7):
        return True
    else:
        return False