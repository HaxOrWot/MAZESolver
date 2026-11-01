# 🧩 MAZESolver

> **AI Micro Project** | Uninformed Search | BFS · DFS · DLS  
> **Language:** Python 3.10+ | **Visualization:** Pygame

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 About

MAZESolver is an AI project that demonstrates **Uninformed (Blind) Search** by solving 2D grid mazes using three classic algorithms:

| Algorithm | Optimal? | Complete? | Data Structure |
|-----------|----------|-----------|----------------|
| **BFS** — Breadth-First Search | ✅ Yes | ✅ Yes | Queue (FIFO) |
| **DFS** — Depth-First Search | ❌ No | ✅ Yes | Stack (LIFO) |
| **DLS** — Depth-Limited Search | ❌ No | ❌ No | Stack + Depth Limit |

---

## 📁 Project Structure

```
MAZESolver/
├── src/
│   ├── main.py               # Entry point (CLI)
│   ├── maze.py               # Maze loading & grid logic
│   ├── node.py               # Node class for search tree
│   ├── algorithms/
│   │   ├── base_solver.py    # Abstract base class
│   │   ├── bfs.py            # BFS implementation
│   │   ├── dfs.py            # DFS implementation
│   │   └── dls.py            # DLS implementation
│   └── visualization/
│       ├── renderer.py       # Pygame visualization
│       ├── hud.py            # Stats HUD panel
│       └── colors.py         # Color constants
├── data/                     # Maze .txt files
├── output/                   # Results & screenshots
├── tests/                    # pytest unit tests
├── docs/                     # Project documentation & plan
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/HaxOrWot/MAZESolver.git
cd MAZESolver
pip install -r requirements.txt
```

### 2. Run (Text Mode)
```bash
python src/main.py --maze data/maze_10x10.txt --algo bfs
```

### 3. Run with Visualization
```bash
python src/main.py --maze data/maze_20x20.txt --algo dfs --visual
```

### 4. DLS with Depth Limit
```bash
python src/main.py --maze data/maze_20x20.txt --algo dls --limit 15 --visual
```

### 5. Compare All Algorithms
```bash
python src/main.py --maze data/maze_20x20.txt --compare
```

---

## 🖥️ Visualization Controls

| Key | Action |
|-----|--------|
| `SPACE` | Pause / Resume animation |
| `R` | Restart (re-run algorithm) |
| `S` | Save screenshot to `output/screenshots/` |
| `ESC` | Quit |

---

## 📊 Sample Output

```
Algorithm : BFS
Maze File : data/maze_20x20.txt
──────────────────────────────────
Found      : YES
Path Length: 34 steps
Nodes Exp. : 87
Time Taken : 0.821 ms
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📚 Documentation

See the [`docs/`](docs/) folder for the full project plan:

- [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md) — Master plan & build phases
- [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md) — System design
- [`docs/algorithms/BFS.md`](docs/algorithms/BFS.md) — BFS theory & pseudocode
- [`docs/algorithms/DFS.md`](docs/algorithms/DFS.md) — DFS theory & pseudocode
- [`docs/algorithms/DLS.md`](docs/algorithms/DLS.md) — DLS theory & pseudocode
- [`docs/ui/UI_DESIGN.md`](docs/ui/UI_DESIGN.md) — Pygame UI plan
- [`docs/testing/TEST_PLAN.md`](docs/testing/TEST_PLAN.md) — Test cases

---

## 👤 Author

**HaxOrWot** — College AI Project
