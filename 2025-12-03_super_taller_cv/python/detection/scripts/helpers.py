"""
Funciones compartidas para los scripts de detección.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "configs" / "default.yaml"


def load_config(path: Optional[Path] = None) -> Dict[str, Any]:
    target = path or DEFAULT_CONFIG
    if not target.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {target}")
    with target.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def ensure_dir(path: Optional[Path]) -> Optional[Path]:
    if path is None:
        return None
    path.mkdir(parents=True, exist_ok=True)
    return path


def _to_numpy(array) -> Any:
    if hasattr(array, "cpu"):
        array = array.cpu()
    if hasattr(array, "numpy"):
        return array.numpy()
    return array


def detections_to_items(result) -> List[Dict[str, Any]]:
    boxes = getattr(result, "boxes", None)
    names = getattr(result, "names", {})
    items: List[Dict[str, Any]] = []

    if boxes is None:
        return items

    xyxy = _to_numpy(boxes.xyxy)
    conf = _to_numpy(boxes.conf)
    cls = _to_numpy(boxes.cls)

    for idx, (coords, score, label_idx) in enumerate(zip(xyxy, conf, cls)):
        coords_list = [float(v) for v in coords.tolist()] if hasattr(coords, "tolist") else list(coords)
        items.append(
            {
                "id": int(idx),
                "label": names.get(int(label_idx), str(int(label_idx))),
                "confidence": float(score),
                "bbox": coords_list,
            }
        )
    return items


def build_detection_message(result, fps: float, latency_ms: float) -> Dict[str, Any]:
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "module": "detection",
        "type": "detections",
        "payload": {
            "fps": fps,
            "latency_ms": latency_ms,
            "items": detections_to_items(result),
        },
    }

