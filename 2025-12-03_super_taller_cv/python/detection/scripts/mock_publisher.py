"""
Genera detecciones simuladas y las envía al WebSocket para pruebas del overlay.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import random
import time
from typing import List

import websockets


def build_fake_boxes(max_boxes: int, width: int, height: int) -> List[dict]:
    boxes = []
    for idx in range(random.randint(1, max_boxes)):
        w = random.uniform(0.1, 0.3) * width
        h = random.uniform(0.1, 0.3) * height
        x = random.uniform(0, width - w)
        y = random.uniform(0, height - h)
        boxes.append(
            {
                "id": idx,
                "label": random.choice(["person", "hand", "object"]),
                "confidence": round(random.uniform(0.6, 0.95), 2),
                "bbox": [x, y, x + w, y + h],
            }
        )
    return boxes


async def publisher(url: str, width: int, height: int, interval: float) -> None:
    print(f"[mock] Connecting to {url}")
    async with websockets.connect(url) as ws:
        while True:
            payload = {
                "timestamp": time.time(),
                "module": "mock_detection",
                "type": "detections",
                "payload": {
                    "fps": 30,
                    "latency_ms": 40,
                    "frame": {"width": width, "height": height},
                    "items": build_fake_boxes(max_boxes=3, width=width, height=height),
                },
            }
            await ws.send(json.dumps(payload))
            await asyncio.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publica detecciones simuladas al WebSocket del dashboard/Three.js."
    )
    parser.add_argument("--ws-url", default="ws://localhost:8000/ws", help="URL del WebSocket.")
    parser.add_argument("--width", type=int, default=1280, help="Ancho del frame simulado.")
    parser.add_argument("--height", type=int, default=720, help="Alto del frame simulado.")
    parser.add_argument("--interval", type=float, default=0.5, help="Segundos entre mensajes.")
    args = parser.parse_args()

    asyncio.run(publisher(args.ws_url, args.width, args.height, args.interval))


if __name__ == "__main__":
    main()

