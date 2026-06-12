import { useEffect, useRef } from "react";
import type { WorldState } from "../types";
import { TRAIT_BOUNDS } from "../traits";

const TERRAIN_COLORS: Record<string, string> = {
  plains: "#cfe8a3",
  forest: "#5b8c3a",
  desert: "#e3c878",
  water: "#5b9bd5",
};

const CELL_SIZE = 28;

interface Props {
  state: WorldState | null;
}

export function SimulationCanvas({ state }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !state) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = state.width * CELL_SIZE;
    canvas.height = state.height * CELL_SIZE;

    drawTiles(ctx, state);
    drawGrid(ctx, state);
    drawOrganisms(ctx, state);
  }, [state]);

  if (!state) {
    return <div className="canvas-placeholder">Connecting to simulation…</div>;
  }

  return <canvas ref={canvasRef} className="simulation-canvas" />;
}

function drawTiles(ctx: CanvasRenderingContext2D, state: WorldState) {
  for (const tile of state.tiles) {
    ctx.fillStyle = TERRAIN_COLORS[tile.terrain] ?? "#cccccc";
    ctx.fillRect(tile.x * CELL_SIZE, tile.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);

    if (tile.max_food > 0 && tile.food > 0) {
      const ratio = tile.food / tile.max_food;
      const pad = CELL_SIZE * 0.25;
      ctx.fillStyle = `rgba(34, 120, 34, ${ratio * 0.6})`;
      ctx.fillRect(tile.x * CELL_SIZE + pad, tile.y * CELL_SIZE + pad, CELL_SIZE - pad * 2, CELL_SIZE - pad * 2);
    }
  }
}

function drawGrid(ctx: CanvasRenderingContext2D, state: WorldState) {
  ctx.strokeStyle = "rgba(0, 0, 0, 0.08)";
  for (let i = 0; i <= state.width; i++) {
    ctx.beginPath();
    ctx.moveTo(i * CELL_SIZE, 0);
    ctx.lineTo(i * CELL_SIZE, state.height * CELL_SIZE);
    ctx.stroke();
  }
  for (let j = 0; j <= state.height; j++) {
    ctx.beginPath();
    ctx.moveTo(0, j * CELL_SIZE);
    ctx.lineTo(state.width * CELL_SIZE, j * CELL_SIZE);
    ctx.stroke();
  }
}

function drawOrganisms(ctx: CanvasRenderingContext2D, state: WorldState) {
  const [speedMin, speedMax] = TRAIT_BOUNDS.speed;
  const [sizeMin, sizeMax] = TRAIT_BOUNDS.size;

  for (const organism of state.organisms) {
    const { speed, size } = organism.genome;

    // Hue maps slow -> fast as blue -> red.
    const speedRatio = (speed - speedMin) / (speedMax - speedMin);
    const hue = 240 - speedRatio * 240;

    // Radius maps small -> large traits onto a visible range.
    const sizeRatio = (size - sizeMin) / (sizeMax - sizeMin);
    const radius = (CELL_SIZE / 2) * (0.35 + sizeRatio * 0.5);

    const cx = organism.x * CELL_SIZE + CELL_SIZE / 2;
    const cy = organism.y * CELL_SIZE + CELL_SIZE / 2;

    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.fillStyle = `hsl(${hue}, 80%, 50%)`;
    ctx.fill();
    ctx.strokeStyle = "rgba(0, 0, 0, 0.4)";
    ctx.stroke();
  }
}
