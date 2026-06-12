"""WebSocket endpoint that streams live simulation state to connected clients."""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.manager import manager

router = APIRouter()


@router.websocket("/ws/simulation")
async def simulation_socket(websocket: WebSocket) -> None:
    await manager.register(websocket)
    try:
        while True:
            # Connection is server-push only; block here until the client
            # disconnects (or sends anything, which we ignore).
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.unregister(websocket)
