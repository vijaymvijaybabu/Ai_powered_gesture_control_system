"""
Gesture Controller — Enhanced AI Gesture Control System
Maps recognised gestures to real OS/computer actions.
Uses PyAutoGUI for:
✔ Mouse control
✔ Keyboard shortcuts
✔ Media control
✔ Smart gestures
"""

import pyautogui
import time
import math

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class GestureController:

    SCREEN_W, SCREEN_H = pyautogui.size()

    # ─────────────────────────────────────────────
    # Debounce Times
    # ─────────────────────────────────────────────

    DEBOUNCE = {

        "Fist": 0.4,

        "Open Palm": 0.8,

        "Thumbs Up": 0.5,

        "Thumbs Down": 0.5,

        "Peace / V": 1.5,

        "OK Sign": 0.6,

        "Rock On": 1.0,

        "Call Me": 1.0,

        "Pinch": 0.1,

        "Point Up": 0.05,

        "Point Right": 0.05,

        "Point Left": 0.05,

        # NEW

        "Three Fingers": 0.8,

        "Four Fingers": 0.8,

        "Gun Gesture": 0.8,

        "Heart Sign": 1.0,
    }

    # ─────────────────────────────────────────────
    # INIT
    # ─────────────────────────────────────────────

    def __init__(self):

        self._last_action_time = {}

        self._last_gesture = None

        self._smooth_x = self.SCREEN_W // 2

        self._smooth_y = self.SCREEN_H // 2

        self._pinch_start = None

        self._gesture_hold_start = None

    # ─────────────────────────────────────────────
    # INTERNAL HELPERS
    # ─────────────────────────────────────────────

    def _debounced(self, gesture) -> bool:

        now = time.time()

        delay = self.DEBOUNCE.get(gesture, 0.5)

        last = self._last_action_time.get(gesture, 0)

        if now - last >= delay:

            self._last_action_time[gesture] = now

            return True

        return False

    def _map_to_screen(self, x, y, margin=0.1):

        """
        Map normalized hand coords
        to screen coordinates
        """

        x = (x - margin) / (1 - 2 * margin)

        y = (y - margin) / (1 - 2 * margin)

        x = max(0.0, min(1.0, x))

        y = max(0.0, min(1.0, y))

        return (
            int(x * self.SCREEN_W),
            int(y * self.SCREEN_H)
        )

    def _smooth_move(self, tx, ty, factor=0.25):

        self._smooth_x += (tx - self._smooth_x) * factor

        self._smooth_y += (ty - self._smooth_y) * factor

        pyautogui.moveTo(
            int(self._smooth_x),
            int(self._smooth_y)
        )

    # ─────────────────────────────────────────────
    # MAIN EXECUTION FUNCTION
    # ─────────────────────────────────────────────

    def execute(self, gesture: str, lm: list, frame_shape) -> str:

        """
        Execute OS action based on gesture

        lm:
        List of 21 hand landmarks

        Returns:
        Human readable action string
        """

        INDEX_TIP = 8

        WRIST = 0

        # ─────────────────────────────────────────
        # CURSOR MOVEMENT
        # ─────────────────────────────────────────

        if gesture in (
            "Point Up",
            "Point Right",
            "Point Left"
        ):

            tx, ty = self._map_to_screen(
                lm[INDEX_TIP][0],
                lm[INDEX_TIP][1]
            )

            self._smooth_move(tx, ty)

            return (
                f"🖱 Move cursor → "
                f"({int(self._smooth_x)}, "
                f"{int(self._smooth_y)})"
            )

        # ─────────────────────────────────────────
        # FIST = LEFT CLICK
        # ─────────────────────────────────────────

        if gesture == "Fist" and self._debounced(gesture):

            pyautogui.click()

            return "🖱 Left Click"

        # ─────────────────────────────────────────
        # OPEN PALM = PLAY / PAUSE
        # ─────────────────────────────────────────

        if gesture == "Open Palm" and self._debounced(gesture):

            pyautogui.press("space")

            return "⏸ Play / Pause"

        # ─────────────────────────────────────────
        # THUMBS UP = VOLUME UP
        # ─────────────────────────────────────────

        if gesture == "Thumbs Up" and self._debounced(gesture):

            pyautogui.press("volumeup")

            return "🔊 Volume Up"

        # ─────────────────────────────────────────
        # THUMBS DOWN = VOLUME DOWN
        # ─────────────────────────────────────────

        if gesture == "Thumbs Down" and self._debounced(gesture):

            pyautogui.press("volumedown")

            return "🔉 Volume Down"

        # ─────────────────────────────────────────
        # PEACE = SCREENSHOT
        # ─────────────────────────────────────────

        if gesture == "Peace / V" and self._debounced(gesture):

            pyautogui.hotkey("ctrl", "shift", "s")

            return "📸 Screenshot"

        # ─────────────────────────────────────────
        # OK SIGN = ENTER
        # ─────────────────────────────────────────

        if gesture == "OK Sign" and self._debounced(gesture):

            pyautogui.press("enter")

            return "✅ Enter / Confirm"

        # ─────────────────────────────────────────
        # ROCK ON = MUTE
        # ─────────────────────────────────────────

        if gesture == "Rock On" and self._debounced(gesture):

            pyautogui.press("volumemute")

            return "🔇 Mute Toggle"

        # ─────────────────────────────────────────
        # CALL ME = NEXT TRACK
        # ─────────────────────────────────────────

        if gesture == "Call Me" and self._debounced(gesture):

            pyautogui.press("nexttrack")

            return "⏭ Next Track"

        # ─────────────────────────────────────────
        # PINCH = SCROLL
        # ─────────────────────────────────────────

        if gesture == "Pinch" and self._debounced(gesture):

            wrist_y = lm[WRIST][1]

            if wrist_y < 0.45:

                pyautogui.scroll(3)

                return "⬆ Scroll Up"

            else:

                pyautogui.scroll(-3)

                return "⬇ Scroll Down"

        # ─────────────────────────────────────────
        # THREE FINGERS = COPY
        # ─────────────────────────────────────────

        if gesture == "Three Fingers" and self._debounced(gesture):

            pyautogui.hotkey("ctrl", "c")

            return "📋 Copy"

        # ─────────────────────────────────────────
        # FOUR FINGERS = PASTE
        # ─────────────────────────────────────────

        if gesture == "Four Fingers" and self._debounced(gesture):

            pyautogui.hotkey("ctrl", "v")

            return "📥 Paste"

        
        # GUN GESTURE = ESCAPE
        
        if gesture == "Gun Gesture" and self._debounced(gesture):

            pyautogui.press("esc")

            return "❌ Escape"

        
        # HEART SIGN = SHOW DESKTOP
        

        if gesture == "Heart Sign" and self._debounced(gesture):

            pyautogui.hotkey("win", "d")

            return "🖥 Show Desktop"

       
        # DEFAULT
        

        return "—" 