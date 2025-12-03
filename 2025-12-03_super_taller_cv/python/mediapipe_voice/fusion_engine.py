"""
Combina eventos de gestos, voz y EEG en un comando final.
"""

from __future__ import annotations

import argparse
import json
import queue
import threading
import time
from pathlib import Path
from typing import Dict, Optional

from python.detection.scripts.inference import WebSocketPublisher


class FusionEngine:
    def __init__(self, ws_url: str | None):
        self.ws_url = ws_url
        self.event_queue: "queue.Queue[Dict]" = queue.Queue()
        self.state = {
            "gesture": None,
            "voice": None,
            "eeg": None,
        }

    def add_event(self, event: Dict) -> None:
        self.event_queue.put(event)

    def process_event(self, event: Dict) -> Optional[Dict]:
        etype = event.get("type")
        payload = event.get("payload", {})
        if etype == "command":
            source = payload.get("source")
            self.state[source] = payload
        elif etype == "eeg_sample":
            self.state["eeg"] = payload

        gesture_action = (self.state.get("gesture") or {}).get("action")
        voice_action = (self.state.get("voice") or {}).get("action")
        eeg_value = (self.state.get("eeg") or {}).get("value", 0)

        if voice_action:
            return {
                "timestamp": time.time(),
                "module": "multimodal",
                "type": "fusion_command",
                "payload": {
                    "action": voice_action,
                    "source": "voice",
                    "confidence": 0.9,
                },
            }

        if gesture_action and eeg_value and eeg_value > 0.8:
            return {
                "timestamp": time.time(),
                "module": "multimodal",
                "type": "fusion_command",
                "payload": {
                    "action": gesture_action,
                    "source": "gesture+eeg",
                    "confidence": 0.85,
                    "params": {"eeg_value": eeg_value},
                },
            }
        return None

    def run(self):
        with WebSocketPublisher(self.ws_url) as publisher:
            while True:
                event = self.event_queue.get()
                result = self.process_event(event)
                if result:
                    publisher.publish(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fusiona eventos multimodales desde JSON.")
    parser.add_argument("--events", type=Path, required=True, help="Archivo JSON con lista de eventos.")
    parser.add_argument("--ws-url", type=str, help="WebSocket destino.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    events = json.loads(args.events.read_text(encoding="utf-8"))
    engine = FusionEngine(args.ws_url)

    thread = threading.Thread(target=engine.run, daemon=True)
    thread.start()

    for event in events:
        engine.add_event(event)
        time.sleep(0.5)

    time.sleep(1.0)


if __name__ == "__main__":
    main()

