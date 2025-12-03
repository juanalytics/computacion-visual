# Paquete Python

Contiene todos los módulos de backend, visión, entrenamiento y utilidades.

## Submódulos

| Carpeta | Descripción |
| --- | --- |
| `detection/` | Detección/segmentación en tiempo real. |
| `training/` | CNN scratch + fine-tuning. |
| `mediapipe_voice/` | Gestos, voz y EEG simulado. |
| `websockets_api/` | Servidor FastAPI + WS broker. |
| `dashboards/` | Dashboards en Python. |
| `utils/` | Scripts compartidos (datos, métricas, media). |

## Dependencias

Administradas vía `requirements.txt`. Usa un entorno virtual:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r python/requirements.txt
```

## Convenciones

- Código formateado con `ruff`/`black` (pendiente de añadir al repo).
- Docstrings y comentarios en español o inglés consistente.
- Scripts CLI con `argparse` y mensajes claros.

Mantén este README actualizado a medida que evolucionan los módulos.

