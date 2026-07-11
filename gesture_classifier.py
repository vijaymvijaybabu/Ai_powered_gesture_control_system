"""
Gesture Classifier — Enhanced AI Gesture Recognition System
Recognizes Multiple Hand Gestures using MediaPipe landmarks.
"""

import numpy as np
import math


class GestureClassifier:

    GESTURES = [
        "Open Palm",
        "Fist",
        "Thumbs Up",
        "Thumbs Down",
        "Peace / V",
        "Point Up",
        "Point Right",
        "Point Left",
        "OK Sign",
        "Rock On",
        "Call Me",
        "Pinch",

        # NEW GESTURES
        "Three Fingers",
        "Four Fingers",
        "Gun Gesture",
        "Heart Sign",
    ]

    # ─────────────────────────────────────────────
    # MediaPipe Landmark Indices
    # ─────────────────────────────────────────────

    WRIST = 0

    THUMB_CMC  = 1
    THUMB_MCP  = 2
    THUMB_IP   = 3
    THUMB_TIP  = 4

    INDEX_MCP  = 5
    INDEX_PIP  = 6
    INDEX_DIP  = 7
    INDEX_TIP  = 8

    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12

    RING_MCP   = 13
    RING_PIP   = 14
    RING_DIP   = 15
    RING_TIP   = 16

    PINKY_MCP  = 17
    PINKY_PIP  = 18
    PINKY_DIP  = 19
    PINKY_TIP  = 20

    # ─────────────────────────────────────────────
    # INIT
    # ─────────────────────────────────────────────

    def __init__(self):
        pass

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────

    def _dist(self, a, b):

        return math.sqrt(
            sum((a[i] - b[i]) ** 2 for i in range(3))
        )

    def _finger_extended(self, lm, tip, pip, mcp):

        wrist = lm[self.WRIST]

        return self._dist(lm[tip], wrist) > \
               self._dist(lm[pip], wrist)

    def _finger_curled(self, lm, tip, pip):

        wrist = lm[self.WRIST]

        return self._dist(lm[tip], wrist) < \
               self._dist(lm[pip], wrist)

    def _thumb_extended(self, lm):

        return self._dist(
            lm[self.THUMB_TIP],
            lm[self.INDEX_MCP]
        ) > self._dist(
            lm[self.THUMB_IP],
            lm[self.INDEX_MCP]
        )

    def _fingers_state(self, lm):

        """
        Returns:
        [thumb, index, middle, ring, pinky]
        """

        return [

            self._thumb_extended(lm),

            self._finger_extended(
                lm,
                self.INDEX_TIP,
                self.INDEX_PIP,
                self.INDEX_MCP
            ),

            self._finger_extended(
                lm,
                self.MIDDLE_TIP,
                self.MIDDLE_PIP,
                self.MIDDLE_MCP
            ),

            self._finger_extended(
                lm,
                self.RING_TIP,
                self.RING_PIP,
                self.RING_MCP
            ),

            self._finger_extended(
                lm,
                self.PINKY_TIP,
                self.PINKY_PIP,
                self.PINKY_MCP
            ),
        ]

    def _pointing_direction(self, lm):

        dx = lm[self.INDEX_TIP][0] - \
             lm[self.INDEX_MCP][0]

        dy = lm[self.INDEX_TIP][1] - \
             lm[self.INDEX_MCP][1]

        angle = math.degrees(
            math.atan2(-dy, dx)
        )

        if -45 < angle <= 45:
            return "right"

        elif 45 < angle <= 135:
            return "up"

        elif angle > 135 or angle <= -135:
            return "left"

        return "down"

    # ─────────────────────────────────────────────
    # MAIN CLASSIFIER
    # ─────────────────────────────────────────────

    def classify(self, lm_list):

        """
        lm_list:
        List of 21 hand landmarks

        Returns:
        (gesture_name, confidence)
        """

        lm = lm_list

        fs = self._fingers_state(lm)

        thumb, index, middle, ring, pinky = fs

        # ─────────────────────────────────────────
        # FIST
        # ─────────────────────────────────────────

        if not any(fs):

            return "Fist", 0.95

        # ─────────────────────────────────────────
        # OPEN PALM
        # ─────────────────────────────────────────

        if all(fs):

            return "Open Palm", 0.95

        # ─────────────────────────────────────────
        # THUMBS UP / DOWN
        # ─────────────────────────────────────────

        if thumb and not index and not middle and not ring and not pinky:

            thumb_tip_y = lm[self.THUMB_TIP][1]

            wrist_y = lm[self.WRIST][1]

            if thumb_tip_y < wrist_y - 0.05:

                return "Thumbs Up", 0.92

            else:

                return "Thumbs Down", 0.88

        # ─────────────────────────────────────────
        # POINT GESTURES
        # ─────────────────────────────────────────

        if index and not middle and not ring and not pinky and not thumb:

            direction = self._pointing_direction(lm)

            if direction == "up":

                return "Point Up", 0.90

            elif direction == "right":

                return "Point Right", 0.88

            elif direction == "left":

                return "Point Left", 0.88

        # ─────────────────────────────────────────
        # PEACE / V
        # ─────────────────────────────────────────

        if index and middle and not ring and not pinky and not thumb:

            spread = self._dist(
                lm[self.INDEX_TIP],
                lm[self.MIDDLE_TIP]
            )

            if spread > 0.04:

                return "Peace / V", 0.92

            return "Peace / V", 0.82

        # ─────────────────────────────────────────
        # OK SIGN
        # ─────────────────────────────────────────

        thumb_index_dist = self._dist(
            lm[self.THUMB_TIP],
            lm[self.INDEX_TIP]
        )

        if thumb_index_dist < 0.05 and middle and ring and pinky:

            return "OK Sign", 0.91

        # ─────────────────────────────────────────
        # ROCK ON
        # ─────────────────────────────────────────

        if index and pinky and not middle and not ring:

            return "Rock On", 0.90

        # ─────────────────────────────────────────
        # CALL ME
        # ─────────────────────────────────────────

        if thumb and pinky and not index and not middle and not ring:

            return "Call Me", 0.89

        # ─────────────────────────────────────────
        # PINCH
        # ─────────────────────────────────────────

        if thumb_index_dist < 0.06 and \
           not middle and not ring and not pinky:

            return "Pinch", 0.88

        # ─────────────────────────────────────────
        # THREE FINGERS
        # ─────────────────────────────────────────

        if index and middle and ring and \
           not pinky and not thumb:

            return "Three Fingers", 0.90

        # ─────────────────────────────────────────
        # FOUR FINGERS
        # ─────────────────────────────────────────

        if index and middle and ring and \
           pinky and not thumb:

            return "Four Fingers", 0.91

        # ─────────────────────────────────────────
        # GUN GESTURE
        # ─────────────────────────────────────────

        if thumb and index and \
           not middle and not ring and not pinky:

            return "Gun Gesture", 0.92

        # ─────────────────────────────────────────
        # HEART SIGN
        # ─────────────────────────────────────────

        heart_dist = self._dist(
            lm[self.THUMB_TIP],
            lm[self.INDEX_TIP]
        )

        if heart_dist < 0.03 and \
           middle and not ring and not pinky:

            return "Heart Sign", 0.88

        # ─────────────────────────────────────────
        # UNKNOWN
        # ─────────────────────────────────────────

        extended_count = sum(fs)

        conf = 0.55 + extended_count * 0.04

        return (
            f"Unknown ({extended_count} fingers)",
            min(conf, 0.75)
        )

    # ─────────────────────────────────────────────
    # GESTURE LIST
    # ─────────────────────────────────────────────

    def get_gesture_list(self):

        return [

            {
                "name": g,
                "description":
                GESTURE_DESCRIPTIONS.get(g, "")
            }

            for g in self.GESTURES
        ]


# ─────────────────────────────────────────────
# DESCRIPTIONS
# ─────────────────────────────────────────────

GESTURE_DESCRIPTIONS = {

    "Open Palm": "Stop / Pause media",

    "Fist": "Click / Select",

    "Thumbs Up": "Volume Up / Scroll Up",

    "Thumbs Down": "Volume Down / Scroll Down",

    "Peace / V": "Screenshot",

    "Point Up": "Move cursor up",

    "Point Right": "Move cursor right / Next",

    "Point Left": "Move cursor left / Previous",

    "OK Sign": "Confirm / Enter",

    "Rock On": "Mute / Unmute",

    "Call Me": "Open phone / Dial",

    "Pinch": "Drag / Select text",

    # NEW

    "Three Fingers": "Copy Action",

    "Four Fingers": "Paste Action",

    "Gun Gesture": "Escape / Close",

    "Heart Sign": "Show Desktop",
}  