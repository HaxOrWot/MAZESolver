# 🧩 MAZESolver — Master Project Plan

> **Topic:** Maze Solver Using AI (Uninformed Search)  
> **Algorithms:** BFS · DFS · DLS  
> **Language:** Python (primary) + HTML/CSS (optional report viewer)  
> **GitHub:** https://github.com/HaxOrWot/MAZESolver  
> **Expected Output:** Visual Solution Path with performance comparison  

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Folder Structure](#2-folder-structure)
3. [Phase-by-Phase Build Plan](#3-phase-by-phase-build-plan)
4. [File Responsibilities](#4-file-responsibilities)
5. [Data Flow](#5-data-flow)
6. [Tech Stack](#6-tech-stack)
7. [Git Commit Strategy](#7-git-commit-strategy)
8. [Deliverables Checklist](#8-deliverables-checklist)

---

## 1. Project Overview

This project demonstrates **Uninformed (Blind) Search** in Artificial Intelligence by solving a 2D grid maze using three classic algorithms:

| Algorithm | Full Name | Data Structure | Optimal? | Complete? |
|-----------|-----------|----------------|----------|-----------|
| BFS | Breadth-First Search | Queue (FIFO) | ✅ Yes | ✅ Yes |
| DFS | Depth-First Search | Stack (LIFO) | ❌ No | ✅ Yes (finite) |
| DLS | Depth-Limited Search | Stack + Depth limit | ❌ No | ❌ No (limited) |

The program:
- Loads a maze from a `.txt` file (grid format)
- Runs any of the 3 algorithms on demand
- Visualizes the search process step-by-step using **Pygame**
- Outputs the solution path, nodes explored, time taken, and path length
- Saves results to the `output/` folder as text and image screenshots

---

## 2. Folder Structure

```
MAZESolver/
│
├── src/                          # All Python source code
│   ├── __init__.py
│   ├── main.py                   # Entry point — CLI + Pygame launcher
│   ├── maze.py                   # Maze class: load, parse, validate, neighbors
│   ├── node.py                   # Node class: position, parent, depth
│   │
│   ├── algorithms/               # AI search algorithms (pure logic, no UI)
│   │   ├── __init__.py
│   │   ├── base_solver.py        # Abstract base class for all solvers
│   │   ├── bfs.py                # Breadth-First Search
│   │   ├── dfs.py                # Depth-First Search
│   │   └── dls.py                # Depth-Limited Search
│   │
│   └── visualization/            # Pygame rendering & display
│       ├── __init__.py
│       ├── renderer.py           # Main Pygame draw loop
│       ├── colors.py             # Color constants
│       └── hud.py                # On-screen HUD (stats panel)
│
├── data/                         # Maze input files
│   ├── maze_5x5.txt              # Tiny maze (for quick tests)
│   ├── maze_10x10.txt            # Small maze
│   ├── maze_20x20.txt            # Medium maze
│   ├── maze_30x30.txt            # Large maze (stress test)
│   └── maze_format.md            # Explains the maze file format
│
├── output/                       # Auto-generated results (gitignored)
│   ├── results_log.txt           # Run history with stats
│   └── screenshots/              # PNG exports of solved mazes
│
├── tests/                        # Automated unit tests
│   ├── __init__.py
│   ├── test_maze.py              # Tests for Maze class
│   ├── test_bfs.py               # BFS correctness tests
│   ├── test_dfs.py               # DFS correctness tests
│   └── test_dls.py               # DLS correctness tests
│
├── docs/                         # ← YOU ARE HERE (planning & design)
│   ├── PROJECT_PLAN.md           # This file — master plan
│   ├── architecture/
│   │   ├── ARCHITECTURE.md       # System design & component diagram
│   │   └── DATA_FLOW.md          # How data moves through the system
│   ├── algorithms/
│   │   ├── BFS.md                # BFS deep-dive: theory + pseudocode
│   │   ├── DFS.md                # DFS deep-dive: theory + pseudocode
│   │   └── DLS.md                # DLS deep-dive: theory + pseudocode
│   ├── ui/
│   │   └── UI_DESIGN.md          # Pygame layout wireframe & UX plan
│   └── testing/
│       └── TEST_PLAN.md          # Test cases and coverage plan
│
├── .gitignore
├── requirements.txt              # pip dependencies
├── README.md                     # Public-facing project readme
└── report/                       # College submission report (optional)
    └── REPORT.md                 # Full academic write-up template
```

---

## 3. Phase-by-Phase Build Plan

> Build in this exact order. Each phase is independently testable.

### ✅ Phase 0 — Repository Setup (Day 0)
- [ ] Clone repo from GitHub
- [ ] Create all folders from the structure above (empty `__init__.py` files)
- [ ] Create `requirements.txt` with: `pygame`, `pytest`, `colorama`
- [ ] Write `.gitignore`
- [ ] Make initial commit: `"chore: scaffold project structure"`

---

### 🧱 Phase 1 — Core Data Structures (Day 1)

**Files to build:**
1. `src/node.py` — Build the `Node` class
2. `src/maze.py` — Build the `Maze` class
3. `data/maze_5x5.txt` — Create the smallest test maze

**What to implement in `Node`:**
- `position: tuple(row, col)`
- `parent: Node | None`
- `depth: int`
- Method: `get_path()` — backtracks through parents to return full solution path

**What to implement in `Maze`:**
- `load_from_file(filepath)` — reads `.txt` grid
- `get_neighbors(position)` — returns valid adjacent cells (UP, DOWN, LEFT, RIGHT)
- `is_wall(position)` → bool
- `is_valid(position)` → bool (within bounds + not a wall)
- Properties: `start`, `goal`, `rows`, `cols`, `grid`

**Exit criteria:** `python -c "from src.maze import Maze; m = Maze('data/maze_5x5.txt'); print(m.start, m.goal)"` prints correctly.

---

### 🤖 Phase 2 — AI Algorithms (Day 2)

**Files to build:**
1. `src/algorithms/base_solver.py` — Abstract base
2. `src/algorithms/bfs.py`
3. `src/algorithms/dfs.py`
4. `src/algorithms/dls.py`

**What each solver returns:**
```python
{
    "path": [(r,c), (r,c), ...],   # Solution path (list of positions)
    "visited": [(r,c), ...],        # All nodes explored (for animation)
    "nodes_explored": int,          # Count of nodes popped from frontier
    "path_length": int,             # Length of solution path
    "time_taken": float,            # Seconds (perf_counter)
    "found": bool                   # Whether a solution was found
}
```

**Implement in this order:** BFS → DFS → DLS (DLS is DFS with a depth cutoff)

**Exit criteria:** Each algorithm solves `maze_5x5.txt` and returns a valid path.

---

### 🖥️ Phase 3 — CLI Interface (Day 3)

**File to build:** `src/main.py`

**Command-line usage:**
```bash
# Run BFS on a maze (text output only)
python src/main.py --maze data/maze_10x10.txt --algo bfs

# Run DFS with visual Pygame window
python src/main.py --maze data/maze_20x20.txt --algo dfs --visual

# Run DLS with depth limit
python src/main.py --maze data/maze_20x20.txt --algo dls --limit 15 --visual

# Compare all 3 algorithms (no visual, prints table)
python src/main.py --maze data/maze_20x20.txt --compare
```

**Text output format (non-visual):**
```
Algorithm : BFS
Maze File : data/maze_10x10.txt
──────────────────────────────────
Found      : YES
Path Length: 23 steps
Nodes Exp. : 47
Time Taken : 0.000412 seconds

Solution Path:
S . . # # # . . . .
# # . # . # . # # #
...
```

**Exit criteria:** CLI works for all 3 algorithms with `--compare` showing a summary table.

---

### 🎨 Phase 4 — Pygame Visualization (Day 4–5)

**Files to build:**
1. `src/visualization/colors.py` — Color palette constants
2. `src/visualization/hud.py` — Stats panel on right side of screen
3. `src/visualization/renderer.py` — Main rendering loop

**Visual elements:**
| Element | Color | Meaning |
|---------|-------|---------|
| Wall cell | Dark gray `#2C2C2C` | Impassable |
| Open cell | White `#F0F0F0` | Passable |
| Start cell | Green `#00C853` | Entry point `S` |
| Goal cell | Red `#D50000` | Exit point `G` |
| Visited cell | Light blue `#81D4FA` | Explored by algorithm |
| Solution path | Yellow `#FFD600` | Final answer path |
| Current cell | Orange `#FF6D00` | Frontier head |

**Animation behavior:**
- Step through `visited` nodes one by one (controlled by `ANIMATION_SPEED`)
- After all visited nodes shown → highlight solution path in yellow
- Press `SPACE` to pause/resume
- Press `R` to reset and re-run
- Press `ESC` to quit
- Press `S` to save screenshot to `output/screenshots/`

**HUD panel (right side 250px):**
- Algorithm name
- Maze file
- Nodes Explored (live counter)
- Path Length
- Time Taken
- Status: SEARCHING / SOLVED / NO PATH

**Exit criteria:** Pygame window opens, animates search, highlights path, HUD updates live.

---

### 🧪 Phase 5 — Tests (Day 6)

**Files to build:**
1. `tests/test_maze.py`
2. `tests/test_bfs.py`
3. `tests/test_dfs.py`
4. `tests/test_dls.py`

**Key test cases:**
- BFS always finds the shortest path
- DFS finds *a* path (correctness, not optimality)
- DLS returns `found=False` when depth limit is too small
- DLS returns `found=True` when depth limit is sufficient
- Maze with no valid path returns `found=False`
- `get_path()` on `Node` returns correct coordinates

**Exit criteria:** `pytest tests/ -v` → all green.

---

### 📊 Phase 6 — Output & Comparison Report (Day 7)

**Files to build:**
1. `output/results_log.txt` generator (auto-appended on each run)
2. `--compare` mode: runs all 3 on same maze, prints side-by-side table
3. `report/REPORT.md` — fill in academic write-up

**Comparison table output:**
```
╔══════════════╦═════════════╦═══════════════╦═════════════╦══════════════╗
║  Algorithm   ║  Found?     ║ Nodes Explored║ Path Length ║  Time (ms)   ║
╠══════════════╬═════════════╬═══════════════╬═════════════╬══════════════╣
║  BFS         ║  ✅ YES     ║     47        ║     23      ║    0.41      ║
║  DFS         ║  ✅ YES     ║     63        ║     31      ║    0.23      ║
║  DLS (L=20)  ║  ✅ YES     ║     38        ║     29      ║    0.31      ║
╚══════════════╩═════════════╩═══════════════╩═════════════╚══════════════╝
```

---

## 4. File Responsibilities

| File | Owner Class/Function | Responsibility |
|------|---------------------|----------------|
| `src/node.py` | `Node` | State representation, path backtracking |
| `src/maze.py` | `Maze` | Grid storage, neighbor generation, validation |
| `src/algorithms/base_solver.py` | `BaseSolver` (ABC) | Interface contract for all solvers |
| `src/algorithms/bfs.py` | `BFSSolver` | FIFO queue search, returns result dict |
| `src/algorithms/dfs.py` | `DFSSolver` | LIFO stack search, returns result dict |
| `src/algorithms/dls.py` | `DLSSolver` | Depth-limited LIFO search, returns result dict |
| `src/main.py` | `main()` | CLI arg parsing, wires maze + solver + renderer |
| `src/visualization/renderer.py` | `Renderer` | Pygame loop, animation, screenshot |
| `src/visualization/hud.py` | `HUD` | Stats panel rendering |
| `src/visualization/colors.py` | constants | Color palette |

---

## 5. Data Flow

```
[CLI Args]
    │
    ▼
[main.py] ──loads──► [Maze] ──provides──► [Solver (BFS/DFS/DLS)]
                                                    │
                                            returns result dict
                                                    │
                    ┌───────────────────────────────┘
                    │
                    ├──► [CLI text output]  (if no --visual)
                    │
                    └──► [Renderer]  (if --visual)
                              │
                              ├──► Pygame window (animation)
                              ├──► HUD (live stats)
                              └──► Screenshot (on S key / auto)
```

---

## 6. Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| Pygame | 2.5+ | Visualization window |
| pytest | 7.x | Automated testing |
| colorama | 0.4+ | Colored CLI output |
| argparse | stdlib | CLI argument parsing |
| collections.deque | stdlib | BFS queue |
| time.perf_counter | stdlib | Precise timing |

Install all with:
```bash
pip install -r requirements.txt
```

---

## 7. Git Commit Strategy

Use **conventional commits**. Commit after each phase:

```
chore: scaffold project structure
feat(maze): implement Maze class with grid loading
feat(node): implement Node class with path backtracking
feat(bfs): implement BFS solver
feat(dfs): implement DFS solver
feat(dls): implement DLS solver with depth limit
feat(cli): add argparse CLI with --algo and --compare flags
feat(visual): add Pygame renderer with animation
feat(visual): add HUD stats panel
feat(visual): add screenshot export on S key
test: add unit tests for maze loading
test: add unit tests for BFS, DFS, DLS
docs: add README with setup and usage instructions
chore: add sample mazes 5x5 to 30x30
```

---

## 8. Deliverables Checklist

- [ ] `src/` — All Python modules implemented
- [ ] `data/` — 4 maze files (5x5, 10x10, 20x20, 30x30)
- [ ] `tests/` — All unit tests passing (`pytest`)
- [ ] `output/` — Sample results and screenshots
- [ ] `docs/` — All documentation files
- [ ] `README.md` — Setup, usage, screenshots
- [ ] `report/REPORT.md` — Academic write-up
- [ ] GitHub — Clean commit history, no junk files
