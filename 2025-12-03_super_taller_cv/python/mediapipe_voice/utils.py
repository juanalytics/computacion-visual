"""Utilidades compartidas para el módulo multimodal."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(path: Path | None = None) -> Dict[str, Any]:
    target = path or Path(__file__).resolve().parent / "configs" / "default.yaml"
    if not target.exists():
        raise FileNotFoundError(target)
    with target.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


