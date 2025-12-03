# Broker WebSocket y API ligera

## Objetivos

- Centralizar la comunicación entre subsistemas mediante WebSockets y REST.
- Serializar eventos siguiendo un esquema común (`SCHEMA.md`).
- Almacenar métricas/eventos en CSV o SQLite para el dashboard.

## Backlog inicial

1. `SCHEMA.md`: definición formal de tipos de mensaje.
2. `main.py`: servidor FastAPI + WebSocket (uvicorn) con canales `detections`, `commands`, `metrics`.
3. `storage.py`: capa de persistencia (SQLite + SQLModel o pandas CSV).
4. `tests/` para validar payloads contra el esquema.
5. Scripts de ejemplo (`clients/threejs_client.py`, `clients/unity_client.cs` snippet) para facilitar integración.

## Endpoints previstos

| Tipo | Ruta | Descripción |
| --- | --- | --- |
| WS | `/ws` | Canal multipropósito (diferenciar por `type` en payload). |
| REST | `/health` | Estado del servidor. |
| REST | `/metrics/latest` | Últimas métricas agregadas. |

## Flujo

1. Cada módulo se conecta al WS y envía mensajes con `module` y `type`.
2. El broker reemite a todos los clientes suscritos (pub/sub simple).
3. Métricas relevantes se guardan y se exponen al dashboard.

Desarrolla este servicio temprano para habilitar integraciones paralelas.

