# EvoSim

A biology-inspired evolution simulation. A population of organisms lives on a
16×16 tile world, foraging for food, spending energy, aging, reproducing, and
dying — all driven by an evolvable **genome** and the **environment** they're
placed in. Watch traits drift over generations as natural selection favors
whatever combination of size, speed, vision, metabolism, and fertility
survives best on the current map.

## How it works

### Genome (`backend/app/simulation/genome.py`)

Each organism has five traits, each bounded and independently mutable
(see `backend/app/config.py` for exact ranges):

| Trait        | Effect |
|--------------|--------|
| `size`       | Bigger organisms eat more food per tick but pay higher movement/metabolic costs; size also extends max lifespan slightly. |
| `speed`      | How many tiles an organism can move per tick (toward food, or randomly if none is visible). |
| `vision`     | Radius (in tiles) within which an organism can detect the richest nearby food tile. |
| `metabolism` | Multiplier on base energy consumption per tick. |
| `fertility`  | Higher fertility lowers the energy threshold required to reproduce. |

When an organism reproduces, its offspring's genome is a copy with each trait
independently mutated (with some probability) by Gaussian noise, clamped to
its valid range.

### World (`backend/app/simulation/world.py`)

A 16×16 grid of tiles, each with a terrain type — plains, forest, desert, or
water — that determines food regrowth rate, food capacity, extra "climate"
energy cost, and whether organisms can move onto it.

### Engine (`backend/app/simulation/engine.py`)

Each tick: the world regrows food, every organism moves/forages/pays energy
costs/ages, organisms that crossed their reproduction threshold spawn mutated
offspring, and dead organisms (starved or aged out) are removed. Population
and average-trait statistics are recorded every tick.

## Project structure

```
backend/
  app/
    config.py          # all tunable constants (single source of truth)
    models.py           # Pydantic API schemas
    simulation/          # pure simulation core (no FastAPI dependency)
      genome.py
      world.py
      organism.py
      engine.py
    api/
      manager.py         # bridges the simulation core to the API/websocket
      routes.py           # REST endpoints
      websocket.py        # live state streaming
    main.py               # FastAPI app
  tests/                  # pytest suite for genome/world/engine/API

frontend/
  src/
    types.ts              # TS mirrors of the API schemas
    traits.ts             # trait bounds used for visualization scaling
    hooks/useSimulation.ts # websocket + REST client hook
    components/
      SimulationCanvas.tsx # renders the grid, terrain, food, and organisms
      ControlPanel.tsx      # start/pause/step/reset + config sliders
      StatsPanel.tsx         # live population & trait charts (Recharts)
    App.tsx
```

## Running it

### Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --reload --port 8000
```

Run tests with:

```bash
.venv/bin/python -m pytest
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

By default the frontend talks to `http://localhost:8000`. To point it at a
different backend, copy `.env.example` to `.env` and set `VITE_API_BASE`.

## Docker

Each service has its own `Dockerfile`:

```bash
# Backend - serves the API on :8000
docker build -t evosim-backend ./backend
docker run -p 8000:8000 evosim-backend

# Frontend - builds the static site and serves it with nginx on :80
# VITE_API_BASE is baked in at build time, so point it at your backend's URL.
docker build -t evosim-frontend --build-arg VITE_API_BASE=http://localhost:8000 ./frontend
docker run -p 8080:80 evosim-frontend
```

On every push to `main`, `.github/workflows/docker-publish.yml` builds both
images and publishes them to GitHub Container Registry as
`ghcr.io/<owner>/<repo>-backend` and `ghcr.io/<owner>/<repo>-frontend`,
tagged `latest` and with the commit SHA.

## API overview

| Method | Path                       | Description |
|--------|----------------------------|--------------|
| GET    | `/api/simulation/state`    | Current world state, organisms, and latest stats |
| GET    | `/api/simulation/stats`    | Full stats history |
| POST   | `/api/simulation/reset`    | Reset with optional `{population_size, mutation_rate, food_regen_multiplier}` |
| POST   | `/api/simulation/step`     | Advance one tick |
| POST   | `/api/simulation/start`    | Start the background tick loop |
| POST   | `/api/simulation/pause`    | Pause the background tick loop |
| WS     | `/ws/simulation`            | Streams the world state on every tick while running |

## Ideas for extending

- A second species (predator/prey dynamics)
- Sexual reproduction with two-parent genome crossover
- More biomes / a larger or randomly generated map
- Save/replay specific simulation runs
