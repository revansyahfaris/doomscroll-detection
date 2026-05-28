import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import cv2

app_state = {
    "is_running": True,
    "is_paused": False,
    "show_camera": False  
}

def create_dummy_icon():
    image = Image.new('RGB', (64, 64), color=(50, 50, 50))
    dc = ImageDraw.Draw(image)
    dc.rectangle([(16, 16), (48, 48)], fill=(0, 200, 0))
    return image

def toggle_pause(icon, item):
    app_state["is_paused"] = not app_state["is_paused"]

def toggle_camera(icon, item):
    app_state["show_camera"] = not app_state["show_camera"]
    if not app_state["show_camera"]:
        cv2.destroyAllWindows()

def quit_app(icon, item):
    app_state["is_running"] = False
    icon.stop()

def setup_tray():
    # Add Show/Hide Camera buttons to the tray menu
    menu = pystray.Menu(
        item(lambda text: "Resume Detection" if app_state["is_paused"] else "Pause Detection", toggle_pause),
        item(lambda text: "Hide Camera" if app_state["show_camera"] else "Show Camera", toggle_camera),
        item('Quit', quit_app)
    )
    
    icon = pystray.Icon("DoomscrollDetector", create_dummy_icon(), "Doomscroll Detector", menu)
    return icon