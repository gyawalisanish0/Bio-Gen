"""FastAPI application entrypoint for the EvoSim backend."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes, websocket

app = FastAPI(title="EvoSim API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
app.include_router(websocket.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
