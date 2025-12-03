# Esquema de mensajes WebSocket (versión 0.1)

Todos los mensajes son JSON con los siguientes campos base:

```json
{
  "timestamp": "ISO-8601",
  "module": "detection|training|multimodal|dashboard|threejs|unity|backend",
  "type": "event",
  "payload": {}
}
```

## Tipos de mensaje

### 1. `detections`

```json
{
  "timestamp": "2025-12-03T15:04:05.000Z",
  "module": "detection",
  "type": "detections",
  "payload": {
    "fps": 42.5,
    "latency_ms": 48,
    "items": [
      {
        "id": 0,
        "label": "person",
        "confidence": 0.95,
        "bbox": [x1, y1, x2, y2],
        "mask_url": "results/2025-12-03/detection/mask_0001.png"
      }
    ]
  }
}
```

### 2. `command`

```json
{
  "timestamp": "2025-12-03T15:04:07.000Z",
  "module": "multimodal",
  "type": "command",
  "payload": {
    "action": "change_material",
    "targets": ["threejs", "unity"],
    "params": {"color": "#33ffaa", "intensity": 0.8},
    "confidence": 0.87,
    "source": "gesture"
  }
}
```

### 3. `metrics`

```json
{
  "timestamp": "2025-12-03T15:04:10.000Z",
  "module": "detection",
  "type": "metrics",
  "payload": {
    "metrics": {
      "fps": 40.1,
      "gpu_usage": 72.3,
      "cpu_usage": 35.0,
      "latency_ms": 50
    }
  }
}
```

### 4. `status`

```json
{
  "timestamp": "2025-12-03T15:04:12.000Z",
  "module": "unity",
  "type": "status",
  "payload": {
    "state": "ready",
    "scene": "FK_Demo",
    "notes": "Listening for commands"
  }
}
```

## Validación

- Implementar validación con `pydantic` o `jsonschema`.
- Rechazar mensajes sin `timestamp`, `module` o `type`.
- Mantener historial de cambios de esquema en este archivo (`CHANGELOG` por versión).

