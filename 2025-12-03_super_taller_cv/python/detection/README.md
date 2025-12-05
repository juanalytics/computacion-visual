# Módulo de detección y segmentación

## Objetivos

- Detección en tiempo real con YOLOv8 (ultralytics).
- Segmentación con SAM o DeepLab para máscaras precisas.
- Exportar resultados como imágenes anotadas y JSON normalizados.
- Publicar métricas (FPS, latencia, uso GPU) vía WebSocket.

## Backlog inicial

1. `setup_env.ipynb` o script `install.py` con dependencias específicas (CUDA opcional).
2. `scripts/inference.py`: pipeline tiempo real (webcam/video) + publicación WS (implementado).
3. `scripts/batch_export.py`: procesa datasets y genera anotaciones+JSON en `results/` (implementado).
4. `scripts/segment.py`: segmentación semántica con DeepLab (implementado, extensible a otros modelos).
5. `scripts/mock_publisher.py`: envía detecciones simuladas al WS para pruebas de la escena 3D (implementado).
6. Pruebas unitarias básicas (verificación de formatos JSON, validación de FPS mínimos).

## Estructura esperada

```
detection/
├── README.md
├── configs/
├── notebooks/
├── scripts/
│   ├── inference.py
│   ├── batch_export.py
│   └── segment.py
└── tests/
```

## Métricas clave

- mAP@50, mAP@50-95
- FPS promedio (GPU/CPU)
- Latencia end-to-end (captura → WS emitido)

Registra resultados en `docs/METRICAS.md` y publica artefactos en `results/detection/`.

## Uso rápido (`scripts/inference.py`)

```bash
python python/detection/scripts/inference.py \
  --config python/detection/configs/default.yaml \
  --model yolov8n.pt \
  --source 0 \
  --ws-url ws://localhost:8000/ws
```

Parámetros relevantes:

- `--source`: ruta a video o índice de webcam.
- `--display`: muestra ventana con anotaciones.
- `--save-dir`: guarda frames anotados (por defecto `results/detection/runs`).
- `--no-emit`: desactiva el envío por WebSocket.
- `--confidence`, `--iou`, `--max-det`: hiperparámetros de predicción.

El mensaje emitido cumple el contrato descrito en `python/websockets_api/SCHEMA.md`.

## Uso rápido (`scripts/batch_export.py`)

```bash
python python/detection/scripts/batch_export.py \
  --input data/raw/sample_images \
  --config python/detection/configs/default.yaml \
  --annotate-dir results/detection/batch/annotated
```

Parámetros clave:

- `--input`: carpeta o archivo individual (imagen o video).
- `--output-dir`: carpeta donde se guardará el JSON (`results/detection/batch` por defecto).
- `--annotate-dir`: carpeta para almacenar imágenes anotadas.
- `--limit`: útil para pruebas rápidas (procesa solo N archivos).

## Uso rápido (`scripts/segment.py`)

```bash
python python/detection/scripts/segment.py \
  --input data/raw/sample_images \
  --config python/detection/configs/default.yaml \
  --model deeplabv3_resnet50
```

Parámetros clave:

- `--input`: imagen o carpeta con imágenes.
- `--output-dir`: carpeta donde se guardarán las máscaras (`results/detection/segment/masks` por defecto).
- `--overlay-dir`: carpeta para overlays fusionados (`results/detection/segment/overlays` si está definido en el config).
- `--model`: `deeplabv3_resnet50` o `deeplabv3_resnet101` (se puede extender a SAM/otros).
- `--limit`: procesa solo N archivos para pruebas.

## Pruebas
### Simulador de detecciones (`scripts/mock_publisher.py`)

Permite probar el overlay en Three.js sin correr YOLO:

```bash
python python/detection/scripts/mock_publisher.py --ws-url ws://127.0.0.1:8000/ws
```

Opciones útiles:

- `--width/--height`: resolución del frame simulado.
- `--interval`: tiempo entre mensajes (s).

Ejecuta los tests de utilidades con:

```bash
pytest python/detection/tests
```

Amplía esta batería a medida que se agreguen más scripts (batch, segmentación, etc.).

