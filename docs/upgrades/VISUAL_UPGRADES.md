# 🎨 Visual Upgrades Specification — MAZESolver v2.0

> This document fully specifies every visual change required in Phase B of the upgrade plan.
> The implementing AI must read this **entire document** before touching any visualization file.

---

## 1. Theme System (`src/visualization/themes.py`)

Create a new file `src/visualization/themes.py`. A theme is a Python dict of color keys.

**All renderer and HUD code must reference theme colors through `THEME["KEY"]` — never hardcode RGB tuples.**

### Theme Dict Shape
```python
THEMES = {
    "dark": {
        # Grid
        "bg":           (18,  18,  18),
        "wall":         (40,  40,  40),
        "open":         (230, 230, 230),
        "start":        (0,   200,  83),
        "goal":         (213,  0,   0),
        # Algorithm animation
        "visited_cold": (30,  100, 200),   # start of heatmap
        "visited_hot":  (255, 100,   0),   # end of heatmap
        "path":         (255, 214,   0),
        "frontier":     (255, 100,   0),
        "glow":         (255, 214,   0),
        # HUD
        "hud_bg":       (12,  12,  12),
        "hud_text":     (210, 210, 210),
        "hud_accent":   (100, 181, 246),
        "hud_divider":  (50,  50,  50),
        "hud_success":  (0,   200,  83),
        "hud_fail":     (213,  0,   0),
        "hud_searching":(255, 214,   0),
        # Grid lines
        "border":       (60,  60,  60),
    },
    "neon": {
        "bg":           (5,    5,  15),
        "wall":         (20,  20,  40),
        "open":         (15,  15,  35),
        "start":        (0,  255, 150),
        "goal":         (255,  0, 100),
        "visited_cold": (0,  120, 255),
        "visited_hot":  (200,   0, 255),
        "path":         (0,  255, 200),
        "frontier":     (255, 255,   0),
        "glow":         (100,   0, 255),
        "hud_bg":       (3,    3,  10),
        "hud_text":     (200, 200, 255),
        "hud_accent":   (0,  255, 200),
        "hud_divider":  (30,  30,  70),
        "hud_success":  (0,  255, 150),
        "hud_fail":     (255,  0, 100),
        "hud_searching":(255, 255,   0),
        "border":       (40,  40, 100),
    },
    "retro": {
        "bg":           (10,  20,   5),
        "wall":         (0,   60,   0),
        "open":         (0,  180,   0),
        "start":        (255, 255,   0),
        "goal":         (255,  80,   0),
        "visited_cold": (0,  100,   0),
        "visited_hot":  (100, 255,   0),
        "path":         (255, 200,   0),
        "frontier":     (200, 255,   0),
        "glow":         (0,  255,   0),
        "hud_bg":       (5,   10,   3),
        "hud_text":     (0,  200,   0),
        "hud_accent":   (0,  255,   0),
        "hud_divider":  (0,   50,   0),
        "hud_success":  (0,  255,   0),
        "hud_fail":     (255,  80,   0),
        "hud_searching":(100, 255,   0),
        "border":       (0,   80,   0),
    },
    "light": {
        "bg":           (245, 245, 245),
        "wall":         (60,  60,  60),
        "open":         (255, 255, 255),
        "start":        (0,  150,  60),
        "goal":         (180,  0,   0),
        "visited_cold": (150, 200, 255),
        "visited_hot":  (255, 150,  80),
        "path":         (255, 200,   0),
        "frontier":     (255, 120,   0),
        "glow":         (255, 200,   0),
        "hud_bg":       (235, 235, 235),
        "hud_text":     (30,  30,  30),
        "hud_accent":   (30,  100, 200),
        "hud_divider":  (200, 200, 200),
        "hud_success":  (0,  150,  60),
        "hud_fail":     (180,  0,   0),
        "hud_searching":(200, 120,   0),
        "border":       (180, 180, 180),
    },
}

THEME_ORDER = ["dark", "neon", "retro", "light"]

def get_theme(name: str) -> dict:
    return THEMES.get(name, THEMES["dark"])

def next_theme(current: str) -> str:
    idx = THEME_ORDER.index(current) if current in THEME_ORDER else 0
    return THEME_ORDER[(idx + 1) % len(THEME_ORDER)]
```

---

## 2. Heatmap Gradient for Visited Cells

Replace the single flat `VISITED_COLOR` with a smooth gradient based on exploration order.

```python
def heatmap_color(index: int, total: int, theme: dict) -> tuple:
    """
    Interpolates between visited_cold and visited_hot based on position in sequence.
    index=0 → cold color, index=total-1 → hot color
    """
    if total <= 1:
        return theme["visited_cold"]
    t = index / (total - 1)       # 0.0 to 1.0
    cold = theme["visited_cold"]
    hot  = theme["visited_hot"]
    r = int(cold[0] + (hot[0] - cold[0]) * t)
    g = int(cold[1] + (hot[1] - cold[1]) * t)
    b = int(cold[2] + (hot[2] - cold[2]) * t)
    return (r, g, b)
```

**Effect:**
- BFS: smooth expanding ring from blue center → orange edge (beautiful circular gradient)
- DFS: deep orange spike going one direction, cold blue everywhere else (shows depth-first nature)
- DLS: visible cutoff where the hot gradient stops abruptly at depth limit

---

## 3. Cell Fade-In Animation

Instead of cells snapping instantly to `VISITED_COLOR`, each newly revealed cell fades in over 8 frames.

**Implementation strategy:**
- Maintain a dict: `cell_alpha: Dict[Tuple, int]` where value goes from 0 → 255
- Each frame, increment alpha by `255 // 8 = 32` for cells being revealed
- Blend: `lerp_color(from_color, to_color, alpha/255)` where lerp_color does per-channel linear interpolation
- Cells at full alpha render as heatmap color; cells mid-fade render as `lerp(open_color, heatmap_color, t)`

---

## 4. Glow Effect on Frontier Cell

The current frontier (most-recently-popped) cell gets a soft glow ring:

```python
def draw_glow(screen, pos, cell_size, glow_color, radius=3):
    """Draw a larger semi-transparent rect behind the cell for glow."""
    r, c = pos
    glow_surf = pygame.Surface((cell_size + radius*2, cell_size + radius*2), pygame.SRCALPHA)
    glow_surf.fill((0, 0, 0, 0))
    inner_rect = pygame.Rect(radius, radius, cell_size, cell_size)
    pygame.draw.rect(glow_surf, (*glow_color, 120), inner_rect, border_radius=3)
    # Blur effect by drawing multiple overlapping rects with decreasing alpha
    for i in range(1, radius+1):
        expanded = pygame.Rect(radius - i, radius - i, cell_size + i*2, cell_size + i*2)
        pygame.draw.rect(glow_surf, (*glow_color, 40 // (i+1)), expanded, border_radius=3+i)
    screen.blit(glow_surf, (c * cell_size - radius, r * cell_size - radius))
```

---

## 5. Traveling Path Animation

When solution is found, don't draw the entire path at once. Instead:
- Maintain `path_reveal_step: int` (0 → len(path))
- Each frame after solving, increment `path_reveal_step` by 1
- Only draw path cells up to `path_reveal_step`
- The leading edge of the path has a bright "pulse" (lighter color)
- Full status changes to "SOLVED" only after `path_reveal_step == len(path)`

---

## 6. Particle Burst on Goal

When `path_reveal_step` reaches `goal` position, spawn particles:

```python
class Particle:
    def __init__(self, x: float, y: float, color: tuple):
        self.x = x
        self.y = y
        import random, math
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 1.0          # 1.0 → 0.0
        self.decay = random.uniform(0.02, 0.04)
        self.size = random.randint(3, 6)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15           # gravity
        self.life -= self.decay
        self.size = max(1, self.size - 0.05)

    @property
    def is_alive(self): return self.life > 0

    def draw(self, screen):
        alpha = int(self.life * 255)
        color = (*self.color[:3], alpha)
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, self.size*2, self.size*2))
        screen.blit(surf, (self.x - self.size, self.y - self.size))
```

Spawn 40 particles at the goal cell's pixel center when path animation reaches it. Update and draw all alive particles every frame.

---

## 7. Start / Goal Pulsing

```python
import math, pygame

def get_pulse_size(base_size: int, time_ms: int, amplitude=2, frequency=0.003) -> int:
    """Returns a cell size that oscillates ±amplitude pixels."""
    return base_size + int(math.sin(time_ms * frequency) * amplitude)
```

Use `pygame.time.get_ticks()` as `time_ms`. Draw start and goal cells slightly larger/smaller on each frame. Center the rect within the cell to avoid layout shift.

---

## 8. Tabbed HUD

Redesign `src/visualization/hud.py` completely.

### Tab System
The HUD has 3 tabs. Press keys `1`, `2`, `3` to switch tabs (or click tab headers if mouse events are handled).

```
┌──────────────────────────┐
│  [1] Stats [2] Insp [3]? │  ← Tab bar
├──────────────────────────┤
│  (tab content below)     │
│                          │
└──────────────────────────┘
```

### Tab 1: Stats (existing + enhancements)
- Algorithm name, maze file, status badge (same as before)
- Nodes explored, path length, time taken
- NEW: A small horizontal bar showing nodes explored relative to total maze cells
  - `(nodes_explored / (maze.rows * maze.cols)) * (HUD_WIDTH - 40)` pixels wide
  - Labeled "Coverage: 47%"

### Tab 2: Inspector
Shows live algorithm internals.
- Header: "Queue Contents" (BFS) or "Stack Contents" (DFS/DLS)
- Lists top 8 items from the current frontier (positions as `(r,c)`)
- Shows current depth of frontier head
- Shows `visited` count vs `frontier` count
- For DLS: shows current depth limit and depth of current node

> **Implementation note:** The solvers in `src/algorithms/` must be modified to yield snapshots.
> The cleanest approach: add `get_inspector_data() -> dict` to each solver class that returns the current frontier state. The renderer calls this once per frame during animation.
>
> Since the current design pre-computes the full result before rendering, the inspector must store a "history" of frontier states. Modify each `solve()` method to also record `frontier_snapshots: list[list[tuple]]` — one snapshot per exploration step. This increases memory slightly but enables the inspector.

### Tab 3: Explainer
Scrollable text panel. For each algorithm shows:
- What the algorithm does in plain English (2–3 sentences)
- Why the current cell was chosen (FIFO/LIFO rule)
- What will happen next
- The current step count and what it means

Pre-written static explanations per algorithm (not dynamic). Scroll with `↑↓` when on this tab.

---

## 9. Animation Speed Slider

Replace the arrow key speed control with a visual slider rendered in the HUD.

```
Speed: [━━━━━━━━━━━━━━━●──────]  Fast
        slow                fast
```

- Mouse click/drag on the slider bar to set speed
- `←/→` arrow keys still work (increment/decrement by 1)
- Current `steps_per_frame` shown as label

---

## 10. Theme Switching

Key `T` cycles through themes: Dark → Neon → Retro → Light → Dark...

- Current theme name shown in HUD footer
- All colors update instantly on next frame
- Theme preference saved to `config.json` on exit

---

## 11. Keyboard Reference (Complete Updated List)

| Key | Action |
|-----|--------|
| `SPACE` | Pause / Resume |
| `R` | Restart animation |
| `S` | Save PNG screenshot |
| `G` | Export animated GIF (of current solve) |
| `T` | Cycle theme |
| `M` | Toggle sound mute |
| `1` | HUD: Stats tab |
| `2` | HUD: Inspector tab |
| `3` | HUD: Explainer tab |
| `←/→` | Decrease/increase animation speed |
| `ESC` | Quit |
