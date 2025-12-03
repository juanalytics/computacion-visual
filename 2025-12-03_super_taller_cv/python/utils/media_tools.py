"""
Helpers para generar GIFs y videos cortos a partir de secuencias de imágenes.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convierte una secuencia de imágenes en GIF/video.")
    parser.add_argument("--input", type=Path, required=True, help="Carpeta con imágenes numeradas.")
    parser.add_argument("--output", type=Path, required=True, help="Ruta del archivo GIF/MP4.")
    parser.add_argument("--fps", type=int, default=12, help="Cuadros por segundo.")
    return parser.parse_args()


def build_command(input_pattern: Path, output: Path, fps: int) -> list[str]:
    return [
        "ffmpeg",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(input_pattern),
        "-vf",
        "scale=iw:-1:flags=lanczos",
        str(output),
    ]


def main() -> None:
    args = parse_args()
    if args.output.suffix.lower() not in {".gif", ".mp4"}:
        raise ValueError("El archivo de salida debe ser .gif o .mp4")

    input_pattern = args.input / "%04d.png"
    cmd = build_command(input_pattern, args.output, args.fps)
    print(f"[media_tools] Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()

