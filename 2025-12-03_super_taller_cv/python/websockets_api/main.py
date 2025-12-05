"""
Servidor FastAPI + WebSocket broker (versión preliminar).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketState
from pydantic import BaseModel
import uvicorn

from python.websockets_api.storage import Storage


class Message(BaseModel):
    timestamp: str
    module: str
    type: str
    payload: Dict[str, Any]


DB_PATH = Path("results/backend/state.db")
storage = Storage(DB_PATH)

app = FastAPI(title="Super Taller CV - WS Broker")
connections: List[WebSocket] = []


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "connections": len(connections)})


@app.get("/metrics/latest")
async def latest_metrics(limit: int = 50) -> Dict[str, Any]:
    rows = storage.latest_metrics(limit)
    return {"items": [row.model_dump() for row in rows]}


@app.get("/commands/recent")
async def recent_commands(limit: int = 20) -> Dict[str, Any]:
    rows = storage.recent_commands(limit)
    return {"items": [row.model_dump() for row in rows]}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            if "timestamp" not in data:
                data["timestamp"] = datetime.utcnow().isoformat()
            message = Message(**data)
            persist_message(message)
            await broadcast(message, origin=websocket)
    except WebSocketDisconnect:
        connections.remove(websocket)
    finally:
        if websocket.application_state != WebSocketState.DISCONNECTED:
            await websocket.close()


def persist_message(message: Message) -> None:
    if message.type == "metrics":
        numeric = {
            key: float(value)
            for key, value in message.payload.get("metrics", message.payload).items()
            if isinstance(value, (int, float))
        }
        storage.add_metrics(message.module, message.timestamp, numeric)
    elif message.type in {"command", "fusion_command"}:
        payload = message.payload
        action = payload.get("action", "unknown")
        source = payload.get("source")
        storage.add_command(
            module=message.module,
            timestamp=message.timestamp,
            action=action,
            source=source,
            payload=json.dumps(payload),
        )


async def broadcast(message: Message, origin: WebSocket | None = None) -> None:
    data = message.model_dump_json()
    for conn in list(connections):
        if conn is origin:
            continue
        try:
            await conn.send_text(data)
        except WebSocketDisconnect:
            connections.remove(conn)


def run() -> None:
    uvicorn.run("python.websockets_api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()

