import { useState } from "react";
import type { SimulationConfig } from "../types";
import { DEFAULT_CONFIG, FOOD_REGEN_RANGE, MUTATION_RATE_RANGE, POPULATION_RANGE, TICK_INTERVAL_RANGE } from "../constants";

interface Props {
  onLaunch: (config: SimulationConfig) => void;
}

export function StartMenu({ onLaunch }: Props) {
  const [config, setConfig] = useState<SimulationConfig>(DEFAULT_CONFIG);

  const update = <K extends keyof SimulationConfig>(key: K, value: SimulationConfig[K]) =>
    setConfig((prev) => ({ ...prev, [key]: value }));

  return (
    <div className="start-menu">
      <div className="start-menu-card">
        <h2>Configure your world</h2>
        <p>
          A 16×16 tile world where a population of organisms forages, ages, reproduces, and dies based on an
          evolvable genome (size, speed, vision, metabolism, fertility). Set the starting conditions below, then
          launch the simulation and watch natural selection play out.
        </p>

        <label className="control-field">
          Initial population: {config.population_size}
          <input
            type="range"
            min={POPULATION_RANGE.min}
            max={POPULATION_RANGE.max}
            step={POPULATION_RANGE.step}
            value={config.population_size}
            onChange={(e) => update("population_size", Number(e.target.value))}
          />
        </label>

        <label className="control-field">
          Mutation rate: {config.mutation_rate.toFixed(2)}
          <input
            type="range"
            min={MUTATION_RATE_RANGE.min}
            max={MUTATION_RATE_RANGE.max}
            step={MUTATION_RATE_RANGE.step}
            value={config.mutation_rate}
            onChange={(e) => update("mutation_rate", Number(e.target.value))}
          />
        </label>

        <label className="control-field">
          Food regrowth: {config.food_regen_multiplier.toFixed(1)}x
          <input
            type="range"
            min={FOOD_REGEN_RANGE.min}
            max={FOOD_REGEN_RANGE.max}
            step={FOOD_REGEN_RANGE.step}
            value={config.food_regen_multiplier}
            onChange={(e) => update("food_regen_multiplier", Number(e.target.value))}
          />
        </label>

        <label className="control-field">
          Tick interval: {config.tick_interval_ms}ms (lower = faster)
          <input
            type="range"
            min={TICK_INTERVAL_RANGE.min}
            max={TICK_INTERVAL_RANGE.max}
            step={TICK_INTERVAL_RANGE.step}
            value={config.tick_interval_ms}
            onChange={(e) => update("tick_interval_ms", Number(e.target.value))}
          />
        </label>

        <button className="launch-button" onClick={() => onLaunch(config)}>
          ▶ Launch simulation
        </button>
      </div>
    </div>
  );
}
