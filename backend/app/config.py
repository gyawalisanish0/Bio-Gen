"""Central configuration and tunable constants for the evolution simulation.

Keeping every tunable number here means the simulation core, API layer, and
tests never hardcode magic numbers, and balancing the simulation only ever
requires editing this one file.
"""

from enum import Enum


class Terrain(str, Enum):
    PLAINS = "plains"
    FOREST = "forest"
    DESERT = "desert"
    WATER = "water"


# World grid dimensions
WORLD_WIDTH = 16
WORLD_HEIGHT = 16

# Terrain properties: food regrowth rate, food cap, extra metabolic cost,
# and whether organisms can occupy/move through the tile.
TERRAIN_PROPERTIES = {
    Terrain.PLAINS: {"food_regen_rate": 0.15, "max_food": 10.0, "climate_cost": 0.0, "passable": True},
    Terrain.FOREST: {"food_regen_rate": 0.25, "max_food": 14.0, "climate_cost": 0.1, "passable": True},
    Terrain.DESERT: {"food_regen_rate": 0.04, "max_food": 4.0, "climate_cost": 0.4, "passable": True},
    Terrain.WATER: {"food_regen_rate": 0.0, "max_food": 0.0, "climate_cost": 0.0, "passable": False},
}

# Genome trait bounds: trait -> (min, max, mutation sigma)
TRAIT_BOUNDS: dict[str, tuple[float, float, float]] = {
    "size": (0.5, 2.0, 0.08),
    "speed": (0.5, 2.5, 0.08),
    "vision": (1.0, 5.0, 0.3),
    "metabolism": (0.5, 2.0, 0.08),
    "fertility": (0.5, 2.0, 0.08),
}

# Organism energy dynamics
# Kept below the lowest possible reproduction threshold (BASE_REPRODUCTION_THRESHOLD
# / max fertility) so newly spawned organisms must forage before reproducing.
STARTING_ENERGY = 8.0
BASE_METABOLIC_COST = 0.4
MOVE_COST_PER_STEP = 0.15
EAT_RATE = 2.0
BASE_REPRODUCTION_THRESHOLD = 20.0
REPRODUCTION_COST_FRACTION = 0.5
CHILD_STARTING_ENERGY_FRACTION = 0.5
BASE_MAX_AGE = 120
MAX_AGE_SIZE_FACTOR = 0.3

# Simulation defaults
DEFAULT_POPULATION_SIZE = 24
DEFAULT_MUTATION_RATE = 0.15
DEFAULT_FOOD_REGEN_MULTIPLIER = 1.0
DEFAULT_TICK_INTERVAL_MS = 200
STATS_HISTORY_LIMIT = 500
