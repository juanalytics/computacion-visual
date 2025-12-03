from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import yaml

from python.detection.scripts import helpers


class DummyTensor:
    def __init__(self, data):
        self._data = np.array(data, dtype=float)

    def cpu(self):
        return self

    def numpy(self):
        return self._data


class DummyBoxes:
    def __init__(self):
        self.xyxy = DummyTensor([[0, 1, 2, 3]])
        self.conf = DummyTensor([0.9])
        self.cls = DummyTensor([0])


class DummyResult:
    def __init__(self):
        self.boxes = DummyBoxes()
        self.names: Dict[int, str] = {0: "person"}


def test_detections_to_items():
    result = DummyResult()
    items = helpers.detections_to_items(result)
    assert len(items) == 1
    assert items[0]["label"] == "person"
    assert items[0]["bbox"] == [0.0, 1.0, 2.0, 3.0]
    assert 0 <= items[0]["confidence"] <= 1


def test_build_detection_message_schema():
    result = DummyResult()
    message = helpers.build_detection_message(result, fps=30.0, latency_ms=15.0)
    assert message["module"] == "detection"
    assert message["type"] == "detections"
    payload = message["payload"]
    assert payload["fps"] == 30.0
    assert payload["latency_ms"] == 15.0
    assert len(payload["items"]) == 1


def test_load_config(tmp_path: Path):
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.dump({"model_path": "foo.pt"}), encoding="utf-8")
    cfg = helpers.load_config(cfg_path)
    assert cfg["model_path"] == "foo.pt"

