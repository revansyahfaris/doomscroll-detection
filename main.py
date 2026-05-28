import time
import threading
import cv2
from src.tray_manager import setup_tray, app_state
from src.audio_engine import play_warning, stop_warning
from src.vision_engine import is_head_tilted_down

def background_camera_loop():
    print("Memulai pemantauan background...")
    cap = cv2.VideoCapture(0)
    
    consecutive_tilt_count = 0
    BATAS_TILT = 5 # Jumlah frame menunduk berturut-turut sebelum alarm berbunyi

    while app_state["is_running"]:
        if app_state["is_paused"]:
            time.sleep(1)
            continue

        success, frame = cap.read()
        if success:
            # Analisa frame-nya
            is_tilted = is_head_tilted_down(frame)

            # Logika Alarm
            if is_tilted:
                consecutive_tilt_count += 1
                print(f"Menunduk terdeteksi: {consecutive_tilt_count}/{BATAS_TILT}")
                if consecutive_tilt_count >= BATAS_TILT:
                    play_warning()
                    consecutive_tilt_count = 0 
                
            else:
                consecutive_tilt_count = 0 
                stop_warning()  # Hentikan suara alarm jika tidak menunduk

            # --- LOGIKA TAMPILKAN LAYAR KAMERA ---
            if app_state["show_camera"]:
                # Teks indikator status
                warna = (0, 0, 255) if is_tilted else (0, 255, 0)
                teks = "NUNDUK!" if is_tilted else "TEGAK"
                cv2.putText(frame, teks, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, warna, 3)
                
                cv2.imshow("Monitor Doomscroll (1 FPS)", frame)
                
                cv2.waitKey(1000) 
            else:
                time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()
    print("Kamera dimatikan.")

if __name__ == "__main__":
    camera_thread = threading.Thread(target=background_camera_loop, daemon=True)
    camera_thread.start()

    tray_icon = setup_tray()
    tray_icon.run()