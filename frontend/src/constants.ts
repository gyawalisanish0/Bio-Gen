import type { SimulationConfig } from "./types";

/**
 * Mirrors backend/app/config.py simulation defaults and bounds. Kept in sync
 * manually since the frontend only needs these for slider ranges/defaults.
 */
export const DEFAULT_CONFIG: SimulationConfig = {
  population_size: 24,
  mutation_rate: 0.15,
  food_regen_multiplier: 1.0,
  tick_interval_ms: 200,
};

export const POPULATION_RANGE = { min: 4, max: 60, step: 1 };
export const MUTATION_RATE_RANGE = { min: 0, max: 1, step: 0.01 };
export const FOOD_REGEN_RANGE = { min: 0.1, max: 3, step: 0.1 };
export const TICK_INTERVAL_RANGE = { min: 50, max: 1000, step: 50 };
