# Pac-Man RL agent with BFS/DFS/A* heuristics  

A modular, extensible Pac‑Man–style gridworld implemented with Pygame. The project provides a clean separation between **I/O**, **environment modeling**, **search/heuristics**, **agents**, and **rendering**, enabling experiments with classical search algorithms and future reinforcement learning (RL) agents.

## Overview
This repository implements a gridworld where an agent plans a path from a **start** cell to a **goal** cell while avoiding **walls**. The default agent is a *search agent* that can run BFS, DFS, UCS, or A* with a selectable heuristic. Rendering is performed with Pygame for an interactive visualization of the planned trajectory.

### Core Modules
- **`environment.py`**: Encapsulates grid dimensions, wall set, start/goal locations, and basic predicates (`in_bounds`, `passable`).  
- **`io.py`**: Robust parser for textual maps; derives `Environment` from file contents, choosing random start/goal if omitted.  
- **`algorithms/search.py`**: Pure algorithmic implementations with minimal coupling (neighbors/cost function callbacks).  
- **`agents/search_agent.py`**: Adapts algorithms to the environment, builds a path, and exposes `plan()` for offline planning.  
- **`game/renderer.py`**: Stateless renderer that draws the grid, planned path, and agent position each frame.  
- **`game/game.py`**: High-level simulation loop, event handling, and timing control.

## Algorithms
### Breadth-First Search (BFS)
- **Optimality**: Optimal for unit-cost grids.  
- **Complexity**: `O(V + E)`; in gridworlds, branching factor `b = 4`, depth `d` → `O(b^d)` in worst case.  
- **Use**: `--algo bfs`

### Depth-First Search (DFS)
- **Optimality**: Not optimal; returns the first found path.  
- **Space**: Linear w.r.t. maximum depth; practical for deep but narrow trees.  
- **Use**: `--algo dfs`

### Uniform-Cost Search (UCS)
- **Optimality**: Optimal for non-negative edge costs.  
- **Use**: `--algo ucs` (default cost is unit cost; extendable via the `cost` function).

### A* Search
- **Optimality**: Optimal when the heuristic is *admissible* (never overestimates) and consistent.  
- **Use**: `--algo astar --heuristic manhattan` (or `euclidean`).

## Heuristics
- **Manhattan** (`L1`): `|x1 - x2| + |y1 - y2|` — suitable for 4-connected grids.  
- **Euclidean** (`L2`): `sqrt((x1 - x2)^2 + (y1 - y2)^2)` — geometrically meaningful; often less informed than Manhattan on 4-neighborhoods but still admissible.

> Heuristics are defined in `pacman/algorithms/heuristics.py`. You can add new heuristics and wire them via the CLI.

## Installation
**Requirements**
- Python **3.9+**
- `pygame` **2.x**

```bash
git clone git://github.com/ak811/dlci.git
cd dlci

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\\Scripts\\Activate.ps1

pip install --upgrade pip
pip install pygame
```

## Usage
Run the simulation from the repository root:
```bash
python -m pacman.main --map pacman/maps/map2.txt --algo astar --heuristic manhattan --fps 20 --tile 40
```

### Examples
```bash
# BFS (shortest path in steps on a unit grid)
python -m pacman.main --map pacman/maps/map1.txt --algo bfs

# UCS (same behavior as BFS on unit-cost grids; enables non-unit costs later)
python -m pacman.main --map pacman/maps/map3.txt --algo ucs

# A* with Euclidean heuristic; larger tiles and higher FPS
python -m pacman.main --map pacman/maps/map2.txt --algo astar --heuristic euclidean --tile 48 --fps 30
```

## Command-Line Interface
```
python -m pacman.main [--map PATH] [--algo {bfs,dfs,ucs,astar}] \
                      [--heuristic {manhattan,euclidean}] \
                      [--fps INT] [--tile INT] [--margin INT]
```
**Parameters**
- `--map PATH` (str): Path to a textual map file. Defaults to `pacman/maps/map2.txt`.
- `--algo` (enum): Search algorithm. One of `bfs`, `dfs`, `ucs`, `astar`. Default: `astar`.
- `--heuristic` (enum): Heuristic for A*. One of `manhattan`, `euclidean`. Default: `manhattan`.
- `--fps` (int): Target frames per second. Default: `15`.
- `--tile` (int): Tile size in pixels. Default: `40`.
- `--margin` (int): Margin around the board in pixels. Default: `0`.

## Map Specification
Maps are plain text with the following glyphs:
- `*` — wall
- `#` — start (spawn)
- `x` or `X` — goal
- space — empty cell

**Notes**
- If **start** or **goal** is absent, a random free cell is selected at load time.
- Non-recognized characters are treated as empty cells for robustness.
- Parsing is implemented in `pacman/io.py` (`read_map`).

