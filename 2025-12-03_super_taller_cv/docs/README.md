# Documentación general del taller

Este documento centraliza la información operativa del proyecto y enlaza a los documentos específicos dentro de `docs/`.

## 1. Objetivos específicos

- Integrar los módulos de percepción, deep learning, multimodalidad, visualización y backend.
- Reproducir cada subsistema de forma independiente y demostrar integración ligera.
- Registrar métricas, evidencias y procedimientos de demo para auditoría completa.

## 2. Guía rápida de entornos

| Área | Herramientas | Setup inicial |
| --- | --- | --- |
| Visión / DL | Python 3.11, Conda/venv, PyTorch, Ultralytics, SAM/DeepLab | `python -m venv .venv && pip install -r requirements.txt` |
| Multimodal | MediaPipe, SpeechRecognition, PyAudio, pyttsx3 | Requiere drivers de audio + micro configurado |
| Backend | FastAPI, websockets, Redis opcional | `.venv` compartido, archivo `.env` con puertos |
| Three.js / Web | Node 18+, Vite/React, R3F, Socket.IO client | `npm install && npm run dev` |
| Unity | Unity 2022 LTS (URP) | Abrir carpeta `unity/` con Unity Hub |

Documenta dependencias extra (CUDA, cuDNN, SDKs) en esta sección conforme se agreguen.

## 3. Gestión de datos y modelos

- `data/raw/`: datasets originales (usar Git LFS si >100 MB).
- `data/processed/`: datos listos para entrenamiento.
- `data/models/`: pesos entrenados, versiones etiquetadas `vX_Y`.
- `python/utils/prepare_data.py`: script maestro para descargar y preparar datos (pendiente).

## 4. Organización de módulos

| Carpeta | Responsable | Descripción |
| --- | --- | --- |
| `python/detection/` | Visión | YOLO + segmentación, exportes JSON |
| `python/training/` | Deep Learning | CNN scratch, fine-tuning, experiment tracking |
| `python/mediapipe_voice/` | Multimodalidad | Gestos, voz, EEG simulado, fusión |
| `python/websockets_api/` | Backend | API/WebSocket + contratos |
| `python/dashboards/` | Observabilidad | Dashboards Python (Streamlit, Dash o Panel) |
| `threejs/` | Web 3D | Escena R3F + AR.js, escucha eventos |
| `unity/` | Motion design | Cinemática, partículas, socket client |
| `results/` | PM/QA | Métricas, capturas, videos, GIFs |

Actualiza la tabla cuando se reasignen responsables.

## 5. Roadmap detallado

Consulta `docs/ARCHITECTURE.md` para el flujo técnico y `docs/RUTINAS_DEMO.md` para la narrativa de la demo. El roadmap semanal vive en la raíz del repo (`README.md`) y se sincroniza con issues/milestones.

## 6. Control de calidad

- Checklist de rúbrica en `docs/RUTINAS_DEMO.md`.
- Resultados cuantitativos en `docs/METRICAS.md`.
- Evidencias visuales en `docs/EVIDENCIAS.md`.
- Cambios de prompts o generación asistida documentados en `docs/PROMPTS.md`.

Mantén este documento como índice actualizado para facilitar on-boarding y seguimiento.

