

from flask import Flask, render_template, Response, jsonify, request
from werkzeug.utils import secure_filename

import cv2
import mediapipe as mp
import numpy as np
import json
import time
import threading
import pyautogui
import math
import os
import base64

from utils.gesture_classifier import GestureClassifier
from utils.gesture_controller import GestureController

app = Flask(__name__)

pyautogui.FAILSAFE = False


# CONFIG

UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# GLOBAL STATE

camera = None

camera_lock = threading.Lock()

gesture_history = []

drawing_points = []

gesture_state = {
    "current_gesture": "None",
    "confidence": 0.0,
    "action": "None",
    "fps": 0,
    "landmarks": [],
    "hand_detected": False,
    "control_enabled": True,
}


# MEDIAPIPE

mp_hands = mp.solutions.hands

mp_drawing = mp.solutions.drawing_utils

mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)


# CLASSIFIER + CONTROLLER

classifier = GestureClassifier()

controller = GestureController()


# CAMERA

def get_camera():

    global camera

    with camera_lock:

        if camera is None or not camera.isOpened():

            camera = cv2.VideoCapture(0)

            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            camera.set(cv2.CAP_PROP_FPS, 30)

    return camera


# PROCESS FRAME


def process_frame(frame):

    global gesture_state

    start = time.time()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    gesture_state["hand_detected"] = False

    gesture_state["landmarks"] = []

    if results.multi_hand_landmarks:

        gesture_state["hand_detected"] = True

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            # Extract landmarks
            lm_list = []

            for lm in hand_landmarks.landmark:

                lm_list.append([lm.x, lm.y, lm.z])

                gesture_state["landmarks"].append({
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z
                })

            # Predict gesture
            gesture, confidence = classifier.classify(lm_list)

            gesture_state["current_gesture"] = gesture

            gesture_state["confidence"] = round(float(confidence), 3)

            # Gesture history
            gesture_history.append({
                "gesture": gesture,
                "confidence": round(float(confidence), 3),
                "time": time.strftime("%H:%M:%S")
            })

            # Keep only latest 10
            gesture_history[:] = gesture_history[-10:]

            # Execute actions
            if gesture_state["control_enabled"]:

                action = controller.execute(
                    gesture,
                    lm_list,
                    frame.shape
                )

                gesture_state["action"] = action

            else:

                gesture_state["action"] = "Control Disabled"

           
            # AIR DRAWING
            

            if gesture == "Point Up":

                x = int(lm_list[8][0] * frame.shape[1])

                y = int(lm_list[8][1] * frame.shape[0])

                drawing_points.append((x, y))

            if gesture == "Fist":

                drawing_points.clear()

            for i in range(1, len(drawing_points)):

                cv2.line(
                    frame,
                    drawing_points[i - 1],
                    drawing_points[i],
                    (0, 255, 255),
                    3
                )

            # Overlay
            _draw_overlay(frame, gesture, confidence)

    else:

        gesture_state["current_gesture"] = "No Hand"

        gesture_state["confidence"] = 0.0

        gesture_state["action"] = "—"

        cv2.putText(
            frame,
            "No hand detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (100, 100, 100),
            2
        )

    fps = 1.0 / (time.time() - start + 1e-9)

    gesture_state["fps"] = round(fps, 1)

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (frame.shape[1] - 120, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 100),
        2
    )

    return frame


# OVERLAY

def _draw_overlay(frame, gesture, confidence):

    h, w, _ = frame.shape

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (w, 70),
        (15, 15, 30),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.7,
        frame,
        0.3,
        0,
        frame
    )

    color = (
        (0, 255, 150)
        if confidence > 0.85
        else (0, 200, 255)
        if confidence > 0.65
        else (0, 120, 255)
    )

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (15, 30),
        cv2.FONT_HERSHEY_DUPLEX,
        0.9,
        color,
        2
    )

    cv2.putText(
        frame,
        f"Confidence: {confidence:.0%}",
        (15, 58),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (200, 200, 200),
        1
    )

    # Confidence bar
    bar_w = int(300 * confidence)

    cv2.rectangle(
        frame,
        (w - 320, 20),
        (w - 20, 40),
        (40, 40, 60),
        -1
    )

    cv2.rectangle(
        frame,
        (w - 320, 20),
        (w - 320 + bar_w, 40),
        color,
        -1
    )


# IMAGE PREDICTION

def process_uploaded_image(image_path):

    image = cv2.imread(image_path)

    if image is None:

        return {
            "success": False,
            "message": "Unable to read image"
        }

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if not results.multi_hand_landmarks:

        return {
            "success": False,
            "message": "No hand detected"
        }

    hand_landmarks = results.multi_hand_landmarks[0]

    lm_list = []

    for lm in hand_landmarks.landmark:

        lm_list.append([lm.x, lm.y, lm.z])

    gesture, confidence = classifier.classify(lm_list)

    # Draw landmarks
    mp_drawing.draw_landmarks(
        image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style(),
    )

    output_path = os.path.join(
        UPLOAD_FOLDER,
        "predicted_" + os.path.basename(image_path)
    )

    cv2.imwrite(output_path, image)

    return {
        "success": True,
        "gesture": gesture,
        "confidence": round(float(confidence), 3),
        "image_url": "/" + output_path.replace("\\", "/")
    }


# VIDEO STREAM


def gen_frames():

    cap = get_camera()

    while True:

        with camera_lock:

            success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        frame = process_frame(frame)

        ret, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 85]
        )

        if not ret:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )


# ROUTES


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(
        gen_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/gesture_data")
def gesture_data():
    return jsonify(gesture_state)

@app.route("/gesture_history")
def get_gesture_history():
    return jsonify(gesture_history)

@app.route("/toggle_control", methods=["POST"])
def toggle_control():

    gesture_state["control_enabled"] = \
        not gesture_state["control_enabled"]

    return jsonify({
        "control_enabled":
        gesture_state["control_enabled"]
    })

@app.route("/gestures_list")
def gestures_list():
    return jsonify(classifier.get_gesture_list())

@app.route("/predict_image", methods=["POST"])
def predict_image():

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "message": "No image uploaded"
        })

    file = request.files["image"]

    if file.filename == "":

        return jsonify({
            "success": False,
            "message": "Empty filename"
        })

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    result = process_uploaded_image(filepath)

    return jsonify(result)



if __name__ == "__main__":

    print("🖐 Hand Gesture Recognition System starting...")

    print("Open http://127.0.0.1:5000 in your browser")

    app.run(
        debug=False,
        host="0.0.0.0", 
        port=5000,
        threaded=True
    ) 