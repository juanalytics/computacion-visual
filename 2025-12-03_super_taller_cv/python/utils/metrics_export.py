"""
Utilidad para consolidar métricas de los distintos módulos y almacenarlas en CSV/SQLite.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta métricas a CSV/JSON unificado.")
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Archivo JSON con métricas o carpeta que contenga múltiples JSON.",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("results/metrics.csv"),
        help="Archivo CSV acumulativo.",
    )
    return parser.parse_args()


def iter_metrics(source: Path) -> Dict[str, Any]:
    if source.is_file():
        yield json.loads(source.read_text(encoding="utf-8"))
    else:
        for path in source.glob("*.json"):
            yield json.loads(path.read_text(encoding="utf-8"))


def append_csv(csv_path: Path, rows: list[Dict[str, Any]]) -> None:
    fieldnames = sorted({k for row in rows for k in row.keys()})
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    exists = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    args = parse_args()
    rows: list[Dict[str, Any]] = []
    timestamp = datetime.utcnow().isoformat()

    for metric in iter_metrics(args.input):
        metric["timestamp"] = metric.get("timestamp", timestamp)
        rows.append(metric)

    append_csv(args.csv, rows)
    print(f"[metrics_export] {len(rows)} registros añadidos a {args.csv}")


if __name__ == "__main__":
    main()

