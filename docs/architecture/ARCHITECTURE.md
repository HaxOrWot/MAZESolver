# 🏗️ System Architecture — MAZESolver

## Overview

MAZESolver follows a **layered, separation-of-concerns architecture**. The three layers never mix:

```
┌─────────────────────────────────────┐
│           PRESENTATION LAYER        │  ← Pygame Renderer + CLI output
├─────────────────────────────────────┤
│            LOGIC LAYER              │  ← BFS / DFS / DLS Solvers
├─────────────────────────────────────┤
│             DATA LAYER              │  ← Maze class + Node class + .txt files
└─────────────────────────────────────┘
```

This separation means:
- Algorithms can be tested **without** Pygame installed
- The maze format can change without touching algorithm code
- The renderer can be swapped (e.g., Tkinter, Web) without touching the AI logic

---

## Component Diagram

```
                    ┌──────────────────────────────────────────┐
                    │               main.py                    │
                    │   (Entry point — parses CLI args)        │
                    └────────────┬─────────────────────────────┘
                                 │  creates
              ┌──────────────────┼──────────────────────┐
              │                  │                       │
              ▼                  ▼                       ▼
        ┌──────────┐    ┌──────────────┐      ┌─────────────────┐
        │  Maze    │    │   Solver     │      │   Renderer      │
        │ (maze.py)│◄───│ (bfs/dfs/   │      │(renderer.py)    │
        └──────────┘    │  dls.py)    │      └────────┬────────┘
              │         └──────┬───────┘               │
              │                │ returns                │ uses
              ▼                ▼                        ▼
        ┌──────────┐    ┌──────────────┐      ┌─────────────────┐
        │  Node    │    │ Result Dict  │      │   HUD           │
        │ (node.py)│    │ {path,       │      │  (hud.py)       │
        └──────────┘    │  visited,    │      └─────────────────┘
                        │  stats...}   │
                        └──────────────┘
```

---

## Class Diagram

```
┌─────────────────────────────────┐
│           Node                  │
├─────────────────────────────────┤
│ + position: tuple(int, int)     │
│ + parent: Node | None           │
│ + depth: int                    │
├─────────────────────────────────┤
│ + get_path() → list[tuple]      │
│ + __eq__(other) → bool          │
│ + __hash__() → int              │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│           Maze                  │
├─────────────────────────────────┤
│ + grid: list[list[str]]         │
│ + rows: int                     │
│ + cols: int                     │
│ + start: tuple(int, int)        │
│ + goal: tuple(int, int)         │
├─────────────────────────────────┤
│ + load_from_file(path) → None   │
│ + is_valid(pos) → bool          │
│ + is_wall(pos) → bool           │
│ + get_neighbors(pos)            │
│     → list[tuple]               │
│ + display() → None (print)      │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        BaseSolver (ABC)         │
├─────────────────────────────────┤
│ + maze: Maze                    │
├─────────────────────────────────┤
│ @abstractmethod                 │
│ + solve() → dict                │
└──────────────┬──────────────────┘
               │  inherits
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│BFSSolv │ │DFSSolv │ │DLSSolv │
│er      │ │er      │ │er      │
├────────┤ ├────────┤ ├────────┤
│        │ │        │ │+limit  │
│        │ │        │ │ :int   │
├────────┤ ├────────┤ ├────────┤
│+solve()│ │+solve()│ │+solve()│
└────────┘ └────────┘ └────────┘

┌─────────────────────────────────┐
│           Renderer              │
├─────────────────────────────────┤
│ + maze: Maze                    │
│ + result: dict                  │
│ + cell_size: int                │
│ + screen: pygame.Surface        │
│ + hud: HUD                      │
├─────────────────────────────────┤
│ + run() → None                  │
│ + draw_maze() → None            │
│ + draw_visited(step) → None     │
│ + draw_path() → None            │
│ + save_screenshot() → None      │
└─────────────────────────────────┘
```

---

## Key Design Decisions

### 1. Solver Returns Full History Upfront
Each solver runs completely first and returns both the `visited` list and the `path`. The Renderer then *replays* the history for animation. This avoids threading complexity and keeps solvers purely deterministic.

### 2. Result Dictionary Contract
All solvers return the **same dict shape**, so `main.py` can handle any algorithm uniformly:
```python
{
    "path": list[tuple],      # Solution path or [] if not found
    "visited": list[tuple],   # All explored nodes in exploration order
    "nodes_explored": int,
    "path_length": int,        # 0 if not found
    "time_taken": float,       # seconds
    "found": bool
}
```

### 3. Maze File Format
Plain `.txt` file. Simple, human-readable, editable in Notepad:
```
#####
#S  #
# # #
#  G#
#####
```
- `#` = Wall
- ` ` (space) = Open path
- `S` = Start
- `G` = Goal

### 4. No Diagonal Movement
Neighbors are strictly: UP `(-1,0)`, DOWN `(+1,0)`, LEFT `(0,-1)`, RIGHT `(0,+1)`. This keeps the search space clean and results predictable for college evaluation.

---

## File Dependency Graph

```
main.py
  ├── maze.py
  │     └── node.py
  ├── algorithms/bfs.py
  │     ├── maze.py
  │     └── node.py
  ├── algorithms/dfs.py
  │     ├── maze.py
  │     └── node.py
  ├── algorithms/dls.py
  │     ├── maze.py
  │     └── node.py
  └── visualization/renderer.py
        ├── maze.py
        ├── visualization/colors.py
        └── visualization/hud.py
```

> **No circular dependencies.** Data flows strictly downward.
