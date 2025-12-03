"""
Genera segmentaciones semánticas usando modelos de TorchVision.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import numpy as np
import torch
from PIL import Image
import torch.nn.functional as F
from torchvision.models.segmentation import (
    DeepLabV3_ResNet101_Weights,
    DeepLabV3_ResNet50_Weights,
    deeplabv3_resnet101,
    deeplabv3_resnet50,
)

from python.detection.scripts.helpers import ensure_dir, load_config

VOC_COLORS = np.array(
    [
        (0, 0, 0),
        (128, 0, 0),
        (0, 128, 0),
        (128, 128, 0),
        (0, 0, 128),
        (128, 0, 128),
        (0, 128, 128),
        (128, 128, 128),
        (64, 0, 0),
        (192, 0, 0),
        (64, 128, 0),
        (192, 128, 0),
        (64, 0, 128),
        (192, 0, 128),
        (64, 128, 128),
        (192, 128, 128),
        (0, 64, 0),
        (128, 64, 0),
        (0, 192, 0),
        (128, 192, 0),
        (0, 64, 128),
    ],
    dtype=np.uint8,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Segmentación semántica por lotes.")
    parser.add_argument("--config", type=Path, help="Archivo YAML con configuración base.")
    parser.add_argument("--model", type=str, help="Nombre del modelo (deeplabv3_resnet50/resnet101).")
    parser.add_argument("--input", type=Path, required=True, help="Imagen o carpeta con imágenes.")
    parser.add_argument("--output-dir", type=Path, help="Carpeta para las máscaras (.png).")
    parser.add_argument("--overlay-dir", type=Path, help="Carpeta para overlays con la imagen original.")
    parser.add_argument("--limit", type=int, help="Número máximo de imágenes a procesar.")
    parser.add_argument("--palette", choices=["voc"], default="voc", help="Paleta de colores para mascaras.")
    return parser.parse_args()


def list_images(target: Path) -> List[Path]:
    if not target.exists():
        raise FileNotFoundError(f"No existe la ruta de entrada: {target}")
    if target.is_file():
        return [target]
    images: List[Path] = []
    for path in sorted(target.rglob("*")):
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}:
            images.append(path)
    if not images:
        raise RuntimeError(f"No se encontraron imágenes soportadas en {target}")
    return images


def load_model(name: str):
    name = name.lower()
    if name == "deeplabv3_resnet50":
        weights = DeepLabV3_ResNet50_Weights.DEFAULT
        model = deeplabv3_resnet50(weights=weights).eval()
    elif name == "deeplabv3_resnet101":
        weights = DeepLabV3_ResNet101_Weights.DEFAULT
        model = deeplabv3_resnet101(weights=weights).eval()
    else:
        raise ValueError(f"Modelo no soportado: {name}")
    return model, weights.transforms()


def mask_to_color(mask: np.ndarray, palette: str) -> np.ndarray:
    if palette == "voc":
        colors = VOC_COLORS
    else:
        raise ValueError(f"Paleta no soportada: {palette}")

    mask = mask.astype(np.int32)
    mask = np.clip(mask, 0, len(colors) - 1)
    return colors[mask]


def build_metadata(
    image_path: Path,
    mask_path: Path,
    overlay_path: Optional[Path],
    classes: Dict[int, int],
) -> Dict[str, object]:
    return {
        "image": str(image_path),
        "mask": str(mask_path),
        "overlay": str(overlay_path) if overlay_path else None,
        "class_histogram": classes,
    }


def process_image(
    model,
    transforms,
    image_path: Path,
    mask_output: Path,
    overlay_output: Optional[Path],
    palette: str,
) -> Dict[str, object]:
    image = Image.open(image_path).convert("RGB")
    batch = transforms(image).unsqueeze(0)

    with torch.no_grad():
        output = model(batch)["out"]
        upsampled = F.interpolate(output, size=image.size[::-1], mode="bilinear", align_corners=False)
        mask = torch.argmax(upsampled, dim=1)[0].cpu().numpy().astype(np.uint8)

    color_mask = mask_to_color(mask, palette)
    Image.fromarray(mask, mode="L").save(mask_output)

    overlay_path = None
    if overlay_output:
        overlay = Image.blend(
            image,
            Image.fromarray(color_mask).convert("RGB"),
            alpha=0.5,
        )
        overlay.save(overlay_output)
        overlay_path = overlay_output

    unique, counts = np.unique(mask, return_counts=True)
    class_hist = {int(k): int(v) for k, v in zip(unique, counts)}

    return build_metadata(image_path, mask_output, overlay_path, class_hist)


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)

    model_name = args.model or cfg.get("segment_model", "deeplabv3_resnet50")
    mask_dir = ensure_dir(args.output_dir or Path(cfg.get("segment_output", "results/detection/segment/masks")))
    overlay_dir = ensure_dir(args.overlay_dir or Path(cfg.get("segment_overlay", "")) if cfg.get("segment_overlay") else None)

    model, transforms = load_model(model_name)
    files = list_images(args.input)
    if args.limit:
        files = files[: args.limit]

    metadata = []
    for image_path in files:
        mask_path = mask_dir / f"{image_path.stem}_mask.png"
        overlay_path = overlay_dir / f"{image_path.stem}_overlay.png" if overlay_dir else None
        record = process_image(model, transforms, image_path, mask_path, overlay_path, args.palette)
        metadata.append(record)
        print(f"[segment] Procesada {image_path} -> {mask_path}")

    summary_path = mask_dir / "metadata.json"
    summary_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"[segment] Resumen guardado en {summary_path}")


if __name__ == "__main__":
    main()

