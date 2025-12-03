"""
Script maestro para descargar y preparar datasets del taller.

Uso:
    python python/utils/prepare_data.py --config configs/data.yaml
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepara datasets para el taller.")
    parser.add_argument(
        "--config",
        type=Path,
        required=False,
        help="Ruta a un archivo JSON/YAML con las fuentes de datos.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed"),
        help="Directorio de salida para los datos procesados.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    # TODO: implementar lógica real de descarga/preprocesado.
    placeholder = args.output / "README_PREPARE_DATA.txt"
    placeholder.write_text(
        "Describe aquí el dataset utilizado, pasos de limpieza y divisiones train/val/test.\n",
        encoding="utf-8",
    )

    metadata = {
        "config": str(args.config) if args.config else None,
        "output": str(args.output),
        "status": "pending_implementation",
    }
    (args.output / "metadata_prepare_data.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    print(f"[prepare_data] Placeholder creado en {args.output}")


if __name__ == "__main__":
    main()

