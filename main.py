import time
import threading
import cv2
from src.tray_manager import setup_tray, app_state
from src.audio_engine import play_warning, stop_warning
from src.vision_engine import is_head_tilted_down

def background_camera_loop():
    print("Starting background monitoring...")
    cap = cv2.VideoCapture(0)
    
    consecutive_tilt_count = 0
    TILT_THRESHOLD = 5 # Number of consecutive tilted frames before the alarm triggers

    while app_state["is_running"]:
        if app_state["is_paused"]:
            time.sleep(1)
            continue

        success, frame = cap.read()
        if success:
            # Analyze the frame
            is_tilted = is_head_tilted_down(frame)

            # Alarm Logic
            if is_tilted:
                consecutive_tilt_count += 1
                print(f"Tilt detected: {consecutive_tilt_count}/{TILT_THRESHOLD}")
                if consecutive_tilt_count >= TILT_THRESHOLD:
                    play_warning()
                    consecutive_tilt_count = 0 
                
            else:
                consecutive_tilt_count = 0 
                stop_warning()  # Stop the alarm if not tilting

            # --- CAMERA DISPLAY LOGIC ---
            if app_state["show_camera"]:
                # Status indicator text
                color = (0, 0, 255) if is_tilted else (0, 255, 0)
                text = "TILTED!" if is_tilted else "UPRIGHT"
                cv2.putText(frame, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                
                cv2.imshow("Doomscroll Monitor (1 FPS)", frame)
                
                cv2.waitKey(1000) 
            else:
                time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()
    print("Camera turned off.")

if __name__ == "__main__":
    camera_thread = threading.Thread(target=background_camera_loop, daemon=True)
    camera_thread.start()

    tray_icon = setup_tray()
    tray_icon.run()