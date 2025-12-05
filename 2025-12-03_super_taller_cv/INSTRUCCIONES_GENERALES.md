# Instrucciones Generales del Taller Super CV (2025-12-03)

## Contenido del repositorio

```
2025-12-03_super_taller_cv/
├── docs/                 # Documentación (arquitectura, métricas, evidencias, demo)
├── python/               # Módulos backend, visión, deep learning, multimodal
├── threejs/              # Frontend React Three Fiber + WebSocket
├── unity/                # Proyecto Unity (scripts + README)
├── data/                 # Datasets/modelos (ignorar en commits)
├── results/              # Resultados, métricas y media
└── INSTRUCCIONES_GENERALES.md   ← este archivo
```

### Módulos destacados

- **Detección (python/detection/)**  
  YOLOv8 + segmentación; `scripts/inference.py` publica detecciones (incluye FPS/latencia y tamaño de frame).  
  `scripts/mock_publisher.py` permite enviar detecciones simuladas para pruebas rápidas.

- **Deep Learning (python/training/)**  
  `train_scratch.py` (CNN desde cero) y `train_finetune.py` (ResNet18). Métricas en `results/training/.../metrics.json`.

- **Multimodal (python/mediapipe_voice/)**  
  Gestos (MediaPipe), voz (SpeechRecognition), EEG simulado y motor de fusión.  
  Configurable vía `configs/default.yaml`. Comandos de voz/gestos → acciones WS (`change_material`, `switch_camera`, `toggle_light`, etc.).

- **Backend / Dashboard**  
  `python/websockets_api/main.py`: FastAPI + WebSocket + persistencia SQLite (`results/backend/state.db`).  
  `python/dashboards/app.py` (Streamlit) muestra métricas (detección, comandos, entrenamiento).

- **Three.js (threejs/)**  
  React Three Fiber + Zustand. Escena (cubos, luces) reacciona a comandos y dibuja overlay de detecciones.  
  Scripts npm: `npm run dev`, `npm run build`, `npm run preview`, `npm run lint`.

- **Unity (unity/)**  
  Scripts en `Assets/Scripts/`: `WsCommandListener`, `IKRigController`, `FxController`. Escena responde a comandos WS con cambios de color, animaciones, cámara, luz, IK y FX. Requiere NativeWebSocket.

## Preparación de entornos

### Backend / Python
```powershell
cd 2025-12-03_super_taller_cv
python -m venv .venv
.venv\Scripts\activate
pip install -r python/requirements.txt
```

### Frontend (Three.js)
```powershell
cd threejs
npm install
```

### Unity
1. Unity 2022 LTS (URP o 3D Core).  
2. Instalar el paquete `https://github.com/endel/NativeWebSocket.git#4.0.3`.  
3. Copiar `unity/` dentro del proyecto y asignar los scripts a los GameObjects (ver README de Unity).

## Cómo ejecutar todo

1. **Servidor WebSocket + API**  
   ```powershell
   cd 2025-12-03_super_taller_cv
   set PYTHONPATH=%CD%
   python -m uvicorn python.websockets_api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Dashboard (Streamlit)**  
   En otra terminal:  
   ```powershell
   set PYTHONPATH=%CD%
   python -m streamlit run python/dashboards/app.py
   ```

3. **Escena Three.js**  
   ```powershell
   cd threejs
   npm run dev   # http://localhost:5173
   ```
   Si el WS corre en otro host/puerto:  
   ```js
   localStorage.setItem('threejs_ws_url', 'ws://127.0.0.1:8000/ws');
   location.reload();
   ```

4. **Proyecto Unity**  
   - Abre el proyecto en Unity, asigna referencias en `WsCommandListener`, `IKRigController`, `FxController`.  
   - Ajusta `websocketUrl` si usas otro puerto.  
   - Play para escuchar comandos en vivo.

5. **Pipelines Multimodales**  
   - Gestos: `python python/mediapipe_voice/gesture_pipeline.py --source 0 --ws-url ws://127.0.0.1:8000/ws --display`  
   - Voz (archivo o mic): `python python/mediapipe_voice/voice_pipeline.py --audio-file data/raw/sample_audios/change_color.wav --ws-url ws://127.0.0.1:8000/ws`  
   - EEG: `python python/mediapipe_voice/eeg_simulator.py --ws-url ws://127.0.0.1:8000/ws`  
   - Mock detecciones: `python python/detection/scripts/mock_publisher.py --ws-url ws://127.0.0.1:8000/ws`

6. **YOLO en vivo (opcional)**  
   ```powershell
   python python/detection/scripts/inference.py --config python/detection/configs/default.yaml --source 0 --ws-url ws://127.0.0.1:8000/ws --display
   ```

## ¿Qué se implementó?

- **Visión**: YOLOv8 + segmentación DeepLab (exporta JSON/frames, métricas).  
- **Deep Learning**: Entrenamiento base + fine-tuning (PyTorch).  
- **Multimodalidad**: Gestos (MediaPipe), voz (SpeechRecognition), EEG simulado y motor de fusión.  
- **Backend**: FastAPI + WebSocket + almacenamiento SQLite + dashboard Streamlit.  
- **Visualización web**: React Three Fiber con overlay de detecciones y respuesta a comandos.  
- **Unity**: Cliente WS con IK, FX, control de cámara, luz y animaciones.  
- **Simuladores**: mock de detecciones, audios, etc., para pruebas sin hardware.  
- **Documentación**: Arquitectura, métricas, evidencias, rutinas de demo (en `docs/`).

## Flujo recomendado para la demo

1. Iniciar backend (`uvicorn`), dashboard y escena Three.js.  
2. Ejecutar pipeline de detección o mock para llenar los overlays.  
3. Lanzar gestos/voz/EEG (ver scripts) → deben cambiar materiales, luces, cámaras y disparar FX.  
4. En paralelo, tener la escena Unity escuchando el mismo WS para mostrar IK/FX.  
5. Registrar métricas en el dashboard, capturar video (30–60 s) y al menos 6 GIFs (`docs/EVIDENCIAS.md`).  
6. Actualizar `docs/METRICAS.md` con los resultados finales (FPS, latencia, precisión, etc.).

Con estos pasos tienes todo lo necesario para reproducir la solución end-to-end y preparar la entrega final. ¡Éxitos con la demo! 🎯

