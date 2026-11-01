# 🧩 MAZESolver 2.0 — Uninformed & Informed AI Search Suite

> **AI College Project** | BFS · DFS · DLS · IDDFS · A* (Heuristic)  
> **Language:** Python 3.10+ | **Visualization:** Pygame & Pillow

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green)
![Pillow](https://img.shields.io/badge/Pillow-13.0+-yellow)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Overview

**MAZESolver 2.0** is an academic Artificial Intelligence laboratory demonstration comparing **Uninformed (Blind)** and **Informed (Heuristic)** search algorithms on 2D grid mazes.

### 🤖 Supported Algorithms

| Algorithm | Category | Data Structure | Optimal? | Complete? | Time | Space |
|-----------|----------|----------------|----------|-----------|------|-------|
| **BFS** | Uninformed | Queue (FIFO) | ✅ Yes | ✅ Yes | $O(V+E)$ | $O(V)$ |
| **DFS** | Uninformed | Stack (LIFO) | ❌ No | ✅ Yes* | $O(V+E)$ | $O(d)$ |
| **DLS** | Uninformed | Stack + Limit | ❌ No | ❌ No | $O(b^L)$ | $O(L)$ |
| **IDDFS** | Uninformed | Iterative Stack| ✅ Yes | ✅ Yes | $O(b^d)$ | $O(d)$ |
| **A\*** | Informed | Min-Heap Priority Queue | ✅ Yes | ✅ Yes | $O((V+E)\log V)$ | $O(V)$ |

*\*On finite, loop-checked graphs.*

---

## ✨ Features (v2.0 Upgrade)

- 🌈 **Exploration Heatmap Gradient:** Cells transition smoothly from cold blue to hot orange/magenta based on exploration order.
- 🎨 **4 Dynamic Color Themes:** Switch on-the-fly (`T` key) between `Dark`, `Neon`, `Retro CRT`, and `Light`.
- 📊 **Multi-Tab HUD:** Press `1` (Live Performance Stats & Coverage), `2` (Frontier/Stack Inspector), or `3` (Algorithm Explainer).
- 🖥️ **Split-Screen Comparison View:** Run BFS, DFS, and DLS side-by-side in real-time (`--splitview`).
- 🏗️ **Procedural Maze Generator:** Infinite solvable mazes via Recursive Backtracking or Randomized Prim's (`--generate`).
- ✏️ **Interactive Maze Editor:** Click-and-drag drawing canvas with undo history and instant solve previews (`--edit`).
- 🎆 **Particle Burst System:** Celebratory physics particles when the solution reaches the goal.
- 🎞️ **Animated GIF Export:** Encode headless runs directly into looping GIFs (`--export-gif` or `G` key).
- 🔊 **Sound Effects:** Exploration tick frequency and goal fanfare chords (mute with `M`).

---

## 📁 Directory Structure

```
MAZESolver/
├── src/
│   ├── main.py                   # CLI runner & coordinator
│   ├── config.py                 # Configuration manager
│   ├── maze.py                   # Grid parsing & topology validation
│   ├── node.py                   # Search node with parent backtracking
│   ├── algorithms/
│   │   ├── base_solver.py        # Abstract solver contract
│   │   ├── bfs.py                # Breadth-First Search
│   │   ├── dfs.py                # Depth-First Search
│   │   ├── dls.py                # Depth-Limited Search
│   │   ├── iddfs.py              # Iterative Deepening DFS
│   │   └── astar.py              # A* Search with Manhattan distance
│   ├── generator/
│   │   ├── recursive_backtrack.py# Winding corridor generator
│   │   ├── prims.py              # Branching corridor generator
│   │   └── generator_cli.py      # Standalone generator tool
│   ├── editor/
│   │   └── maze_editor.py        # Interactive GUI maze designer
│   └── visualization/
│       ├── renderer.py           # Advanced Pygame visualizer
│       ├── split_view.py         # Side-by-side comparison engine
│       ├── hud.py                # 3-tab live HUD display
│       ├── themes.py             # Dark / Neon / Retro / Light palettes
│       ├── particles.py          # Particle effects engine
│       ├── sound_manager.py      # Audio feedback
│       └── gif_exporter.py       # Pillow animated GIF encoder
├── data/                         # Sample and generated mazes
├── tests/                        # 47 automated unit tests
├── docs/                         # Specifications & planning docs
├── config.json                   # User customizable settings
└── requirements.txt
```

---

## ⚡ Quick Start

### 1. Installation
```powershell
git clone https://github.com/HaxOrWot/MAZESolver.git
cd MAZESolver
pip install -r requirements.txt
```

### 2. Run Single Algorithm with Visualization
```powershell
python src/main.py --maze data/maze_20x20.txt --algo astar --visual
```

### 3. Compare All 5 Algorithms (CLI Table)
```powershell
python src/main.py --maze data/maze_20x20.txt --compare
```
*Output Table:*
```
╔════════════════╦═════════╦════════════════╦══════════════╦══════════════╗
║  Algorithm     ║  Found? ║ Nodes Explored ║ Path Length  ║  Time (ms)   ║
╠════════════════╬═════════╬════════════════╬══════════════╬══════════════╣
║  BFS           ║  YES    ║     94         ║     33       ║    0.26      ║
║  DFS           ║  YES    ║     38         ║     37       ║    0.10      ║
║  DLS (L=41)    ║  YES    ║     38         ║     37       ║    0.10      ║
║  IDDFS         ║  YES    ║     1540       ║     33       ║    3.64      ║
║  A* (Heuristic)║  YES    ║     76         ║     33       ║    0.21      ║
╚════════════════╩═════════╩════════════════╩══════════════╩══════════════╝
```

### 4. Split-Screen Synchronized View
```powershell
python src/main.py --maze data/maze_20x20.txt --splitview --theme neon
```

### 5. Generate and Solve a Random Maze
```powershell
python src/main.py --generate --maze-size 25 --algo bfs --visual
```

### 6. Interactive Maze Editor
```powershell
python src/main.py --edit
```
- **Left Click / Drag:** Draw or toggle walls
- **Right Click:** Cycle Start (`S`) or Goal (`G`)
- **`B` / `D` / `A`:** Preview BFS, DFS, or A* solution overlay
- **`Ctrl+S`:** Save custom maze to file
- **`Ctrl+G`:** Generate procedural maze

### 7. Export Animated GIF
```powershell
python src/main.py --maze data/maze_20x20.txt --algo astar --export-gif
```
*Outputs looping GIF to `output/gifs/`.*

---

## 🎮 Visualizer Keyboard Controls

| Key | Action |
|-----|--------|
| `SPACE` | Pause / Resume animation |
| `R` | Reset and replay |
| `T` | Cycle visual theme (Dark / Neon / Retro / Light) |
| `M` | Toggle sound effects on/off |
| `1` | Show Performance & Coverage Stats |
| `2` | Open Frontier / Stack Inspector |
| `3` | Open Algorithm Concept Explainer |
| `S` | Save high-resolution PNG screenshot |
| `G` | Export full solve as animated GIF |
| `↑` / `↓` | Adjust animation speed |
| `ESC` | Exit |

---

## 🧪 Testing

Run all 47 tests with coverage:
```powershell
pytest tests/ -v
```

---

## 👤 Author

**HaxOrWot** — College AI Project
