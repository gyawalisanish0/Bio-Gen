"""Grid-based world: terrain layout, food distribution, and food regrowth."""

from __future__ import annotations

import random
from dataclasses import dataclass

from app.config import TERRAIN_PROPERTIES, Terrain, WORLD_HEIGHT, WORLD_WIDTH


@dataclass
class Tile:
    x: int
    y: int
    terrain: Terrain
    food: float = 0.0

    @property
    def max_food(self) -> float:
        return TERRAIN_PROPERTIES[self.terrain]["max_food"]

    @property
    def climate_cost(self) -> float:
        return TERRAIN_PROPERTIES[self.terrain]["climate_cost"]

    @property
    def passable(self) -> bool:
        return TERRAIN_PROPERTIES[self.terrain]["passable"]


class World:
    """A rectangular grid of tiles with terrain-driven food dynamics."""

    def __init__(self, width: int = WORLD_WIDTH, height: int = WORLD_HEIGHT, food_regen_multiplier: float = 1.0):
        self.width = width
        self.height = height
        self.food_regen_multiplier = food_regen_multiplier
        self.tiles: list[list[Tile]] = self._generate_tiles()

    def _generate_tiles(self) -> list[list[Tile]]:
        tiles: list[list[Tile]] = []
        for y in range(self.height):
            row: list[Tile] = []
            for x in range(self.width):
                terrain = self._terrain_for(x, y)
                tile = Tile(x=x, y=y, terrain=terrain)
                tile.food = tile.max_food * random.uniform(0.3, 1.0)
                row.append(tile)
            tiles.append(row)
        return tiles

    def _terrain_for(self, x: int, y: int) -> Terrain:
        """Lay out a small fixed biome: two ponds, a desert band along the
        bottom edge, scattered forest, and plains everywhere else."""
        if (x - 3) ** 2 + (y - 12) ** 2 <= 4:
            return Terrain.WATER
        if (x - 12) ** 2 + (y - 4) ** 2 <= 3:
            return Terrain.WATER
        if y >= self.height - 3:
            return Terrain.DESERT
        if (x + y) % 5 == 0:
            return Terrain.FOREST
        return Terrain.PLAINS

    def get(self, x: int, y: int) -> Tile:
        return self.tiles[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def passable_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """The (up to 8) surrounding tiles that an organism could move onto."""
        candidates: list[tuple[int, int]] = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.in_bounds(nx, ny) and self.get(nx, ny).passable:
                    candidates.append((nx, ny))
        return candidates

    def best_food_tile_in_range(self, x: int, y: int, vision: float) -> tuple[int, int] | None:
        """The passable tile with the most food within a square of the given
        vision radius, or ``None`` if no nearby tile has food."""
        best: tuple[int, int] | None = None
        best_food = 0.0
        r = int(round(vision))
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if not self.in_bounds(nx, ny):
                    continue
                tile = self.get(nx, ny)
                if not tile.passable:
                    continue
                if tile.food > best_food:
                    best_food = tile.food
                    best = (nx, ny)
        return best

    def step(self) -> None:
        """Regrow food on every tile up to its terrain-specific cap."""
        for row in self.tiles:
            for tile in row:
                regen = TERRAIN_PROPERTIES[tile.terrain]["food_regen_rate"] * self.food_regen_multiplier
                if regen > 0:
                    tile.food = min(tile.max_food, tile.food + regen)
