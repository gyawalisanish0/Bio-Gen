import { useState } from "react";
import type { SimulationConfig, WorldState } from "../types";
import { DEFAULT_CONFIG, FOOD_REGEN_RANGE, MUTATION_RATE_RANGE, POPULATION_RANGE, TICK_INTERVAL_RANGE } from "../constants";

interface Props {
  state: WorldState | null;
  onStart: () => void;
  onPause: () => void;
  onStep: () => void;
  onReset: (config: SimulationConfig) => void;
  onSpeedChange: (tickIntervalMs: number) => void;
  onNewSimulation: () => void;
}

export function ControlPanel({ state, onStart, onPause, onStep, onReset, onSpeedChange, onNewSimulation }: Props) {
  const [populationSize, setPopulationSize] = useState(DEFAULT_CONFIG.population_size);
  const [mutationRate, setMutationRate] = useState(DEFAULT_CONFIG.mutation_rate);
  const [foodRegenMultiplier, setFoodRegenMultiplier] = useState(DEFAULT_CONFIG.food_regen_multiplier);

  const running = state?.running ?? false;
  const tickIntervalMs = state?.tick_interval_ms ?? DEFAULT_CONFIG.tick_interval_ms;

  return (
    <div className="control-panel">
      <h2>Controls</h2>

      <div className="control-row">
        <button onClick={onStart} disabled={running}>
          ▶ Start
        </button>
        <button onClick={onPause} disabled={!running}>
          ⏸ Pause
        </button>
        <button onClick={onStep}>⏭ Step</button>
        <button
          onClick={() =>
            onReset({
              population_size: populationSize,
              mutation_rate: mutationRate,
              food_regen_multiplier: foodRegenMultiplier,
              tick_interval_ms: tickIntervalMs,
            })
          }
        >
          ↺ Reset
        </button>
      </div>

      <label className="control-field">
        Tick interval: {tickIntervalMs}ms (lower = faster)
        <input
          type="range"
          min={TICK_INTERVAL_RANGE.min}
          max={TICK_INTERVAL_RANGE.max}
          step={TICK_INTERVAL_RANGE.step}
          value={tickIntervalMs}
          onChange={(e) => onSpeedChange(Number(e.target.value))}
        />
      </label>

      <label className="control-field">
        Initial population: {populationSize}
        <input
          type="range"
          min={POPULATION_RANGE.min}
          max={POPULATION_RANGE.max}
          step={POPULATION_RANGE.step}
          value={populationSize}
          onChange={(e) => setPopulationSize(Number(e.target.value))}
        />
      </label>

      <label className="control-field">
        Mutation rate: {mutationRate.toFixed(2)}
        <input
          type="range"
          min={MUTATION_RATE_RANGE.min}
          max={MUTATION_RATE_RANGE.max}
          step={MUTATION_RATE_RANGE.step}
          value={mutationRate}
          onChange={(e) => setMutationRate(Number(e.target.value))}
        />
      </label>

      <label className="control-field">
        Food regrowth: {foodRegenMultiplier.toFixed(1)}x
        <input
          type="range"
          min={FOOD_REGEN_RANGE.min}
          max={FOOD_REGEN_RANGE.max}
          step={FOOD_REGEN_RANGE.step}
          value={foodRegenMultiplier}
          onChange={(e) => setFoodRegenMultiplier(Number(e.target.value))}
        />
      </label>

      <button className="new-simulation-button" onClick={onNewSimulation}>
        ⏹ New simulation
      </button>
    </div>
  );
}
