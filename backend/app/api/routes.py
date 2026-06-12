"""REST endpoints for controlling and inspecting the simulation."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.manager import manager
from app.models import SimulationConfigSchema, SpeedSchema, StatsHistorySchema, WorldStateSchema

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


@router.get("/state", response_model=WorldStateSchema)
def get_state() -> WorldStateSchema:
    return manager.get_state()


@router.get("/stats", response_model=StatsHistorySchema)
def get_stats() -> StatsHistorySchema:
    return manager.get_stats_history()


@router.post("/reset", response_model=WorldStateSchema)
async def reset_simulation(config: SimulationConfigSchema | None = None) -> WorldStateSchema:
    await manager.pause()
    return manager.reset(config)


@router.post("/step", response_model=WorldStateSchema)
def step_simulation() -> WorldStateSchema:
    return manager.step()


@router.post("/start")
async def start_simulation() -> dict[str, bool]:
    await manager.start()
    return {"running": manager.running}


@router.post("/pause")
async def pause_simulation() -> dict[str, bool]:
    await manager.pause()
    return {"running": manager.running}


@router.post("/speed", response_model=WorldStateSchema)
def set_speed(speed: SpeedSchema) -> WorldStateSchema:
    manager.set_tick_interval(speed.tick_interval_ms)
    return manager.get_state()
