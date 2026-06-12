"""Simulation manager: holds engine state, the background run loop, and
websocket broadcasting. This is the single bridge between the pure
simulation core and the FastAPI layer."""

from __future__ import annotations

import asyncio
from dataclasses import asdict

from fastapi import WebSocket

from app.config import DEFAULT_TICK_INTERVAL_MS, MAX_TICK_INTERVAL_MS, MIN_TICK_INTERVAL_MS
from app.models import (
    GenomeSchema,
    OrganismSchema,
    SimulationConfigSchema,
    StatsHistorySchema,
    StatsSnapshotSchema,
    TileSchema,
    WorldStateSchema,
)
from app.simulation.engine import SimulationConfig, SimulationEngine


class SimulationManager:
    def __init__(self) -> None:
        self.engine = SimulationEngine()
        self.running = False
        self.tick_interval_ms = DEFAULT_TICK_INTERVAL_MS
        self._task: asyncio.Task | None = None
        self._connections: set[WebSocket] = set()

    # --- lifecycle ---------------------------------------------------
    def reset(self, config: SimulationConfigSchema | None = None) -> WorldStateSchema:
        sim_config = None
        if config:
            sim_config = SimulationConfig(
                population_size=config.population_size,
                mutation_rate=config.mutation_rate,
                food_regen_multiplier=config.food_regen_multiplier,
            )
            self.set_tick_interval(config.tick_interval_ms)
        self.engine.reset(sim_config)
        return self.get_state()

    def step(self) -> WorldStateSchema:
        self.engine.step()
        return self.get_state()

    def set_tick_interval(self, tick_interval_ms: int) -> None:
        self.tick_interval_ms = max(MIN_TICK_INTERVAL_MS, min(MAX_TICK_INTERVAL_MS, tick_interval_ms))

    async def start(self) -> None:
        if self.running:
            return
        self.running = True
        self._task = asyncio.create_task(self._run_loop())

    async def pause(self) -> None:
        self.running = False
        if self._task:
            self._task.cancel()
            self._task = None

    async def _run_loop(self) -> None:
        try:
            while self.running:
                self.engine.step()
                await self._broadcast(self.get_state())
                await asyncio.sleep(self.tick_interval_ms / 1000)
        except asyncio.CancelledError:
            pass

    # --- websocket -----------------------------------------------------
    async def register(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)
        await websocket.send_json(self.get_state().model_dump())

    def unregister(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)

    async def _broadcast(self, state: WorldStateSchema) -> None:
        if not self._connections:
            return
        payload = state.model_dump()
        stale: list[WebSocket] = []
        for ws in self._connections:
            try:
                await ws.send_json(payload)
            except Exception:
                stale.append(ws)
        for ws in stale:
            self._connections.discard(ws)

    # --- serialization ---------------------------------------------------
    def get_state(self) -> WorldStateSchema:
        engine = self.engine
        tiles = [
            TileSchema(x=tile.x, y=tile.y, terrain=tile.terrain.value, food=round(tile.food, 2), max_food=tile.max_food)
            for row in engine.world.tiles
            for tile in row
        ]
        organisms = [
            OrganismSchema(
                id=o.id,
                x=o.x,
                y=o.y,
                energy=round(o.energy, 2),
                age=o.age,
                generation=o.generation,
                genome=GenomeSchema(**o.genome.to_dict()),
            )
            for o in engine.organisms
        ]
        stats = engine.stats_history[-1]
        return WorldStateSchema(
            tick=engine.tick,
            width=engine.world.width,
            height=engine.world.height,
            tiles=tiles,
            organisms=organisms,
            stats=StatsSnapshotSchema(**asdict(stats)),
            running=self.running,
            tick_interval_ms=self.tick_interval_ms,
        )

    def get_stats_history(self) -> StatsHistorySchema:
        return StatsHistorySchema(history=[StatsSnapshotSchema(**asdict(s)) for s in self.engine.stats_history])


manager = SimulationManager()
