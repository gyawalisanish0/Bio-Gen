import { useCallback, useState } from "react";
import "./styles.css";
import { ControlPanel } from "./components/ControlPanel";
import { SimulationCanvas } from "./components/SimulationCanvas";
import { StartMenu } from "./components/StartMenu";
import { StatsPanel } from "./components/StatsPanel";
import { useSimulation } from "./hooks/useSimulation";
import type { SimulationConfig } from "./types";

type View = "menu" | "simulation";

function App() {
  const { state, statsHistory, connected, start, pause, step, reset, setSpeed, launch } = useSimulation();
  const [view, setView] = useState<View>("menu");

  const handleLaunch = useCallback(
    async (config: SimulationConfig) => {
      await launch(config);
      setView("simulation");
    },
    [launch],
  );

  const handleNewSimulation = useCallback(async () => {
    await pause();
    setView("menu");
  }, [pause]);

  return (
    <div className="app">
      <header className="app-header">
        <h1>EvoSim</h1>
        <p>A 16×16 tile-based evolution simulation driven by genetic traits and environmental factors.</p>
        <span className={`status ${connected ? "connected" : "disconnected"}`}>
          {connected ? "● connected" : "○ disconnected"}
        </span>
      </header>

      {view === "menu" ? (
        <StartMenu onLaunch={handleLaunch} />
      ) : (
        <main className="app-main">
          <section className="canvas-section">
            <SimulationCanvas state={state} />
          </section>

          <aside className="sidebar">
            <ControlPanel
              state={state}
              onStart={start}
              onPause={pause}
              onStep={step}
              onReset={reset}
              onSpeedChange={setSpeed}
              onNewSimulation={handleNewSimulation}
            />
            <StatsPanel history={statsHistory} />
          </aside>
        </main>
      )}
    </div>
  );
}

export default App;
