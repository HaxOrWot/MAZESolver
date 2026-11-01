# 🖥️ Split-Screen Comparison View Specification

---

## Overview

The split-screen view renders **3 algorithm animations simultaneously** in a single Pygame window, divided into equal vertical panels. All panels are synchronized — they start, pause, and reset together.

Run with:
```bash
python src/main.py --maze data/maze_20x20.txt --splitview
```

---

## Window Layout

```
╔═══════════════════════╦═══════════════════════╦═══════════════════════╗
║                       ║                       ║                       ║
║    BFS Panel          ║    DFS Panel          ║    DLS Panel          ║
║                       ║                       ║                       ║
║   (animated maze)     ║   (animated maze)     ║   (animated maze)     ║
║                       ║                       ║                       ║
║ Nodes: 87             ║ Nodes: 63             ║ Nodes: 38             ║
║ Status: SOLVED        ║ Status: SOLVED        ║ Status: NO PATH       ║
╠═══════════════════════╩═══════════════════════╩═══════════════════════╣
║  Bottom Stats Bar: BFS: 23 steps | DFS: 31 steps | DLS(L=20): N/A   ║
║  [SPACE] Pause  [R] Restart  [ESC] Quit  [S] Screenshot  [T] Theme  ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## Dimensions

```python
PANEL_COUNT = 3
BOTTOM_BAR_HEIGHT = 80
HEADER_HEIGHT = 30   # algorithm name at top of each panel
CELL_SIZE = max(8, min(25, 550 // max(maze.rows, maze.cols)))

panel_width  = CELL_SIZE * maze.cols
panel_height = CELL_SIZE * maze.rows + HEADER_HEIGHT
window_width = panel_width * PANEL_COUNT + (PANEL_COUNT - 1) * 2  # 2px dividers
window_height = panel_height + BOTTOM_BAR_HEIGHT
```

---

## Synchronization

All 3 panels advance at the same `steps_per_frame`. Since each algorithm explores a different number of nodes, they finish at different times. **The animation continues until ALL panels have finished.**

Finished panels display their final state (solution path highlighted or "NO PATH" overlay) while still-running panels continue animating.

---

## Per-Panel Rendering

Each panel is offset horizontally by `panel_index * (panel_width + 2)`.

All drawing calls use `pygame.Surface.blit()` with an x-offset instead of drawing directly to screen, or alternatively shift all rect x-coordinates by the panel offset.

```python
class SplitPanel:
    def __init__(self, maze, result, algo_name, x_offset, cell_size, theme):
        self.maze = maze
        self.result = result
        self.algo_name = algo_name
        self.x_offset = x_offset
        self.cell_size = cell_size
        self.theme = theme
        self.current_step = 0
        self.status = "SEARCHING"
        self.revealed_visited = set()
        self.path_reveal_step = 0

    def advance(self, steps: int):
        """Advance animation by N steps."""
        if self.status != "SEARCHING":
            return
        if self.current_step < len(self.result["visited"]):
            target = min(len(self.result["visited"]), self.current_step + steps)
            for i in range(self.current_step, target):
                self.revealed_visited.add(self.result["visited"][i])
            self.current_step = target
        else:
            self.status = "SOLVED" if self.result["found"] else "NO PATH"

    def draw(self, screen):
        """Draw this panel's maze grid, header, and mini-stats."""
        self._draw_header(screen)
        self._draw_grid(screen)
        self._draw_mini_stats(screen)

    def _draw_header(self, screen):
        """Algorithm name label at top of panel."""
        ...

    def _draw_grid(self, screen):
        """Draw maze cells with x_offset applied."""
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                pos = (r, c)
                color = self._get_cell_color(pos)
                rect = pygame.Rect(
                    self.x_offset + c * self.cell_size,
                    HEADER_HEIGHT + r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, color, rect)

    def _draw_mini_stats(self, screen):
        """Small stat line below the maze grid."""
        text = f"Nodes: {self.current_step}  |  {self.status}"
        ...
```

---

## Bottom Stats Bar

After all panels finish, the bottom bar shows a full comparison table:

```
  BFS: FOUND  |  Path: 23  |  Explored: 87  |  Time: 0.82ms
  DFS: FOUND  |  Path: 31  |  Explored: 63  |  Time: 0.23ms
  DLS: NO PATH|  Path: --  |  Explored: 38  |  Time: 0.31ms
```

While any panel is still searching, the bottom bar shows:
```
  Searching...  [SPACE] Pause  [R] Restart  [S] Screenshot  [ESC] Quit
```

---

## `SplitRenderer` Class (`src/visualization/split_view.py`)

```python
class SplitRenderer:
    """Renders BFS, DFS, and DLS side-by-side with synchronized animation."""

    def __init__(self, maze, results: dict, theme_name: str = "dark"):
        """
        results = {
            "bfs": bfs_result_dict,
            "dfs": dfs_result_dict,
            "dls": dls_result_dict,
        }
        """
        pygame.init()
        self.maze = maze
        self.theme = get_theme(theme_name)
        
        cell_size = max(8, min(25, 550 // max(maze.rows, maze.cols)))
        panel_w = cell_size * maze.cols
        
        self.panels = [
            SplitPanel(maze, results["bfs"], "BFS",      0,         cell_size, self.theme),
            SplitPanel(maze, results["dfs"], "DFS",      panel_w+2, cell_size, self.theme),
            SplitPanel(maze, results["dls"], "DLS",      panel_w*2+4, cell_size, self.theme),
        ]
        
        window_w = panel_w * 3 + 4
        window_h = cell_size * maze.rows + HEADER_HEIGHT + BOTTOM_BAR_HEIGHT
        self.screen = pygame.display.set_mode((window_w, window_h))
        pygame.display.set_caption("MAZESolver — Split View Comparison")
        
        self.clock = pygame.time.Clock()
        self.is_paused = False
        self.steps_per_frame = 2
        self.is_running = True

    def run(self):
        """Main split-view animation loop."""
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: self.is_running = False
                    elif event.key == pygame.K_SPACE: self.is_paused = not self.is_paused
                    elif event.key == pygame.K_r:
                        for p in self.panels: p.reset()
                    elif event.key == pygame.K_s: self._save_screenshot()

            if not self.is_paused:
                for panel in self.panels:
                    panel.advance(self.steps_per_frame)

            self.screen.fill(self.theme["bg"])
            for panel in self.panels:
                panel.draw(self.screen)
            self._draw_dividers()
            self._draw_bottom_bar()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
```

---

## Integration in `main.py`

```python
if args.splitview:
    from src.algorithms.bfs import BFSSolver
    from src.algorithms.dfs import DFSSolver
    from src.algorithms.dls import DLSSolver
    from src.visualization.split_view import SplitRenderer

    bfs_result = BFSSolver(maze).solve()
    dfs_result = DFSSolver(maze).solve()
    dls_limit = args.limit or (maze.rows + maze.cols)
    dls_result = DLSSolver(maze, limit=dls_limit).solve()

    renderer = SplitRenderer(maze, {
        "bfs": bfs_result,
        "dfs": dfs_result,
        "dls": dls_result,
    }, theme_name=args.theme or "dark")
    renderer.run()
```
