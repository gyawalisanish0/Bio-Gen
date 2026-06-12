import { useState } from "react";
import type { SimulationConfig, WorldState } from "../types";

interface Props {
  state: WorldState | null;
  onStart: () => void;
  onPause: () => void;
  onStep: () => void;
  onReset: (config: SimulationConfig) => void;
}

export function ControlPanel({ state, onStart, onPause, onStep, onReset }: Props) {
  const [populationSize, setPopulationSize] = useState(24);
  const [mutationRate, setMutationRate] = useState(0.15);
  const [foodRegenMultiplier, setFoodRegenMultiplier] = useState(1.0);

  const running = state?.running ?? false;

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
            })
          }
        >
          ↺ Reset
        </button>
      </div>

      <label className="control-field">
        Initial population: {populationSize}
        <input
          type="range"
          min={4}
          max={60}
          value={populationSize}
          onChange={(e) => setPopulationSize(Number(e.target.value))}
        />
      </label>

      <label className="control-field">
        Mutation rate: {mutationRate.toFixed(2)}
        <input
          type="range"
          min={0}
          max={1}
          step={0.01}
          value={mutationRate}
          onChange={(e) => setMutationRate(Number(e.target.value))}
        />
      </label>

      <label className="control-field">
        Food regrowth: {foodRegenMultiplier.toFixed(1)}x
        <input
          type="range"
          min={0.1}
          max={3}
          step={0.1}
          value={foodRegenMultiplier}
          onChange={(e) => setFoodRegenMultiplier(Number(e.target.value))}
        />
      </label>
    </div>
  );
}
