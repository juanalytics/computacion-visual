"""
Simulador simple de señales EEG para disparar comandos.
"""

from __future__ import annotations

import argparse
import random
import time
from pathlib import Path

from python.mediapipe_voice.utils import load_config
from python.detection.scripts.inference import WebSocketPublisher


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simula valores EEG y emite comandos al WS.")
    parser.add_argument("--config", type=Path, help="Archivo YAML base.")
    parser.add_argument("--interval", type=float, default=1.0, help="Segundos entre muestras.")
    parser.add_argument("--ws-url", type=str, help="WebSocket destino.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    threshold = cfg["eeg"].get("threshold", 0.7)
    ws_url = args.ws_url or cfg.get("ws_url")

    with WebSocketPublisher(ws_url) as publisher:
        last_trigger = 0.0
        cooldown = cfg["eeg"].get("cooldown_seconds", 3)
        while True:
            value = random.random()
            message = {
                "timestamp": time.time(),
                "module": "multimodal",
                "type": "eeg_sample",
                "payload": {"value": value, "threshold": threshold},
            }
            publisher.publish(message)

            if value >= threshold and time.time() - last_trigger > cooldown:
                trigger = {
                    "timestamp": time.time(),
                    "module": "multimodal",
                    "type": "command",
                    "payload": {
                        "action": "trigger_animation",
                        "params": {"intensity": value},
                        "confidence": 0.9,
                        "source": "eeg",
                    },
                }
                publisher.publish(trigger)
                last_trigger = time.time()

            time.sleep(args.interval)


if __name__ == "__main__":
    main()

