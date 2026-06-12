import { useCallback, useEffect, useRef, useState } from "react";
import type { SimulationConfig, StatsSnapshot, WorldState } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
const WS_URL = `${API_BASE.replace(/^http/, "ws")}/ws/simulation`;
const STATS_HISTORY_LIMIT = 200;

interface UseSimulation {
  state: WorldState | null;
  statsHistory: StatsSnapshot[];
  connected: boolean;
  start: () => Promise<void>;
  pause: () => Promise<void>;
  step: () => Promise<void>;
  reset: (config: SimulationConfig) => Promise<void>;
  setSpeed: (tickIntervalMs: number) => Promise<void>;
  launch: (config: SimulationConfig) => Promise<void>;
}

export function useSimulation(): UseSimulation {
  const [state, setState] = useState<WorldState | null>(null);
  const [statsHistory, setStatsHistory] = useState<StatsSnapshot[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onmessage = (event) => {
      const data: WorldState = JSON.parse(event.data);
      applyState(data);
    };

    return () => ws.close();
  }, []);

  const applyState = useCallback((data: WorldState) => {
    setState(data);
    setStatsHistory((prev) => [...prev.slice(-(STATS_HISTORY_LIMIT - 1)), data.stats]);
  }, []);

  const start = useCallback(async () => {
    await fetch(`${API_BASE}/api/simulation/start`, { method: "POST" });
  }, []);

  const pause = useCallback(async () => {
    await fetch(`${API_BASE}/api/simulation/pause`, { method: "POST" });
  }, []);

  const step = useCallback(async () => {
    const res = await fetch(`${API_BASE}/api/simulation/step`, { method: "POST" });
    applyState(await res.json());
  }, [applyState]);

  const reset = useCallback(async (config: SimulationConfig) => {
    const res = await fetch(`${API_BASE}/api/simulation/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(config),
    });
    const data: WorldState = await res.json();
    setState(data);
    setStatsHistory([data.stats]);
  }, []);

  const setSpeed = useCallback(
    async (tickIntervalMs: number) => {
      const res = await fetch(`${API_BASE}/api/simulation/speed`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tick_interval_ms: tickIntervalMs }),
      });
      applyState(await res.json());
    },
    [applyState],
  );

  const launch = useCallback(
    async (config: SimulationConfig) => {
      await reset(config);
      await start();
    },
    [reset, start],
  );

  return { state, statsHistory, connected, start, pause, step, reset, setSpeed, launch };
}
