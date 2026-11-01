# 🎨 UI Design Plan — Pygame Visualization

## 1. Window Layout

```
┌──────────────────────────────────────────────────────┬───────────────────────┐
│                                                      │                       │
│                                                      │   MAZESolver          │
│                                                      │   ─────────────────── │
│                                                      │   Algorithm: BFS      │
│                                                      │   Maze: maze_20x20    │
│                                                      │                       │
│                                                      │   ─────────────────── │
│                  MAZE GRID                           │   Status:             │
│              (auto-scaling cells)                    │   🔵 SEARCHING        │
│                                                      │                       │
│                                                      │   ─────────────────── │
│                                                      │   Nodes Explored:     │
│                                                      │        47             │
│                                                      │                       │
│                                                      │   Path Length:        │
│                                                      │        --             │
│                                                      │                       │
│                                                      │   Time Taken:         │
│                                                      │      0.0004s          │
│                                                      │                       │
│                                                      │   ─────────────────── │
│                                                      │   [SPACE] Pause       │
│                                                      │   [R]     Reset       │
│                                                      │   [S]     Screenshot  │
│                                                      │   [ESC]   Quit        │
└──────────────────────────────────────────────────────┴───────────────────────┘
   ← MAZE_AREA_WIDTH (auto) →                           ← HUD_WIDTH: 250px →
```

---

## 2. Color Palette

All colors defined in `src/visualization/colors.py`:

```python
# Background
BG_COLOR        = (30,  30,  30)   # Dark gray background

# Cell types
WALL_COLOR      = (44,  44,  44)   # #2C2C2C — very dark gray
OPEN_COLOR      = (240, 240, 240)  # #F0F0F0 — near-white
START_COLOR     = (0,   200,  83)  # #00C853 — bright green
GOAL_COLOR      = (213,  0,   0)   # #D50000 — bright red

# Algorithm animation
VISITED_COLOR   = (129, 212, 250)  # #81D4FA — light blue
PATH_COLOR      = (255, 214,  0)   # #FFD600 — bright yellow
FRONTIER_COLOR  = (255, 109,  0)   # #FF6D00 — orange (current cell)

# HUD
HUD_BG          = (20,  20,  20)   # Near-black panel
HUD_TEXT        = (220, 220, 220)  # Light gray text
HUD_ACCENT      = (100, 181, 246)  # #64B5F6 — blue accent
HUD_DIVIDER     = (60,  60,  60)   # Subtle divider line
HUD_SUCCESS     = (0,   200,  83)  # Green for SOLVED
HUD_FAIL        = (213,  0,   0)   # Red for NO PATH
HUD_SEARCHING   = (255, 214,  0)   # Yellow for SEARCHING

# Grid border
BORDER_COLOR    = (80,  80,  80)   # Cell border lines
```

---

## 3. Cell Rendering Rules

Each cell is drawn as a filled rectangle with a 1px border:

```
Priority (highest wins):
  1. START cell        → always green (regardless of visited/path state)
  2. GOAL cell         → always red   (regardless of visited/path state)
  3. WALL cell         → dark gray
  4. PATH cell         → yellow (shown only after search completes)
  5. VISITED cell      → light blue (shown during animation)
  6. OPEN cell         → white (unvisited open path)
```

---

## 4. Cell Size Auto-Scaling

```python
WINDOW_MAX_SIZE = 700   # max pixels for the maze area
CELL_SIZE = max(10, min(40, WINDOW_MAX_SIZE // max(maze.rows, maze.cols)))

# Examples:
# 5×5 maze   → CELL_SIZE = 40px → maze area = 200×200
# 10×10 maze → CELL_SIZE = 40px → maze area = 400×400
# 20×20 maze → CELL_SIZE = 35px → maze area = 700×700
# 30×30 maze → CELL_SIZE = 23px → maze area = 690×690
```

Total window size:
```python
WINDOW_W = maze.cols * CELL_SIZE + HUD_WIDTH   # (+ 250 for HUD)
WINDOW_H = maze.rows * CELL_SIZE
```

---

## 5. Animation Speed

```python
ANIMATION_FPS     = 60      # Pygame clock target FPS
STEPS_PER_FRAME   = 1       # How many visited cells to reveal per frame
                             # Set higher (e.g., 5) for large mazes to speed up
```

Controls:
- `SPACE` — toggle pause
- `↑ / ↓` arrows — increase/decrease `STEPS_PER_FRAME` (optional enhancement)

---

## 6. HUD Panel Sections

### Header
```
┌─────────────────────────────┐
│     🧩 MAZESolver           │  ← Title, white bold 22px
│  ─────────────────────────  │
│  Algorithm: BFS             │  ← Algorithm name, accent color
│  Maze: maze_20x20.txt       │  ← Maze filename
└─────────────────────────────┘
```

### Status Badge
```
┌─────────────────────────────┐
│  Status:                    │
│  ● SEARCHING                │  ← Yellow dot + text while animating
│  ● SOLVED                   │  ← Green dot + text when path drawn
│  ● NO PATH                  │  ← Red dot when no solution
└─────────────────────────────┘
```

### Stats
```
┌─────────────────────────────┐
│  Nodes Explored:            │
│          87                 │  ← Updates live during animation (large font)
│                             │
│  Path Length:               │
│          34                 │  ← Shows "--" until solved
│                             │
│  Time Taken:                │
│       0.821 ms              │  ← Shows immediately (computed before render)
└─────────────────────────────┘
```

### Controls Legend
```
┌─────────────────────────────┐
│  [SPACE]  Pause / Resume    │
│  [R]      Restart           │
│  [S]      Screenshot        │
│  [ESC]    Quit              │
└─────────────────────────────┘
```

---

## 7. Screenshot Naming Convention

```python
# Format: {algo}_{mazename}_{timestamp}.png
# Example:
"output/screenshots/bfs_maze20x20_20261101_175512.png"
"output/screenshots/dfs_maze10x10_20261101_175543.png"
"output/screenshots/dls_L15_maze30x30_20261101_175601.png"
```

---

## 8. Pygame Font Recommendations

```python
pygame.font.SysFont("Consolas", 14)   # HUD stats (monospace for alignment)
pygame.font.SysFont("Consolas", 22)   # HUD title
pygame.font.SysFont("Consolas", 11)   # HUD controls legend
```

Fall back to `pygame.font.Font(None, size)` if Consolas isn't available.

---

## 9. States Machine

```
State: IDLE
  │  (animation starts immediately on window open)
  ▼
State: ANIMATING
  │  SPACE pressed → State: PAUSED
  │  All visited shown + path drawn → State: SOLVED / NO_PATH
  ▼
State: PAUSED
  │  SPACE pressed → State: ANIMATING
  ▼
State: SOLVED / NO_PATH
  │  R pressed → re-run solver → State: ANIMATING
  │  S pressed → save screenshot → stay in SOLVED
  │  ESC pressed → quit
```
