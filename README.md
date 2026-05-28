# Doomscroll Detection 📱👀

**Doomscroll Detection** is an AI-powered tool designed to maintain neck posture health and reduce "doomscrolling" habits. This application uses a webcam to monitor your head position in real-time and provides an audio warning if you tilt your head down for too long.

## ✨ Key Features
- **Automatic Tilt Detection**: Uses MediaPipe Face Landmarker to accurately detect head tilt.
- **Audio Warnings**: An alarm triggers if the system detects prolonged downward tilting (preventing "tech neck").
- **Background Mode (System Tray)**: The app runs in the background. You can control it via the system tray icon (bottom right corner of the screen).
- **Camera Monitor**: Option to show or hide the camera window to verify detection accuracy.
- **Pause/Resume**: Temporarily disable detection when needed.

## 📋 Prerequisites
Before running this application, ensure you have:
- Python 3.8 or newer.
- A webcam (internal or external).
- Required assets in the `assets/` folder.

## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/doomscroll-detection.git
   cd doomscroll-detection
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv .venv
   # Activate venv (Windows)
   .venv\Scripts\activate
   # Activate venv (Linux/Mac)
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Asset Preparation

This application requires two essential files in the `assets/` folder:

1.  **MediaPipe Model**: Download the `face_landmarker.task` file from [MediaPipe Google](https://developers.google.com/mediapipe/solutions/vision/face_landmarker#models) and place it inside the `assets/` folder.
2.  **Alarm Audio**: 
    - You can rename `assets/alarm.mp3.example` to `assets/alarm.mp3`.
    - Or use your own `.mp3` file and save it as `alarm.mp3` in the `assets/` folder.

## 🎮 How to Use

Run the application using:
```bash
python main.py
```

### System Tray Navigation
Once running, look for the green square icon in your system tray:
- **Pause/Resume Detection**: Stop or restart monitoring.
- **Show/Hide Camera**: Display the camera window to see the AI detection in action.
- **Quit**: Close the application completely.

## ⚙️ How It Works
The system calculates the vertical distance between the forehead, nose, and chin. If the nose-to-chin distance decreases significantly compared to the forehead-to-nose distance, the system identifies a "tilted down" position. If this position persists for several consecutive frames, the alarm is triggered.

## 📄 License
[MIT License](LICENSE) - Feel free to use and develop further!
