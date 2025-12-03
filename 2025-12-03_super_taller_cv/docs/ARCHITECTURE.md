# Arquitectura técnica

## 1. Vista general

```
Webcam / Mic / EEG sim
        │
        ▼
python/detection (YOLO + SAM) ─┐
python/mediapipe_voice (gestos/voz/EEG) ─┤
python/training (CNN & FT) ──────────────┤
                                        ▼
python/websockets_api (FastAPI + WS broker) ───►
        ├── python/dashboards (metrics UI)
        ├── threejs/ (React Three Fiber scene + AR.js)
        └── unity/ (FK/IK, partículas, cinemática)
```

Los subsistemas funcionan de forma autónoma pero comparten eventos mediante WebSockets y almacenamiento ligero (CSV/SQLite).

## 2. Componentes clave

| Componente | Responsabilidad | Entradas | Salidas |
| --- | --- | --- | --- |
| `detection` | YOLO en tiempo real + segmentación SAM/DeepLab | Stream cámara, modelos | `detections.json`, frames anotados, métricas |
| `training` | CNN scratch + fine-tuning | `data/processed`, config experimento | Pesos (`.pt`/`.pth`), métricas, gráficas |
| `mediapipe_voice` | Gestos, reconocimiento/síntesis voz, EEG simulado | Cámara, micro, generador EEG | Eventos multimodales, comandos |
| `websockets_api` | Broker WS + REST ligeras | Eventos de módulos | Mensajes WS, persistencia en CSV/SQLite |
| `dashboards` | Visualización de métricas | CSV/SQLite, WS | UI en navegador |
| `threejs` | Visualización 3D Web/AR | Comandos WS, assets | Escena reactiva, overlays |
| `unity` | Motion design, IK/FK, partículas | Comandos WS, assets 3D | Animaciones y efectos sincronizados |

## 3. Contratos de datos

- **Mensajes WebSocket**: JSON con campos obligatorios `timestamp`, `module`, `type`, `payload`.
- **Métricas**: CSV + SQLite con esquema `timestamp,module,metric,value`.
- **Resultados AI**: carpetas `results/<fecha>/<modulo>/` con `metrics.json`, `preview.png`, `notes.md`.

El detalle del contrato se documentará en `python/websockets_api/SCHEMA.md` (pendiente).

## 4. Integraciones previstas

| Origen | Destino | Evento | Acción |
| --- | --- | --- | --- |
| `mediapipe_voice` | `threejs` | `command:change_material` | Modificar materiales/luces |
| `mediapipe_voice` | `unity` | `command:trigger_animation` | Activar animación IK/FK |
| `detection` | `dashboards` | `metrics:update` | Graficar FPS, uso GPU |
| `detection` | `threejs` | `detections` | Mostrar bounding boxes en overlay |
| `training` | `dashboards` | `metrics:model_eval` | Comparar CNN vs FT |
| `dashboards` | `web_shared` | `snapshot` | Publicar métricas resumidas |

## 5. Persistencia y resultados

- **Datos**: se almacenan localmente; si se usan datasets grandes, documentar enlaces y scripts.
- **Modelos**: versionar mediante etiquetas `model_<modulo>_<fecha>.pth`.
- **Métricas**: dashboard consume `metrics.db` (SQLite). Scripts en `python/utils/metrics_export.py` (pendiente) generarán CSV y gráficas.

## 6. Seguridad y performance

- Aislar dependencias mediante entornos dedicados.
- Limitar ancho de banda WS usando compresión opcional y envío de máscaras por referencia (URL) en vez de base64.
- Reportar FPS, latencia y consumo de recursos en `docs/METRICAS.md`.

Mantén este documento actualizado cuando cambien topologías, contratos o herramientas.

