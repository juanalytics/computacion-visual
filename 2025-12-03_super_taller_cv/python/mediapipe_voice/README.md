# Módulo de interacción multimodal (gestos, voz, EEG)

## Objetivos

- Detectar gestos (manos/rostro/cuerpo) con MediaPipe.
- Reconocer comandos de voz y sintetizar respuestas auditivas.
- Simular señales EEG y generar eventos según umbrales configurables.
- Fusionar entradas multimodales y emitir comandos al broker WebSocket.

## Backlog inicial

1. `gesture_pipeline.py`: detección de gestos + normalización (mano derecha, posturas) ✅.
2. `voice_pipeline.py`: SpeechRecognition + PyAudio + pyttsx3 para feedback (voz → comandos) ✅.
3. `eeg_simulator.py`: generador de señales y lógica de umbrales ✅.
4. `fusion_engine.py`: combina señales, resuelve conflictos y emite comandos JSON ✅.
5. `configs/default.yaml`: parametrización central de acciones/umbrales ✅.

## Integración con otros módulos

- Envía eventos (`command`, `confidence`, `source`) a `python/websockets_api`.
- Recibe confirmaciones del dashboard para mostrar feedback por voz.
- Dispara efectos en `threejs/` y `unity/` según las reglas definidas.

## Métricas

- Latencia promedio por pipeline (<150 ms objetivo).
- Precisión detección de gestos (evaluación manual/automática).
- Tasa de error de reconocimiento de voz (WER aproximado).
- Estabilidad de umbrales EEG (falsos positivos/negativos).

Documenta pruebas y configuraciones en `docs/METRICAS.md` y en `results/multimodal/`.

## Uso rápido

Detectar gestos desde webcam/video:

```bash
python python/mediapipe_voice/gesture_pipeline.py --source 0 --display
```

Reconocimiento de voz (archivo de audio):

```bash
python python/mediapipe_voice/voice_pipeline.py --audio-file samples/command.wav
```

Simulador EEG:

```bash
python python/mediapipe_voice/eeg_simulator.py --interval 0.5
```

Fusionar eventos pregrabados:

```bash
python python/mediapipe_voice/fusion_engine.py \
  --events python/mediapipe_voice/examples/sample_events.json
```

