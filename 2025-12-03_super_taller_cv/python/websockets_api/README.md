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
| REST | `/metrics/latest` | Últimas métricas agregadas (orden descendente). |
| REST | `/commands/recent` | Últimos comandos/fusiones registrados. |

## Flujo

1. Cada módulo se conecta al WS y envía mensajes con `module` y `type`.
2. El broker reemite a todos los clientes suscritos (pub/sub simple).
3. Métricas relevantes se guardan y se exponen al dashboard.

### Ejecución

```bash
uvicorn python.websockets_api.main:app --host 0.0.0.0 --port 8000 --reload
```

Los datos se almacenan en `results/backend/state.db` (SQLite). Asegúrate de que los módulos clientes envíen mensajes `type="metrics"` para que el dashboard los muestre.

