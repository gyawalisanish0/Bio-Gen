import "./styles.css";
import { ControlPanel } from "./components/ControlPanel";
import { SimulationCanvas } from "./components/SimulationCanvas";
import { StatsPanel } from "./components/StatsPanel";
import { useSimulation } from "./hooks/useSimulation";

function App() {
  const { state, statsHistory, connected, start, pause, step, reset } = useSimulation();

  return (
    <div className="app">
      <header className="app-header">
        <h1>EvoSim</h1>
        <p>A 16×16 tile-based evolution simulation driven by genetic traits and environmental factors.</p>
        <span className={`status ${connected ? "connected" : "disconnected"}`}>
          {connected ? "● connected" : "○ disconnected"}
        </span>
      </header>

      <main className="app-main">
        <section className="canvas-section">
          <SimulationCanvas state={state} />
        </section>

        <aside className="sidebar">
          <ControlPanel state={state} onStart={start} onPause={pause} onStep={step} onReset={reset} />
          <StatsPanel history={statsHistory} />
        </aside>
      </main>
    </div>
  );
}

export default App;
