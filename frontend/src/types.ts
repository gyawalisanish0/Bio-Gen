import type { ShapeName } from "./shapes";

export type Terrain = "plains" | "forest" | "desert" | "water";

export interface Genome {
  size: number;
  speed: number;
  vision: number;
  metabolism: number;
  fertility: number;
}

export interface Organism {
  id: number;
  x: number;
  y: number;
  energy: number;
  age: number;
  generation: number;
  species_id: number;
  genome: Genome;
}

export interface Species {
  id: number;
  shape: ShapeName;
  hue: number;
}

export interface Tile {
  x: number;
  y: number;
  terrain: Terrain;
  food: number;
  max_food: number;
}

export interface StatsSnapshot {
  tick: number;
  population: number;
  avg_size: number;
  avg_speed: number;
  avg_vision: number;
  avg_metabolism: number;
  avg_fertility: number;
  max_generation: number;
}

export interface WorldState {
  tick: number;
  width: number;
  height: number;
  tiles: Tile[];
  organisms: Organism[];
  species: Species[];
  stats: StatsSnapshot;
  running: boolean;
  tick_interval_ms: number;
}

export interface SimulationConfig {
  population_size: number;
  mutation_rate: number;
  food_regen_multiplier: number;
  tick_interval_ms: number;
}
