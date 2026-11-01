# 🧩 MAZESolver 2.0 — Uninformed & Informed AI Search Suite

> **AI College Project** | BFS · DFS · DLS · IDDFS · A* (Heuristic)  
> **Language:** Python 3.10+ | **Visualization:** Pygame & Pillow

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green)
![Pillow](https://img.shields.io/badge/Pillow-13.0+-yellow)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ⚡ Super Short Commands (Fast Start)

No need to write long paths or complex arguments! Use `.\maze` (PowerShell/CMD) or `python run.py`:

| What you want to do | Short Command (Windows) | Cross-Platform |
|---------------------|-------------------------|----------------|
| **Launch Visualizer** | `.\maze` | `python run.py` |
| **Compare all 5 algorithms** | `.\maze -c` | `python run.py -c` |
| **Split-screen comparison (3 panels)** | `.\maze -s` | `python run.py -s` |
| **Interactive Maze Editor** | `.\maze -e` | `python run.py -e` |
| **Solve 50x50 Maze** | `.\maze 50` | `python run.py 50` |
| **Solve 100x100 with A\*** | `.\maze 100 astar` | `python run.py 100 astar` |
| **Neon Cyberpunk Theme** | `.\maze 20 -t neon` | `python run.py 20 -t neon` |
| **Export Animated GIF** | `.\maze 10 --export-gif` | `python run.py 10 --export-gif` |
| **Generate a fresh 35x35 maze** | `.\maze -g --maze-size 35` | `python run.py -g --maze-size 35` |

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

## 📁 Included Mazes (`data/`)

Pre-generated, guaranteed-solvable mazes ready to run:

- `maze_5x5.txt`
- `maze_10x10.txt`
- `maze_20x20.txt`
- `maze_30x30.txt`
- `maze_40x40.txt`
- `maze_50x50.txt`
- `maze_60x60.txt`
- `maze_70x70.txt`
- `maze_80x80.txt`
- `maze_90x90.txt`
- `maze_100x100.txt` *(Stress Test: 10,000+ cells)*

You can pass just the number to any command (e.g. `.\maze 40` or `.\maze 100`).

---

## ✨ Features (v2.0)

- 🌈 **Exploration Heatmap Gradient:** Cells transition smoothly from cold blue to hot orange/magenta based on exploration order.
- 🎨 **4 Dynamic Color Themes:** Switch on-the-fly (`T` key) between `Dark`, `Neon`, `Retro CRT`, and `Light`.
- 📊 **Multi-Tab HUD:** Press `1` (Live Performance Stats & Coverage), `2` (Frontier/Stack Inspector), or `3` (Algorithm Explainer).
- 🖥️ **Split-Screen Comparison View:** Run BFS, DFS, and DLS side-by-side in real-time (`.\maze -s`).
- 🏗️ **Procedural Maze Generator:** Infinite solvable mazes via Recursive Backtracking or Randomized Prim's (`.\maze -g`).
- ✏️ **Interactive Maze Editor:** Click-and-drag drawing canvas with undo history and instant solve previews (`.\maze -e`).
- 🎆 **Particle Burst System:** Celebratory physics particles when the solution reaches the goal.
- 🎞️ **Animated GIF Export:** Encode headless runs directly into looping GIFs (`--export-gif` or `G` key).
- 🔊 **Sound Effects:** Exploration tick frequency and goal fanfare chords (mute with `M`).

---

## 📊 Sample Output (`.\maze -c`)

```
Running 5-Algorithm Comparison on 'maze_20x20.txt'...

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

---

## 🎮 Visualizer In-Window Controls

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

## 🧪 Running Tests

Run all 47 tests:
```powershell
pytest tests/ -v
```

---

## 👤 Author

**HaxOrWot** — College AI Project
