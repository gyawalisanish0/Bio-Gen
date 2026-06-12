"""Pydantic schemas exposed by the simulation API."""

from __future__ import annotations

from pydantic import BaseModel

from app.config import (
    DEFAULT_FOOD_REGEN_MULTIPLIER,
    DEFAULT_MUTATION_RATE,
    DEFAULT_POPULATION_SIZE,
    DEFAULT_TICK_INTERVAL_MS,
)


class GenomeSchema(BaseModel):
    size: float
    speed: float
    vision: float
    metabolism: float
    fertility: float


class OrganismSchema(BaseModel):
    id: int
    x: int
    y: int
    energy: float
    age: int
    generation: int
    species_id: int
    genome: GenomeSchema


class TileSchema(BaseModel):
    x: int
    y: int
    terrain: str
    food: float
    max_food: float


class SpeciesSchema(BaseModel):
    id: int
    shape: str
    hue: int


class StatsSnapshotSchema(BaseModel):
    tick: int
    population: int
    avg_size: float
    avg_speed: float
    avg_vision: float
    avg_metabolism: float
    avg_fertility: float
    max_generation: int


class WorldStateSchema(BaseModel):
    tick: int
    width: int
    height: int
    tiles: list[TileSchema]
    organisms: list[OrganismSchema]
    species: list[SpeciesSchema]
    stats: StatsSnapshotSchema
    running: bool
    tick_interval_ms: int


class SimulationConfigSchema(BaseModel):
    population_size: int = DEFAULT_POPULATION_SIZE
    mutation_rate: float = DEFAULT_MUTATION_RATE
    food_regen_multiplier: float = DEFAULT_FOOD_REGEN_MULTIPLIER
    tick_interval_ms: int = DEFAULT_TICK_INTERVAL_MS


class SpeedSchema(BaseModel):
    tick_interval_ms: int


class StatsHistorySchema(BaseModel):
    history: list[StatsSnapshotSchema]
