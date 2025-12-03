"""
Servidor FastAPI + WebSocket broker (versión preliminar).
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketState
from pydantic import BaseModel
import uvicorn


class Message(BaseModel):
    timestamp: str
    module: str
    type: str
    payload: Dict[str, Any]


app = FastAPI(title="Super Taller CV - WS Broker")
connections: List[WebSocket] = []


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "connections": len(connections)})


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
            await broadcast(message, origin=websocket)
    except WebSocketDisconnect:
        connections.remove(websocket)
    finally:
        if websocket.application_state != WebSocketState.DISCONNECTED:
            await websocket.close()


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

