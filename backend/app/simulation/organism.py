"""Organism: position, genome-derived traits, energy, aging, and behaviour."""

from __future__ import annotations

import itertools
import random

from app.config import (
    BASE_MAX_AGE,
    BASE_METABOLIC_COST,
    BASE_REPRODUCTION_THRESHOLD,
    CHILD_STARTING_ENERGY_FRACTION,
    EAT_RATE,
    MAX_AGE_SIZE_FACTOR,
    MOVE_COST_PER_STEP,
    REPRODUCTION_COST_FRACTION,
    STARTING_ENERGY,
)
from app.simulation.genome import Genome
from app.simulation.world import World

_id_counter = itertools.count(1)


class Organism:
    """A single creature living on the grid, driven entirely by its genome."""

    def __init__(self, x: int, y: int, genome: Genome, energy: float = STARTING_ENERGY, generation: int = 0):
        self.id = next(_id_counter)
        self.x = x
        self.y = y
        self.genome = genome
        self.energy = energy
        self.age = 0
        self.generation = generation
        self.alive = True

    @property
    def max_age(self) -> int:
        """Larger organisms live proportionally longer."""
        return int(BASE_MAX_AGE * (1 + MAX_AGE_SIZE_FACTOR * (self.genome.size - 1)))

    @property
    def reproduction_threshold(self) -> float:
        """Higher fertility lowers the energy bar needed to reproduce."""
        return BASE_REPRODUCTION_THRESHOLD / self.genome.fertility

    def act(self, world: World) -> None:
        """Move, forage, pay energy costs, age, and check for death."""
        steps = max(1, round(self.genome.speed))
        moved_steps = self._move(world, steps)

        tile = world.get(self.x, self.y)
        metabolic_cost = BASE_METABOLIC_COST * self.genome.size * self.genome.metabolism
        movement_cost = moved_steps * MOVE_COST_PER_STEP * self.genome.size
        self.energy -= metabolic_cost + movement_cost + tile.climate_cost

        if tile.food > 0:
            eaten = min(tile.food, EAT_RATE * self.genome.size)
            tile.food -= eaten
            self.energy += eaten

        self.age += 1
        if self.energy <= 0 or self.age >= self.max_age:
            self.alive = False

    def _move(self, world: World, steps: int) -> int:
        """Move toward the best visible food tile, or wander randomly."""
        moved = 0
        for _ in range(steps):
            target = world.best_food_tile_in_range(self.x, self.y, self.genome.vision)
            neighbors = world.passable_neighbors(self.x, self.y)
            if not neighbors:
                break
            if target:
                neighbors.sort(key=lambda pos: _distance(pos, target))
                next_pos = neighbors[0]
            else:
                next_pos = random.choice(neighbors)
            self.x, self.y = next_pos
            moved += 1
            if target and (self.x, self.y) == target:
                break
        return moved

    def can_reproduce(self) -> bool:
        return self.alive and self.energy >= self.reproduction_threshold

    def reproduce(self, mutation_rate: float) -> "Organism":
        """Spend energy to create a mutated offspring at the same tile."""
        cost = self.reproduction_threshold * REPRODUCTION_COST_FRACTION
        child_energy = self.reproduction_threshold * CHILD_STARTING_ENERGY_FRACTION
        self.energy -= cost
        child_genome = self.genome.mutate(mutation_rate)
        return Organism(self.x, self.y, child_genome, energy=child_energy, generation=self.generation + 1)


def _distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
