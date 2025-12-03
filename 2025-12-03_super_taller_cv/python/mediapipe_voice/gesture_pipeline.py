"""
Pipeline de gestos usando MediaPipe Hands.
"""

from __future__ import annotations

import argparse
import collections
import json
import time
from pathlib import Path
from typing import Deque, Dict, Optional

import cv2
import mediapipe as mp
import numpy as np

from python.mediapipe_voice.utils import load_config
from python.detection.scripts.helpers import ensure_dir
from python.detection.scripts.inference import WebSocketPublisher  # reuse

GESTURE_OPEN = "open_palm"
GESTURE_FIST = "fist"
GESTURE_POINT = "point"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detecta gestos básicos con MediaPipe Hands.")
    parser.add_argument("--config", type=Path, help="Archivo YAML de configuración.")
    parser.add_argument("--source", type=str, default="0", help="Webcam (0) o ruta a video.")
    parser.add_argument("--ws-url", type=str, help="WebSocket para emitir comandos.")
    parser.add_argument("--save-dir", type=Path, help="Guardar frames anotados.")
    parser.add_argument("--display", action="store_true", help="Mostrar preview en ventana.")
    parser.add_argument("--max-frames", type=int, help="Procesar solo N frames (para pruebas).")
    return parser.parse_args()


def classify_gesture(hand_landmarks) -> str | None:
    landmarks = np.array([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])
    wrist = landmarks[0]
    tips = landmarks[[4, 8, 12, 16, 20]]
    dip = landmarks[[3, 7, 11, 15, 19]]
    extended = np.linalg.norm(tips[:, :2] - wrist[:2], axis=1) > np.linalg.norm(dip[:, :2] - wrist[:2], axis=1) * 1.2
    count = extended.sum()
    if count >= 4:
        return GESTURE_OPEN
    if count <= 1:
        return GESTURE_FIST
    if extended[1] and not extended[2:].any():
        return GESTURE_POINT
    return None


def gesture_to_command(gesture: str, mapping: Dict[str, str]) -> Dict[str, str] | None:
    if gesture not in mapping:
        return None
    return {"action": mapping[gesture], "source": "gesture", "params": {}}


def open_capture(source: str):
    if source.isdigit():
        cap = cv2.VideoCapture(int(source))
    else:
        cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente {source}")
    return cap


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    ws_url = args.ws_url or cfg.get("ws_url")
    save_dir = ensure_dir(args.save_dir)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=cfg["gesture"].get("min_detection_confidence", 0.7),
        min_tracking_confidence=cfg["gesture"].get("min_tracking_confidence", 0.5),
    )
    drawing = mp.solutions.drawing_utils
    history: Deque[str] = collections.deque(maxlen=cfg["gesture"].get("history_size", 5))

    cap = open_capture(str(args.source))
    frame_idx = 0

    with WebSocketPublisher(ws_url) as publisher:
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)
                gesture_label = None
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        gesture_label = classify_gesture(hand_landmarks)
                        drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                history.append(gesture_label or "none")

                stable = max(set(history), key=history.count) if history else None
                command = gesture_to_command(stable, cfg["gesture"].get("commands", {}))
                if command:
                    message = {
                        "timestamp": time.time(),
                        "module": "multimodal",
                        "type": "command",
                        "payload": {
                            "action": command["action"],
                            "params": command["params"],
                            "confidence": 0.8,
                            "source": command["source"],
                        },
                    }
                    publisher.publish(message)

                if save_dir:
                    cv2.imwrite(str(save_dir / f"gesture_{frame_idx:05d}.jpg"), frame)
                if args.display:
                    cv2.imshow("gestures", frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                frame_idx += 1
                if args.max_frames and frame_idx >= args.max_frames:
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

