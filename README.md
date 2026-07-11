# 🖐 AI-Powered Hand Gesture Recognition System

Control your computer using hand gestures detected in real-time via your webcam.
Built with **Flask**, **OpenCV**, **MediaPipe**, and a custom ML gesture classifier.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note (Linux):** PyAutoGUI may need extra packages:
> ```bash
> sudo apt-get install python3-tk python3-dev scrot
> pip install python3-xlib
> ```

> **Note (macOS):** Grant Terminal/Python access to Accessibility & Screen Recording in
> System Preferences → Privacy & Security.

### 2. Run the App
```bash
python app.py
```

### 3. Open in Browser
Navigate to **http://127.0.0.1:5000**

---

## 🖐 Supported Gestures & Actions

| Gesture       | Emoji | Action Triggered            |
|---------------|-------|-----------------------------|
| Open Palm     | 🖐    | Play / Pause (Space)        |
| Fist          | ✊    | Left Mouse Click            |
| Thumbs Up     | 👍    | Volume Up                   |
| Thumbs Down   | 👎    | Volume Down                 |
| Peace / V     | ✌️    | Screenshot (Ctrl+Shift+S)   |
| Point Up      | ☝️    | Move Cursor Up              |
| Point Right   | 👉    | Move Cursor Right           |
| Point Left    | 👈    | Move Cursor Left            |
| OK Sign       | 👌    | Enter / Confirm             |
| Rock On       | 🤘    | Mute Toggle                 |
| Call Me       | 🤙    | Next Media Track            |
| Pinch         | 🤏    | Scroll Up / Down            |

---

## 🏗 Project Structure

```
gesture_control/
├── app.py                    # Flask server & video pipeline
├── requirements.txt
├── README.md
├── utils/
│   ├── gesture_classifier.py # ML gesture recognition engine
│   └── gesture_controller.py # OS action executor (PyAutoGUI)
└── templates/
    └── index.html            # Live dashboard UI
```

---

## ⚙️ How It Works

```
Webcam → OpenCV → MediaPipe (21 landmarks) → GestureClassifier → GestureController
                                                     ↓                     ↓
                                               Gesture Name         OS Action (mouse/keyboard)
                                                     ↓
                                             Flask JSON API → Browser Dashboard
```

1. **MediaPipe Hands** detects 21 3D hand landmarks per frame.
2. **GestureClassifier** analyses finger extension states and angles to classify gestures.
3. **GestureController** maps gestures to PyAutoGUI mouse/keyboard/media actions with debouncing.
4. **Flask** serves the video stream (`/video_feed`) and gesture state (`/gesture_data`) as APIs.
5. **Dashboard** polls `/gesture_data` every 100 ms and visualises everything live.

---

## 🛠 Configuration

Edit `utils/gesture_controller.py` to:
- Change debounce delays (prevent repeated triggers)
- Remap gestures to different keyboard shortcuts

Edit `utils/gesture_classifier.py` to:
- Add new gestures
- Adjust detection thresholds

---

## 💻 System Requirements

- Python 3.9+
- Webcam (built-in or USB)
- OS: Windows 10+, macOS 12+, Ubuntu 20.04+
