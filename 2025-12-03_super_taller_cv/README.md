# Super Taller de Computación Visual Avanzada

Repositorio maestro para coordinar el desarrollo del taller integral que combina visión por computador, aprendizaje profundo, interacción multimodal y visualización 3D/AR.

## Objetivos

- Entregar un sistema compuesto por subsistemas especializados totalmente funcionales.
- Cubrir el 100 % de la rúbrica: detección/segmentación, interacción multimodal, entrenamiento de CNN, visualización 3D/AR, dashboards y evidencias.
- Mantener integraciones ligeras mediante WebSockets y contratos JSON estandarizados.

## Roadmap resumido

| Semana | Enfoque principal | Entregables clave |
| --- | --- | --- |
| 0 | Setup y contratos | Estructura repo, entornos, esquema WebSocket |
| 1 | Percepción + baseline DL | YOLO + SAM/DeepLab, CNN desde cero, métricas iniciales |
| 2 | Fine-tuning + multimodalidad | ResNet/MobileNet FT, MediaPipe gestos, voz, EEG simulado |
| 3 | Backend + dashboards | WebSocket server, almacenamiento, dashboard métricas |
| 4 | Visualización 3D + Unity | Three.js/AR.js, Unity FK/IK, optimización visual |
| 5 | Integración ligera + evidencias | Demo coordinada, video 30–60 s, 6+ GIFs, docs finales |

## Estructura principal

```
2025-12-03_super_taller_cv/
├── README.md
├── unity/
├── threejs/
├── python/
│   ├── detection/
│   ├── training/
│   ├── mediapipe_voice/
│   ├── websockets_api/
│   ├── dashboards/
│   └── utils/
├── data/
├── web_shared/
├── results/
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── EVIDENCIAS.md
│   ├── METRICAS.md
│   ├── PROMPTS.md
│   └── RUTINAS_DEMO.md
└── .github/
```

## Entornos y dependencias mínimas

- **Python 3.11 + Conda/venv**: PyTorch, Ultralytics YOLO, OpenCV, MediaPipe, FastAPI, websockets, pandas, scikit-learn, SpeechRecognition, PyAudio, pyttsx3.
- **Node 18+**: Vite + React + Three.js, React Three Fiber, Zustand, Socket.IO client, AR.js (via script) o 8thWall según alcance.
- **Unity 2022 LTS**: URP, Input System, Cinemachine, Visual Effect Graph (opcional).
- **Herramientas comunes**: Git LFS (para modelos), ffmpeg (generar video/GIF), OBS (capturas).

Documenta la instalación específica en `docs/README.md` a medida que se estabilicen los entornos.

## Contrato WebSocket (borrador)

```json
{
  "timestamp": 0,
  "module": "detection|multimodal|dashboard|visualization",
  "payload": {
    "detections": [
      {"id": 0, "label": "person", "bbox": [x1, y1, x2, y2], "confidence": 0.95}
    ],
    "segmentation_mask": "s3://.../mask.png",
    "command": "change_material",
    "params": {"color": "#33ffaa"},
    "metrics": {"fps": 42.1, "gpu": 76.2, "latency_ms": 48}
  }
}
```

El contrato definitivo vivirá en `python/websockets_api/SCHEMA.md` y deberá versionarse con cambios controlados.

## Buenas prácticas

- Commits y PR en inglés, mensajes descriptivos (`feat: add mediapipe hand fusion pipeline`).
- Documentar cada módulo en su carpeta con README y scripts reproducibles.
- Guardar datasets/modelos en `data/` (usar LFS cuando superen 100 MB).
- Consolidar métricas y evidencias gráficas en `results/` con subcarpetas fechadas.
- Mantener `docs/` sincronizado con el progreso real (diagrama arquitectura, métricas actualizadas, rutinas demo listas).

## Próximos pasos inmediatos

1. Completar documentos base en `docs/`.
2. Crear plantillas de scripts iniciales (setup entornos, preparación de datos).
3. Abrir issues/milestones por subsistema siguiendo el roadmap.

Con esto queda trazado el plan para cumplir la rúbrica al 100 %. Continúa en `docs/` para el detalle operativo.

