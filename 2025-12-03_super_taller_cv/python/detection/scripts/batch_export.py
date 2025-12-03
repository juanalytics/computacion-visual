"""
Procesa un conjunto de imágenes/videos y genera anotaciones JSON para evaluación.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import cv2
from ultralytics import YOLO

from python.detection.scripts.helpers import detections_to_items, ensure_dir, load_config

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta detecciones de un lote de archivos.")
    parser.add_argument("--config", type=Path, help="Archivo YAML con configuración base.")
    parser.add_argument("--model", type=str, help="Modelo YOLO a utilizar.")
    parser.add_argument("--input", type=Path, required=True, help="Carpeta o archivo con datos.")
    parser.add_argument("--output-dir", type=Path, help="Carpeta destino para JSON.")
    parser.add_argument("--annotate-dir", type=Path, help="Carpeta donde guardar imágenes anotadas.")
    parser.add_argument("--confidence", type=float, help="Umbral de confianza.")
    parser.add_argument("--iou", type=float, help="Umbral IoU.")
    parser.add_argument("--max-det", type=int, help="Máximo de detecciones por archivo.")
    parser.add_argument("--limit", type=int, help="Número máximo de archivos a procesar.")
    return parser.parse_args()


def gather_inputs(target: Path) -> List[Path]:
    if not target.exists():
        raise FileNotFoundError(f"No se encontró la ruta de entrada: {target}")
    if target.is_file():
        return [target]
    files: List[Path] = []
    for path in sorted(target.rglob("*")):
        if path.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS:
            files.append(path)
    if not files:
        raise RuntimeError(f"No se hallaron archivos soportados en {target}")
    return files


def process_image(model: YOLO, path: Path, conf: float, iou: float, max_det: int):
    results = model.predict(
        source=str(path),
        conf=conf,
        iou=iou,
        max_det=max_det,
        verbose=False,
    )
    return results[0]


def process_video(model: YOLO, path: Path, conf: float, iou: float, max_det: int):
    results = model.predict(
        source=str(path),
        conf=conf,
        iou=iou,
        max_det=max_det,
        stream=True,
        verbose=False,
    )
    for idx, result in enumerate(results):
        yield idx, result


def export_records(records, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"batch_{timestamp}.json"
    payload = {
        "created_at": datetime.utcnow().isoformat(),
        "records": records,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)

    model_path = args.model or cfg["model_path"]
    conf = args.confidence if args.confidence is not None else cfg.get("confidence", 0.25)
    iou = args.iou if args.iou is not None else cfg.get("iou", 0.45)
    max_det = args.max_det if args.max_det is not None else cfg.get("max_det", 100)

    output_dir = args.output_dir or Path(cfg.get("batch_output", "results/detection/batch"))
    annotate_dir = ensure_dir(args.annotate_dir or Path(cfg.get("batch_annotate", "")) if cfg.get("batch_annotate") else None)

    files = gather_inputs(args.input)
    if args.limit:
        files = files[: args.limit]

    model = YOLO(model_path)
    records = []

    for path in files:
        suffix = path.suffix.lower()
        if suffix in IMAGE_EXTS:
            result = process_image(model, path, conf, iou, max_det)
            items = detections_to_items(result)
            record = {
                "source": str(path),
                "timestamp": datetime.utcnow().isoformat(),
                "type": "image",
                "detections": items,
            }
            records.append(record)

            if annotate_dir and items:
                annotated = result.plot()
                out_path = annotate_dir / f"{path.stem}_annotated.jpg"
                cv2.imwrite(str(out_path), annotated)
        elif suffix in VIDEO_EXTS:
            for frame_idx, result in process_video(model, path, conf, iou, max_det):
                items = detections_to_items(result)
                record = {
                    "source": f"{path}:{frame_idx}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "type": "video_frame",
                    "frame_index": frame_idx,
                    "detections": items,
                }
                records.append(record)
        else:
            print(f"[batch_export] Formato no soportado: {path}")

    output_path = export_records(records, output_dir)
    print(f"[batch_export] Exportados {len(records)} registros a {output_path}")


if __name__ == "__main__":
    main()

