# 🚀 MAZESolver — Upgrade Master Plan

> This document replaces and supersedes `PROJECT_PLAN.md` as the governing build blueprint.
> The existing codebase is a valid foundation. **Do NOT delete or rewrite it** — only extend and enhance it.

---

## 📊 Before vs After

| Dimension | Current (v1.0) | Upgraded (v2.0) |
|-----------|----------------|-----------------|
| Algorithms | BFS, DFS, DLS | BFS, DFS, DLS, IDDFS, **A\*** (bonus) |
| Mazes | 4 hand-crafted .txt files | Procedural generator (4 algorithms) + interactive editor |
| Visualization | Static flat colored cells | Animated cells with glow, gradient heatmap, particle burst on goal |
| HUD | Text stats panel | Multi-tab panel: Stats, Queue/Stack inspector, Algorithm explainer |
| Animation | Flat speed control | Smooth lerp, per-cell fade-in, configurable via slider UI |
| Comparison | CLI table only | **Split-screen side-by-side live Pygame comparison** |
| Themes | One dark theme | Dark, Neon, Retro CRT, Minimal Light — switchable with `T` |
| Audio | None | Subtle sound effects (exploration tick, goal fanfare) |
| Export | PNG screenshot | PNG screenshot + **animated GIF export** of full solve |
| Config | Hardcoded values | `config.json` loaded at startup — all tweakables externalized |
| Tests | 33 unit tests | 33 existing + tests for generator, IDDFS, A\*, themes, GIF export |

---

## 🗂️ New Folder Structure (additions only — existing files stay)

```
MAZESolver/
│
├── src/
│   ├── algorithms/
│   │   ├── iddfs.py              ← NEW: Iterative Deepening DFS
│   │   └── astar.py              ← NEW: A* (bonus — shows informed vs uninformed gap)
│   │
│   ├── generator/                ← NEW: Procedural maze generation
│   │   ├── __init__.py
│   │   ├── base_generator.py     ← Abstract base
│   │   ├── recursive_backtrack.py ← Most visually interesting maze structure
│   │   ├── prims.py              ← Prim's algorithm mazes (more open)
│   │   └── generator_cli.py      ← Standalone: python -m src.generator --size 30 --algo prims
│   │
│   ├── editor/                   ← NEW: Interactive Pygame maze editor
│   │   ├── __init__.py
│   │   └── maze_editor.py        ← Click to toggle walls, place S/G, save .txt
│   │
│   └── visualization/
│       ├── colors.py             ← EXTEND: add theme system
│       ├── themes.py             ← NEW: DARK, NEON, RETRO, LIGHT theme dicts
│       ├── hud.py                ← REWRITE: tabbed HUD (Stats / Inspector / Explain)
│       ├── renderer.py           ← REWRITE: smooth animation, glow, gradient heatmap
│       ├── particles.py          ← NEW: Particle system for goal-reached effect
│       ├── split_view.py         ← NEW: Side-by-side dual/triple algorithm renderer
│       └── gif_exporter.py       ← NEW: Captures frames → outputs animated GIF
│
├── config.json                   ← NEW: All runtime settings
├── assets/
│   └── sounds/
│       ├── tick.wav              ← Cell explored sound
│       └── goal.wav              ← Goal reached fanfare
│
├── data/
│   └── generated/                ← Auto-generated mazes land here
│
├── output/
│   ├── screenshots/              ← Existing
│   └── gifs/                     ← NEW: Animated GIF exports
│
└── docs/
    ├── UPGRADE_MASTER_PLAN.md    ← THIS FILE
    ├── upgrades/
    │   ├── VISUAL_UPGRADES.md    ← Visual feature specs
    │   ├── TECHNICAL_UPGRADES.md ← Algorithm & architecture specs
    │   ├── GENERATOR.md          ← Maze generator deep-dive
    │   ├── EDITOR.md             ← Maze editor spec
    │   └── SPLIT_VIEW.md         ← Side-by-side comparison spec
    └── [all existing docs stay]
```

---

## 🔢 Build Phases

### Phase A — Config & Theme Foundation (Do First)
> Everything else depends on this.

- Create `config.json` — centralizes all previously hardcoded values
- Create `src/visualization/themes.py` — 4 complete color theme dicts
- Extend `src/visualization/colors.py` — add `get_theme(name)` loader

### Phase B — Visual Engine Overhaul
> Upgrade renderer.py and hud.py. Most impactful change.

1. **Smooth cell animation** — each newly revealed cell fades from `WALL_COLOR` → `VISITED_COLOR` over 8 frames using alpha lerp (not instant snap)
2. **Heatmap gradient** — visited cells colored on a Blue→Red gradient based on exploration order index (earliest = cool blue, latest = warm orange). Shows the "wave" of BFS vs the "spike" of DFS beautifully
3. **Glow effect** — current frontier cell gets a 3px soft glow ring around it (draw larger rect behind in semi-transparent color before main cell)
4. **Path animation** — solution path drawn cell-by-cell with a traveling highlight, not all at once
5. **Particle burst** — when goal cell is reached, emit 30–40 small square particles in goal color that drift outward with gravity and fade out over 60 frames
6. **Start/Goal pulse** — start and goal cells gently pulse (size ±2px oscillating via `sin(time)`)
7. **Rewrite HUD** — tabbed HUD with 3 tabs: `[1] Stats` `[2] Inspector` `[3] Explain`
   - Tab 1 (Stats): existing stat display, now with a live bar chart comparing BFS/DFS/DLS nodes explored if `--compare` mode was run
   - Tab 2 (Inspector): live display of current Queue/Stack contents (top 8 items) — shows WHY BFS and DFS explore differently
   - Tab 3 (Explain): scrollable plain-English explanation of the current algorithm step

### Phase C — New Algorithms
1. **IDDFS** (`src/algorithms/iddfs.py`) — iterative deepening: run DLS with L=0, then L=1, L=2... until found. Optimal like BFS but O(d) memory like DFS. Must return full history of all iterations for animation.
2. **A\*** (`src/algorithms/astar.py`) — bonus algorithm using Manhattan distance heuristic. Allows dramatic visual comparison: show BFS exploring in a ring, A\* going straight to goal. `--algo astar` flag.

### Phase D — Procedural Maze Generator
- `python src/generator/generator_cli.py --size 25 --algo recursive_backtrack --output data/generated/`
- Generates valid, solvable mazes with guaranteed path from S to G
- Three generation algorithms: Recursive Backtrack (winding), Prim's (branchy), Wilson's (unbiased)
- `--size` takes a single int (generates N×N maze)
- `--difficulty` flag: `easy` (many open paths), `hard` (fewer paths)

### Phase E — Interactive Maze Editor
- `python src/editor/maze_editor.py` — opens Pygame editor window
- Left-click: toggle wall on/off
- Right-click: place Start (S) or Goal (G) via popup menu
- `Ctrl+S`: save maze as .txt to `data/` (prompts for filename)
- `Ctrl+G`: generate random maze using Phase D generator
- `Ctrl+R`: run BFS instantly on current maze and display solution path
- Resize maze via `+` / `-` keys (adds/removes row/col from edge)
- Clear all: `Ctrl+C`

### Phase F — Split-Screen Comparison View
- `python src/main.py --maze data/maze_20x20.txt --splitview`
- Opens a single Pygame window divided into 3 equal panels
- Each panel runs a different algorithm's animation **simultaneously and in sync**
- All three start, pause, and reset together
- Bottom bar shows live comparison stats for all 3
- This is the most impressive visual demo feature

### Phase G — Animated GIF Export
- `python src/main.py --maze data/maze_20x20.txt --algo bfs --export-gif`
- Runs algorithm headlessly, captures every Nth frame into a list
- Uses `Pillow` to encode frames into an animated GIF
- Output: `output/gifs/bfs_maze20x20_<timestamp>.gif`
- GIF plays at ~15fps, loops forever

### Phase H — Sound Effects (Optional but impactful)
- `pip install pygame` already handles audio
- On each cell explored: play `assets/sounds/tick.wav` (very short, low volume)
- On goal found: play `assets/sounds/goal.wav` (success chime, ~1 second)
- Mute toggle: `M` key
- Sound volume in `config.json`

### Phase I — Tests & Documentation
- New tests for: generator (solvability), IDDFS (optimality), A\* (optimality + heuristic admissibility), GIF export (file created)
- Update README.md with GIF showcase, new commands, theme screenshots
- Add `report/REPORT.md` filled in with academic analysis

---

## ⚡ Priority Order for Maximum Impact

If time is limited, build in this order — each phase is independently shippable:

1. **Phase B** (Visual Engine) — biggest "wow factor" change, purely visual
2. **Phase F** (Split View) — most impressive demo feature
3. **Phase D** (Generator) — enables infinite new mazes
4. **Phase C** (IDDFS + A\*) — academic depth
5. **Phase E** (Editor) — quality of life
6. **Phase G** (GIF Export) — shareability
7. **Phase A** (Config/Themes) — polish
8. **Phase H** (Sound) — cherry on top

---

## 🔧 New Dependencies

Add to `requirements.txt`:
```
pygame>=2.5.0
pytest>=7.4.0
colorama>=0.4.6
pytest-cov>=4.1.0
Pillow>=10.0.0        # GIF export
numpy>=1.24.0          # Efficient grid operations in generator
```
