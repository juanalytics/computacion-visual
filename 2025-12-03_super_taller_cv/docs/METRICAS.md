# Métricas y rendimiento

Consolida aquí todas las métricas cuantitativas solicitadas en la rúbrica.

## 1. Detección y segmentación

| Experimento | Modelo | Dataset | mAP@50 | FPS (GPU) | Latencia (ms) | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| DET-BASE | YOLOv8n | sample_scene.mp4 (CPU) | — | 7.06 | 299 | Video sintético 30 f, métricas escritas en `results/detection/test_run/metrics.json` |
| DET-SAM | YOLOv8s + SAM | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ |

## 2. CNN desde cero vs Fine-Tuning

| Experimento | Arquitectura | Epochs | Accuracy | F1 | Loss val | Comentarios |
| --- | --- | --- | --- | --- | --- | --- |
| CNN-SCRATCH | SimpleCNN | 1 | 0.333 | _(pendiente)_ | 1.735 | Subconjunto 10% CIFAR10, resultados en `results/training/cnn_scratch/metrics.json` |
| FT-RESNET | ResNet50 FT | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ |

## 3. Interacción multimodal

| Pipeline | Latencia promedio (ms) | Precisión gesto | Tasa error voz | Estabilidad EEG | Observaciones |
| --- | --- | --- | --- | --- | --- |
| GESTOS-01 | _(pendiente)_ | _(pendiente)_ | — | — | _(pendiente)_ |
| VOZ-01 | _(pendiente)_ | — | _(pendiente)_ | — | _(pendiente)_ |
| EEG-01 | _(pendiente)_ | — | — | _(pendiente)_ | _(pendiente)_ |

## 4. Visualización 3D / Unity

| Escena | Plataforma | FPS objetivo | FPS medido | VRAM (MB) | Observaciones |
| --- | --- | --- | --- | --- | --- |
| R3F-BASE | Web (Three.js) | 60 | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ |
| UNITY-FK | Unity URP | 60 | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ |

## 5. Backend y dashboards

| Servicio | Throughput (msg/s) | Latencia WS (ms) | Uso CPU (%) | Uso RAM (MB) | Notas |
| --- | --- | --- | --- | --- | --- |
| FastAPI WS | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ | _(pendiente)_ |

## 6. Trazabilidad

- Guardar la fuente de cada métrica en `results/<fecha>/<modulo>/metrics.json`.
- Referenciar experimentos mediante IDs consistentes (ej. `DET-BASE`, `FT-RESNET`).
- Añadir gráficas exportadas (PNG/SVG) en `results/plots/` y enlazarlas desde aquí.

