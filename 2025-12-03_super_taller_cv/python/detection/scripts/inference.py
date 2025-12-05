"""
Pipeline de inferencia y streaming WebSocket para YOLO.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import cv2
from ultralytics import YOLO

try:
    from websockets.sync.client import connect as ws_connect
except ImportError:  # pragma: no cover
    ws_connect = None

from python.detection.scripts.helpers import (
    build_detection_message,
    ensure_dir,
    load_config,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inferencia YOLO + publicación WebSocket.")
    parser.add_argument("--config", type=Path, help="Ruta a archivo YAML de configuración.")
    parser.add_argument("--model", type=str, help="Ruta al modelo YOLO.")
    parser.add_argument("--source", type=str, help="Fuente de video (ruta o índice).")
    parser.add_argument("--ws-url", type=str, help="URL del WebSocket.")
    parser.add_argument("--confidence", type=float, help="Umbral de confianza.")
    parser.add_argument("--iou", type=float, help="Umbral IoU para NMS.")
    parser.add_argument("--max-det", type=int, help="Máximo de detecciones por frame.")
    parser.add_argument("--display", action="store_true", help="Mostrar ventana con resultados.")
    parser.add_argument("--save-dir", type=Path, help="Carpeta donde guardar frames anotados.")
    parser.add_argument("--no-emit", action="store_true", help="No enviar eventos al WS.")
    return parser.parse_args()


class WebSocketPublisher:
    def __init__(self, url: Optional[str]):
        self.url = url if url and ws_connect else None
        self.connection = None

    def __enter__(self) -> "WebSocketPublisher":
        if self.url:
            try:
                self.connection = ws_connect(self.url)
                print(f"[WS] Conectado a {self.url}")
            except Exception as exc:  # pragma: no cover
                print(f"[WS] Error al conectar ({exc}); se continúa sin emisión")
                self.connection = None
        return self

    def publish(self, message: Dict[str, Any]) -> None:
        if not self.connection:
            return
        try:
            self.connection.send(json.dumps(message))
        except Exception as exc:  # pragma: no cover
            print(f"[WS] Error enviando mensaje: {exc}")

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.connection:
            self.connection.close()
            print("[WS] Conexión cerrada")


def open_capture(source: Union[str, int]) -> cv2.VideoCapture:
    if isinstance(source, str) and source.isdigit():
        source = int(source)
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente de video: {source}")
    return cap


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)

    model_path = args.model or cfg["model_path"]
    source = args.source if args.source is not None else cfg["source"]
    ws_url = args.ws_url or cfg.get("ws_url")
    confidence = args.confidence if args.confidence is not None else cfg.get("confidence", 0.25)
    iou = args.iou if args.iou is not None else cfg.get("iou", 0.45)
    max_det = args.max_det if args.max_det is not None else cfg.get("max_det", 100)
    display = args.display or cfg.get("display", False)
    save_dir = ensure_dir(args.save_dir or Path(cfg.get("save_dir", "")) if cfg.get("save_dir") else None)
    emit = not args.no_emit and cfg.get("emit", True)

    model = YOLO(model_path)
    cap = open_capture(source)
    frame_idx = 0
    stats: List[Dict[str, float]] = []

    with WebSocketPublisher(ws_url if emit else None) as publisher:
        try:
            while True:
                success, frame = cap.read()
                if not success:
                    print("[inference] Fin del stream o error de captura.")
                    break

                start = time.perf_counter()
                results = model.predict(
                    source=frame,
                    conf=confidence,
                    iou=iou,
                    max_det=max_det,
                    verbose=False,
                )
                latency_ms = (time.perf_counter() - start) * 1000
                fps = 1000.0 / max(latency_ms, 1e-3)
                result = results[0]
                stats.append({"fps": fps, "latency_ms": latency_ms})

                frame_shape = frame.shape[:2]
                message = build_detection_message(
                    result, fps=fps, latency_ms=latency_ms, frame_shape=frame_shape
                )

                if emit:
                    publisher.publish(message)
                    metrics_message = {
                        "timestamp": message["timestamp"],
                        "module": "detection",
                        "type": "metrics",
                        "payload": {"metrics": {"fps": fps, "latency_ms": latency_ms}},
                    }
                    publisher.publish(metrics_message)

                annotated = result.plot() if display or save_dir else None
                if display and annotated is not None:
                    cv2.imshow("detections", annotated)
                    if cv2.waitKey(1) & 0xFF == 27:  # ESC
                        break

                if save_dir and annotated is not None:
                    out_path = save_dir / f"frame_{frame_idx:06d}.jpg"
                    cv2.imwrite(str(out_path), annotated)

                frame_idx += 1
        finally:
            cap.release()
            cv2.destroyAllWindows()

    if save_dir and stats:
        summary = {
            "frames": frame_idx,
            "avg_fps": statistics.fmean(s["fps"] for s in stats),
            "avg_latency_ms": statistics.fmean(s["latency_ms"] for s in stats),
            "config": {
                "model": model_path,
                "source": source,
            },
        }
        metrics_path = save_dir / "metrics.json"
        metrics_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"[inference] Métricas guardadas en {metrics_path}")


if __name__ == "__main__":
    main()

