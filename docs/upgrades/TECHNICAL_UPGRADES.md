# ⚙️ Technical Upgrades Specification — MAZESolver v2.0

---

## 1. `config.json` — Centralized Configuration

Create `config.json` at the project root. The renderer and CLI load this on startup.

```json
{
  "theme": "dark",
  "animation_fps": 60,
  "steps_per_frame": 3,
  "sound_enabled": true,
  "sound_volume": 0.3,
  "cell_size_override": null,
  "hud_width": 280,
  "hud_default_tab": 1,
  "gif_fps": 15,
  "gif_skip_frames": 3,
  "default_dls_limit_multiplier": 1.5,
  "particle_count": 40,
  "particle_gravity": 0.15,
  "glow_radius": 3,
  "fade_frames": 8
}
```

A `Config` class at `src/config.py`:
```python
import json, os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

class Config:
    _instance = None

    def __init__(self):
        with open(CONFIG_PATH, "r") as f:
            self._data = json.load(f)

    @classmethod
    def get(cls) -> "Config":
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    def __getattr__(self, key):
        return self._data.get(key)

    def save(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self._data, f, indent=2)

    def set(self, key, value):
        self._data[key] = value
```

---

## 2. IDDFS — Iterative Deepening DFS (`src/algorithms/iddfs.py`)

### Theory
IDDFS runs DLS repeatedly with depth limit L = 0, 1, 2, 3, ... until the goal is found. It combines:
- BFS's **optimality** (finds shortest path)
- DFS's **memory efficiency** (O(depth) space)

It is technically superior to plain DFS for finding optimal paths.

### Implementation Spec

```python
class IDDFSSolver(BaseSolver):
    def solve(self) -> dict:
        """
        Runs DLS with L=0, L=1, L=2, ... until goal found.
        
        The result's 'visited' must include ALL nodes explored across ALL iterations
        (so the animation shows multiple waves of DLS attempts before success).
        
        The result dict must include:
            "iterations": int  — how many DLS iterations were needed
        
        Time complexity: O(b^d) where b=branching factor, d=solution depth
        Space complexity: O(d)
        """
        all_visited = []
        iteration = 0

        while True:
            found, path, visited_this_iter = self._dls_iteration(
                self.maze.start, self.maze.goal, iteration
            )
            all_visited.extend(visited_this_iter)
            if found:
                return {
                    "path": path,
                    "visited": all_visited,
                    "nodes_explored": len(all_visited),
                    "path_length": len(path),
                    "time_taken": ...,
                    "found": True,
                    "iterations": iteration + 1,
                }
            iteration += 1
            if iteration > self.maze.rows * self.maze.cols:
                # Safety cap: maze is unsolvable
                return {"found": False, ...}

    def _dls_iteration(self, start, goal, limit):
        """Single DLS pass, returns (found, path, visited_order)."""
        # Standard DLS logic here (same as DLSSolver.solve() internals)
        ...
```

### Key rule: The `visited` list for IDDFS animation must show all exploration attempts (including failed ones from earlier iterations). This is what makes IDDFS visually fascinating — you see it trying multiple times with increasing depth before succeeding.

---

## 3. A\* Solver (`src/algorithms/astar.py`) — Bonus

### Theory
A\* is an **informed search** — it uses a heuristic `h(n)` to guide the search toward the goal. For grid mazes, Manhattan distance is the perfect heuristic.

```
f(n) = g(n) + h(n)
  g(n) = exact cost from start to n (depth)
  h(n) = Manhattan distance from n to goal
  f(n) = estimated total path cost through n
```

A\* always expands the node with lowest `f(n)` first (using a min-heap/priority queue).

### Why Include It?
Including A\* alongside BFS/DFS/DLS lets you demonstrate the **power of heuristics**:
- On a 30×30 maze: BFS explores ~400 nodes, A\* explores ~80 nodes
- The split-view showing BFS vs A\* side-by-side is visually dramatic

### Implementation Spec
```python
import heapq

class AStarSolver(BaseSolver):
    def heuristic(self, pos):
        """Manhattan distance to goal."""
        return abs(pos[0] - self.maze.goal[0]) + abs(pos[1] - self.maze.goal[1])

    def solve(self):
        # Priority queue: (f_cost, tie_breaker, node)
        # tie_breaker is an incrementing counter to break equal f_cost ties
        heap = []
        start_node = Node(self.maze.start, parent=None, depth=0)
        h = self.heuristic(self.maze.start)
        heapq.heappush(heap, (h, 0, start_node))
        
        visited = set()
        visited_order = []
        counter = 0

        while heap:
            f, _, current = heapq.heappop(heap)

            if current.position in visited:
                continue
            visited.add(current.position)
            visited_order.append(current.position)

            if current.position == self.maze.goal:
                path = current.get_path()
                return {"path": path, "visited": visited_order, ...}

            for neighbor in self.maze.get_neighbors(current.position):
                if neighbor not in visited:
                    counter += 1
                    child = Node(neighbor, parent=current, depth=current.depth + 1)
                    g = child.depth
                    h = self.heuristic(neighbor)
                    heapq.heappush(heap, (g + h, counter, child))
        
        return {"found": False, ...}
```

### CLI: `--algo astar`
Add `astar` to the `--algo` choices in `main.py`. Include in `--compare` mode.

---

## 4. Solver Frontier Snapshots (Inspector Support)

Modify each solver to also record frontier state snapshots for the HUD Inspector Tab.

Add to each solver's internal loop:
```python
frontier_snapshot = [n.position for n in list(queue)][:8]  # top 8
self.frontier_history.append(frontier_snapshot)
```

Add instance variable: `self.frontier_history: List[List[Tuple]] = []`

The result dict gains:
```python
"frontier_history": List[List[Tuple]]  # one snapshot per visited step
```

The renderer indexes into this at `current_step` to display in Inspector tab.

---

## 5. Updated `main.py` — New CLI Flags

Add these new flags to `argparse`:

```
--algo       : bfs | dfs | dls | iddfs | astar (existing + new)
--splitview  : open side-by-side 3-panel comparison window
--export-gif : run headless and export animated GIF
--theme      : dark | neon | retro | light (overrides config.json)
--generate   : generate a random maze before solving (size from --maze-size)
--maze-size  : N (integer, for --generate flag)
--gen-algo   : recursive_backtrack | prims | wilsons (maze generator algorithm)
--edit       : open the interactive maze editor
```

### New Full Command Examples
```bash
# Open editor
python src/main.py --edit

# Generate a 25x25 maze then solve with BFS visually
python src/main.py --generate --maze-size 25 --algo bfs --visual

# Split-screen comparison on generated maze
python src/main.py --generate --maze-size 20 --splitview

# Run BFS and export GIF
python src/main.py --maze data/maze_20x20.txt --algo bfs --export-gif

# Full comparison with A* included
python src/main.py --maze data/maze_20x20.txt --compare

# Use neon theme
python src/main.py --maze data/maze_20x20.txt --algo dfs --visual --theme neon
```

---

## 6. Sound System (`src/visualization/sound_manager.py`)

```python
import pygame
import os

class SoundManager:
    def __init__(self, enabled: bool = True, volume: float = 0.3):
        self.enabled = enabled
        if enabled:
            pygame.mixer.init()
        self._load_sounds()
        self.set_volume(volume)

    def _load_sounds(self):
        assets = os.path.join(os.path.dirname(...), "assets", "sounds")
        try:
            self.tick  = pygame.mixer.Sound(os.path.join(assets, "tick.wav"))
            self.goal  = pygame.mixer.Sound(os.path.join(assets, "goal.wav"))
        except:
            self.tick = self.goal = None

    def set_volume(self, v: float):
        if self.tick: self.tick.set_volume(v)
        if self.goal: self.goal.set_volume(v * 3)

    def play_tick(self):
        if self.enabled and self.tick:
            self.tick.play()

    def play_goal(self):
        if self.enabled and self.goal:
            self.goal.play()

    def toggle_mute(self):
        self.enabled = not self.enabled
```

**Sound Files:** Generate minimal WAV files using Python's `wave` module as a fallback (no external audio files required). These are simple 440Hz sine wave beeps, very small in file size.

---

## 7. GIF Export (`src/visualization/gif_exporter.py`)

```python
from PIL import Image
import pygame
import io

class GIFExporter:
    def __init__(self, skip_frames: int = 3, fps: int = 15):
        self.frames = []
        self.skip_frames = skip_frames
        self.frame_count = 0
        self.fps = fps

    def capture(self, screen: pygame.Surface):
        """Call every frame. Only saves every Nth frame."""
        if self.frame_count % self.skip_frames == 0:
            # Convert pygame surface to PIL Image
            raw = pygame.image.tostring(screen, "RGB")
            size = screen.get_size()
            img = Image.frombytes("RGB", size, raw)
            self.frames.append(img)
        self.frame_count += 1

    def export(self, filepath: str):
        """Write captured frames as animated GIF."""
        if not self.frames:
            return
        duration = int(1000 / self.fps)  # ms per frame
        self.frames[0].save(
            filepath,
            save_all=True,
            append_images=self.frames[1:],
            duration=duration,
            loop=0,
            optimize=True,
        )
        print(f"[GIF] Exported {len(self.frames)} frames → {filepath}")
```

When `--export-gif` is passed, the renderer captures every Nth frame. On quit (or when solve completes), calls `exporter.export(...)`.

---

## 8. Updated Test Suite

Add these new test files:

### `tests/test_iddfs.py`
- Finds shortest path (optimal like BFS)
- `iterations` key present in result
- Visits all expected cells across iterations
- No path case returns `found=False`

### `tests/test_astar.py`
- Finds shortest path (optimal)
- Explores fewer nodes than BFS on open mazes
- `h(goal) == 0` (heuristic is 0 at goal)
- `h(n) >= 0` for all n (admissible)

### `tests/test_generator.py`
- Generated maze is rectangular
- Has exactly one `S` and one `G`
- BFS can solve it (`found=True`)
- Outer border is all walls

### `tests/test_config.py`
- Config loads without error
- All required keys present
- `save()` + reload preserves values
