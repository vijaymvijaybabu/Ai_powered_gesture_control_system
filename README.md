# 🖐️ AI Hand Gesture Recognition & Computer Control System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![Flask](https://img.shields.io/badge/Flask-Web%20Application-lightgrey)
![License](https://img.shields.io/badge/License-MIT-red)

## 📌 Project Overview

The **AI Hand Gesture Recognition & Computer Control System** is a real-time Computer Vision application that enables users to interact with their computer using hand gestures instead of traditional input devices like a keyboard and mouse.

The system utilizes **MediaPipe** for accurate hand landmark detection, **OpenCV** for image processing, and a custom gesture classification model to recognize gestures in real time. Recognized gestures are mapped to various computer actions such as cursor movement, clicking, scrolling, drawing, and media control.

A Flask-based web interface provides live camera streaming, gesture visualization, image prediction, gesture history, and system controls.

---

# 🎯 Features

✅ Real-Time Hand Gesture Recognition

✅ AI-Based Gesture Classification

✅ Cursor Movement using Hand Tracking

✅ Left Click

✅ Right Click

✅ Double Click

✅ Scroll Up / Scroll Down

✅ Air Drawing

✅ Live Gesture Confidence Score

✅ Hand Landmark Detection

✅ Image-Based Gesture Prediction

✅ Gesture History Tracking

✅ Live FPS Monitoring

✅ Flask Web Dashboard

✅ Upload Image for Gesture Prediction

---

# 🛠️ Technologies Used

### Programming Language
- Python

### Computer Vision
- OpenCV
- MediaPipe

### Machine Learning
- NumPy
- Custom Gesture Classifier

### Web Framework
- Flask

### Automation
- PyAutoGUI

### Frontend
- HTML
- CSS
- JavaScript

---

# 🏗️ System Architecture

```
Web Camera
     │
     ▼
Frame Capture
     │
     ▼
MediaPipe Hand Detection
     │
     ▼
21 Hand Landmarks
     │
     ▼
Gesture Classification
     │
     ▼
Gesture Recognition
     │
     ▼
Computer Action Execution
     │
     ▼
Flask Dashboard
```

---

# 📂 Project Structure

```
AI-Hand-Gesture-Control/

│── static/
│── templates/
│── utils/
│── models/
│── dataset/
│── app.py
│── train_model.py
│── requirements.txt
│── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AI-Hand-Gesture-Control.git

cd AI-Hand-Gesture-Control
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 📷 Supported Gestures

| Gesture | Action |
|----------|--------|
| Open Palm | Cursor Movement |
| Fist | Clear Drawing |
| Point Up | Air Drawing |
| Victory | Left Click |
| Thumb Up | Right Click |
| Pinch | Scroll |
| Custom Gestures | User Defined |

---

# 🧠 AI Pipeline

1. Capture live video
2. Detect hands using MediaPipe
3. Extract 21 hand landmarks
4. Classify gesture using AI model
5. Execute mapped computer action
6. Display confidence score
7. Update gesture history
8. Stream processed video to Flask dashboard

---

# 📊 Project Highlights

- Real-time gesture recognition
- Low latency processing
- Live FPS monitoring
- Smooth hand tracking
- AI-powered gesture classification
- Image upload prediction
- Interactive web interface
- Modular project architecture

---

# 📸 Screenshots

Add screenshots inside the **screenshots/** folder.

Example:

```
screenshots/home.png

screenshots/live_detection.png

screenshots/gesture_history.png

screenshots/image_prediction.png
```

---

# 🎥 Demo

Add your YouTube demo here.

Example

https://youtu.be/your-demo-link

---

# 📚 Future Improvements

- Voice Assistant Integration
- Sign Language Recognition
- Gesture Customization
- Multi-Hand Collaboration
- Virtual Mouse
- Virtual Keyboard
- AI Drawing Assistant
- Volume & Brightness Control
- Presentation Control
- Smart Home Integration
- Deep Learning Gesture Recognition
- Mobile Version

---

# 💻 Skills Demonstrated

- Artificial Intelligence
- Machine Learning
- Computer Vision
- Hand Tracking
- Gesture Recognition
- Image Processing
- OpenCV
- MediaPipe
- Flask
- Python
- Human Computer Interaction
- Real-Time AI Systems

---

# 👨‍💻 Author

**Macherla Manohar Babu**

🎓 MCA Student | AI & Machine Learning Engineer

📧 Email: yourmail@gmail.com

🔗 GitHub: https://github.com/yourusername

🔗 LinkedIn: https://linkedin.com/in/yourprofile

---

# ⭐ Support

If you like this project, don't forget to ⭐ star the repository.

It motivates future improvements and helps others discover the project.

---

# 📄 License

This project is licensed under the MIT License.
