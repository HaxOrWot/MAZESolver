# ✏️ Interactive Maze Editor Specification (`src/editor/maze_editor.py`)

---

## Overview

The maze editor is a standalone Pygame application that lets the user:
- Draw and erase walls with mouse clicks
- Place Start and Goal markers
- Resize the grid
- Generate a random maze
- Save the maze to a `.txt` file
- Immediately run a solver to preview the solution

Run with:
```bash
python src/main.py --edit
```

---

## Window Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  TOOLBAR (top 50px)                                                │
│  [New] [Open] [Save] [Generate] [Solve▼ BFS] [Clear]  Theme: Dark │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                                                                    │
│              GRID CANVAS                                           │
│            (cells are 24px each)                                   │
│            Click: toggle wall                                      │
│            Right-click: place S or G                               │
│                                                                    │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│  STATUS BAR (bottom 30px):  Grid: 25×25 | Tool: Wall Toggle | ... │
└────────────────────────────────────────────────────────────────────┘
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+S` | Save maze as .txt (uses dialog or prompts for filename in console) |
| `Ctrl+N` | New empty maze (prompts for rows×cols) |
| `Ctrl+O` | Open existing .txt file |
| `Ctrl+G` | Generate random maze (replaces current) |
| `Ctrl+C` | Clear all walls (make everything open except border) |
| `Ctrl+Z` | Undo last action (stack of up to 20 states) |
| `1` | Switch tool to: Wall Toggle |
| `2` | Switch tool to: Place Start |
| `3` | Switch tool to: Place Goal |
| `B` | Solve with BFS and show solution (overlay on grid) |
| `D` | Solve with DFS and show solution |
| `+` | Increase grid size by 2 rows and 2 cols |
| `-` | Decrease grid size by 2 rows and 2 cols |
| `T` | Cycle theme |
| `ESC` | Quit editor |

---

## Mouse Controls

| Input | Action |
|-------|--------|
| Left click | Toggle wall/open at cell |
| Left click + drag | Continuous wall drawing |
| Right click | Opens small popup: [Place Start] [Place Goal] |
| Middle click | Erase (set to open) regardless of current state |
| Scroll wheel | Zoom in/out (resize cells between 16px and 48px) |

---

## Grid State Management

The editor maintains:
- `self.grid: List[List[str]]` — current maze state
- `self.undo_stack: List[List[List[str]]]` — up to 20 snapshots for undo
- `self.start: Optional[Tuple]`, `self.goal: Optional[Tuple]`

Every modification pushes a deep copy of the grid onto `undo_stack` before changing.

---

## "Solve Preview" Feature

When `B` or `D` is pressed:
1. Validate the maze has both S and G
2. Run the selected solver
3. If found: overlay the solution path in the editor view (transparent yellow overlay on path cells)
4. Display stats in status bar: `BFS: FOUND in 23 steps, 47 explored`
5. Clear overlay on next edit

---

## Save Behavior

`Ctrl+S`:
1. If maze has no `S`, show error in status bar: `Error: No Start position set`
2. If maze has no `G`, show error: `Error: No Goal position set`
3. Otherwise, prompt user for filename (print to terminal: `Save as (filename): `)
4. Save to `data/<filename>.txt`
5. Status bar: `Saved to data/my_maze.txt`

---

## New/Resize Behavior

`Ctrl+N` or `+`/`-`:
- Prompt for new dimensions (or auto-adjust for `+`/`-`)
- New grid: all `#` (walls) with single open-bordered interior empty
- Existing S/G are preserved if they fit in new size, otherwise cleared

---

## Generator Integration

`Ctrl+G` or toolbar Generate button:
1. Run `RecursiveBacktrackGenerator(self.rows, self.cols)`
2. Replace `self.grid` with generated maze
3. Auto-detect and set `self.start` and `self.goal`
4. Do NOT run solver automatically — user can then manually edit and run B/D

---

## EditorApp Class Structure

```python
class MazeEditor:
    CELL_SIZE = 24
    TOOLBAR_HEIGHT = 50
    STATUSBAR_HEIGHT = 30
    
    def __init__(self, rows: int = 21, cols: int = 21):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.grid = self._init_empty_grid()
        self.undo_stack = []
        self.start = None
        self.goal = None
        self.tool = "wall"        # "wall", "start", "goal"
        self.solution_overlay = set()  # path cells to highlight
        self.status_msg = "Ready"
        # ... init screen, fonts, clock

    def _init_empty_grid(self) -> List[List[str]]:
        """All walls on border, all open inside."""
        grid = [["#"] * self.cols for _ in range(self.rows)]
        for r in range(1, self.rows - 1):
            for c in range(1, self.cols - 1):
                grid[r][c] = " "
        return grid

    def run(self):
        """Main loop."""
        running = True
        while running:
            for event in pygame.event.get():
                running = self._handle_event(event)
            self._draw()
            self.clock.tick(60)
        pygame.quit()
    
    def _handle_event(self, event) -> bool:
        # Handle QUIT, KEYDOWN (shortcuts), MOUSEBUTTONDOWN, MOUSEMOTION
        ...

    def _draw(self):
        # Draw toolbar, grid cells, solution overlay, status bar
        ...

    def _cell_at_mouse(self, mx, my) -> Optional[Tuple[int, int]]:
        """Convert mouse pixel to (row, col)."""
        r = (my - self.TOOLBAR_HEIGHT) // self.CELL_SIZE
        c = mx // self.CELL_SIZE
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return (r, c)
        return None

    def push_undo(self):
        """Save current state to undo stack."""
        import copy
        self.undo_stack.append(copy.deepcopy(self.grid))
        if len(self.undo_stack) > 20:
            self.undo_stack.pop(0)

    def undo(self):
        if self.undo_stack:
            self.grid = self.undo_stack.pop()
```
