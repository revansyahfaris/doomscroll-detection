import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

# 1. Pastikan path modelnya mengarah ke folder assets
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

model_path = os.path.join(PROJECT_ROOT, 'assets', 'face_landmarker.task')

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Tolong download file 'face_landmarker.task' dan letakkan di: {model_path}")

# 2. Konfigurasi MediaPipe Tasks API
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

# 3. Inisialisasi Detektor
detector = vision.FaceLandmarker.create_from_options(options)

def is_head_tilted_down(image_bgr):
    """
    Menerima 1 frame gambar, mengecek wajah dengan Tasks API, dan me-return True jika menunduk.
    """
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    
    detection_result = detector.detect(mp_image)

    if not detection_result.face_landmarks:
        return False

    face_landmarks = detection_result.face_landmarks[0]

    # Ambil kordinat Y
    y_nose = face_landmarks[1].y
    y_forehead = face_landmarks[10].y
    y_chin = face_landmarks[152].y

    # Hitung jarak
    jarak_dahi_ke_hidung = y_nose - y_forehead
    jarak_hidung_ke_dagu = y_chin - y_nose

    # Logika pemicu
    if jarak_hidung_ke_dagu < (jarak_dahi_ke_hidung * 0.7):
        return True
    else:
        return False