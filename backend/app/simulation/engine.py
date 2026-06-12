"""Simulation engine: orchestrates the world, population, ticks, and stats."""

from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass

from app.config import (
    DEFAULT_FOOD_REGEN_MULTIPLIER,
    DEFAULT_MUTATION_RATE,
    DEFAULT_POPULATION_SIZE,
    STATS_HISTORY_LIMIT,
    WORLD_HEIGHT,
    WORLD_WIDTH,
)
from app.simulation.genome import Genome
from app.simulation.organism import Organism
from app.simulation.world import World


@dataclass
class SimulationConfig:
    population_size: int = DEFAULT_POPULATION_SIZE
    mutation_rate: float = DEFAULT_MUTATION_RATE
    food_regen_multiplier: float = DEFAULT_FOOD_REGEN_MULTIPLIER


@dataclass
class StatsSnapshot:
    tick: int
    population: int
    avg_size: float
    avg_speed: float
    avg_vision: float
    avg_metabolism: float
    avg_fertility: float
    max_generation: int


class SimulationEngine:
    """Owns the world and population, and advances them one tick at a time."""

    def __init__(self, config: SimulationConfig | None = None):
        self.config = config or SimulationConfig()
        self.tick = 0
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT, self.config.food_regen_multiplier)
        self.organisms: list[Organism] = []
        self.stats_history: list[StatsSnapshot] = []
        self._spawn_initial_population()
        self._record_stats()

    def reset(self, config: SimulationConfig | None = None) -> None:
        self.config = config or self.config
        self.tick = 0
        self.world = World(WORLD_WIDTH, WORLD_HEIGHT, self.config.food_regen_multiplier)
        self.organisms = []
        self.stats_history = []
        self._spawn_initial_population()
        self._record_stats()

    def _spawn_initial_population(self) -> None:
        for _ in range(self.config.population_size):
            x, y = self._random_passable_tile()
            self.organisms.append(Organism(x, y, Genome.random()))

    def _random_passable_tile(self) -> tuple[int, int]:
        while True:
            x = random.randrange(self.world.width)
            y = random.randrange(self.world.height)
            if self.world.get(x, y).passable:
                return x, y

    def step(self) -> None:
        self.tick += 1
        self.world.step()

        for organism in self.organisms:
            organism.act(self.world)

        children = [o.reproduce(self.config.mutation_rate) for o in self.organisms if o.can_reproduce()]

        self.organisms = [o for o in self.organisms if o.alive] + children

        if not self.organisms:
            self._spawn_initial_population()

        self._record_stats()

    def _record_stats(self) -> None:
        n = len(self.organisms)
        if n == 0:
            snapshot = StatsSnapshot(self.tick, 0, 0, 0, 0, 0, 0, 0)
        else:
            snapshot = StatsSnapshot(
                tick=self.tick,
                population=n,
                avg_size=_avg(o.genome.size for o in self.organisms),
                avg_speed=_avg(o.genome.speed for o in self.organisms),
                avg_vision=_avg(o.genome.vision for o in self.organisms),
                avg_metabolism=_avg(o.genome.metabolism for o in self.organisms),
                avg_fertility=_avg(o.genome.fertility for o in self.organisms),
                max_generation=max(o.generation for o in self.organisms),
            )
        self.stats_history.append(snapshot)
        if len(self.stats_history) > STATS_HISTORY_LIMIT:
            self.stats_history = self.stats_history[-STATS_HISTORY_LIMIT:]


def _avg(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values)
