# 🏗️ Maze Generator Specification (`src/generator/`)

---

## Overview

The maze generator creates valid, solvable 2D grid mazes programmatically. All generators produce mazes in the same `.txt` format as the existing `data/` mazes, ensuring full compatibility with all solvers.

**Key guarantee:** Every generated maze is guaranteed to have a valid path from `S` to `G`.

---

## Base Generator (`src/generator/base_generator.py`)

```python
from abc import ABC, abstractmethod
from typing import List, Tuple
import random

class BaseGenerator(ABC):
    def __init__(self, rows: int, cols: int, seed: int = None):
        # Ensure odd dimensions so we have proper wall/cell grid structure
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        # Initialize grid: all walls
        self.grid: List[List[str]] = [["#"] * self.cols for _ in range(self.rows)]
        self.start: Tuple[int, int] = None
        self.goal: Tuple[int, int] = None

    @abstractmethod
    def generate(self) -> List[List[str]]:
        """Generate the maze grid. Returns grid."""
        ...

    def _carve(self, r: int, c: int):
        """Mark a cell as open path."""
        self.grid[r][c] = " "

    def _place_start_goal(self):
        """
        Place S near top-left and G near bottom-right (always on open cells).
        Uses (1,1) for start and (rows-2, cols-2) for goal by default.
        """
        self.grid[1][1] = "S"
        self.start = (1, 1)
        self.grid[self.rows - 2][self.cols - 2] = "G"
        self.goal = (self.rows - 2, self.cols - 2)

    def to_txt_string(self) -> str:
        """Convert grid to .txt file string."""
        return "\n".join("".join(row) for row in self.grid)

    def save(self, filepath: str):
        """Save generated maze to a .txt file."""
        import os
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_txt_string())
        print(f"[Generator] Saved maze to {filepath}")
```

---

## Algorithm 1: Recursive Backtracker (`src/generator/recursive_backtrack.py`)

Most commonly used, produces mazes with long winding corridors. Ideal for BFS/DFS comparison since paths are complex.

### How it works:
1. Start at cell (1,1), mark it as visited
2. While there are unvisited neighbors (2 cells away):
   - Pick a random unvisited neighbor
   - Carve through the wall between current and neighbor (the cell in between)
   - Recurse into the neighbor
3. When no unvisited neighbors remain, backtrack

### Implementation:
```python
class RecursiveBacktrackGenerator(BaseGenerator):
    def generate(self) -> List[List[str]]:
        # Only cells at odd (row, col) positions are "rooms"
        # Cells at even positions between them are potential walls
        visited = set()

        def dfs(r, c):
            visited.add((r, c))
            self._carve(r, c)

            directions = [(-2,0),(2,0),(0,-2),(0,2)]
            random.shuffle(directions)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.rows-1 and 0 < nc < self.cols-1:
                    if (nr, nc) not in visited:
                        # Carve the wall between (r,c) and (nr,nc)
                        self._carve(r + dr//2, c + dc//2)
                        dfs(nr, nc)

        dfs(1, 1)
        self._place_start_goal()
        return self.grid
```

---

## Algorithm 2: Prim's Algorithm (`src/generator/prims.py`)

Produces mazes with more branching paths (less winding). Good for demonstrating BFS exploring many branches.

### How it works:
1. Start with all walls. Pick a random starting cell, mark as visited.
2. Add all walls adjacent to the visited cell to a "frontier" list.
3. While frontier is not empty:
   - Pick a random wall from frontier
   - If exactly one of the two cells it connects is visited:
     - Carve the wall and mark the new cell visited
     - Add new cell's walls to frontier

```python
class PrimsGenerator(BaseGenerator):
    def generate(self) -> List[List[str]]:
        visited = set()
        frontier = []

        def add_walls(r, c):
            for dr, dc in [(-2,0),(2,0),(0,-2),(0,2)]:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.rows-1 and 0 < nc < self.cols-1:
                    if (nr, nc) not in visited:
                        frontier.append((r, c, nr, nc))

        start_r, start_c = 1, 1
        visited.add((start_r, start_c))
        self._carve(start_r, start_c)
        add_walls(start_r, start_c)

        while frontier:
            idx = random.randrange(len(frontier))
            r1, c1, r2, c2 = frontier.pop(idx)

            if (r2, c2) not in visited:
                visited.add((r2, c2))
                self._carve(r2, c2)
                self._carve((r1+r2)//2, (c1+c2)//2)
                add_walls(r2, c2)

        self._place_start_goal()
        return self.grid
```

---

## Algorithm 3: Wilson's Algorithm (`src/generator/wilsons.py`)

Produces **unbiased** random spanning trees — all possible mazes equally likely. More complex but worth implementing.

### How it works:
1. Start with one cell visited (random).
2. Pick any unvisited cell. Do a random walk from it until hitting a visited cell (erase loops as you go).
3. Carve the loop-erased path into the maze.
4. Repeat until all cells are visited.

Wilson's is notable because it avoids the bias that Recursive Backtrack has toward long corridors.

Implementation: see pseudocode in https://en.wikipedia.org/wiki/Maze_generation_algorithm#Wilson's_algorithm

---

## Generator CLI (`src/generator/generator_cli.py`)

```bash
# Generate 25x25 recursive backtrack maze
python src/generator/generator_cli.py --size 25 --algo recursive_backtrack

# Generate 30x31 Prim's maze with seed 42 (reproducible)
python src/generator/generator_cli.py --rows 30 --cols 31 --algo prims --seed 42

# Generate and immediately view with BFS
python src/generator/generator_cli.py --size 20 --algo prims --solve bfs --visual
```

### Arguments:
```
--size    INT           Square maze of NxN (overridden by --rows/--cols)
--rows    INT           Row count (must be odd, or will be rounded up)
--cols    INT           Col count (must be odd, or will be rounded up)
--algo    STR           recursive_backtrack | prims | wilsons (default: recursive_backtrack)
--seed    INT           Random seed for reproducibility
--output  PATH          Output file path (default: data/generated/maze_NxN_ALGO_SEED.txt)
--solve   STR           After generating, immediately solve with bfs|dfs|dls and print stats
--visual  FLAG          Open Pygame window to show generated maze
```

---

## Integration with `main.py`

When `--generate` flag is used:
```bash
python src/main.py --generate --maze-size 25 --gen-algo prims --algo bfs --visual
```

1. Run `RecursiveBacktrackGenerator(25, 25)` (or whichever gen-algo)
2. Save to `data/generated/maze_25x25_prims_<timestamp>.txt`
3. Load the generated maze
4. Proceed normally with the specified algo + visual flag

---

## `tests/test_generator.py`

```python
from src.generator.recursive_backtrack import RecursiveBacktrackGenerator
from src.generator.prims import PrimsGenerator
from src.maze import Maze
from src.algorithms.bfs import BFSSolver

@pytest.mark.parametrize("GeneratorClass", [RecursiveBacktrackGenerator, PrimsGenerator])
def test_generator_produces_solvable_maze(tmp_path, GeneratorClass):
    gen = GeneratorClass(rows=11, cols=11, seed=42)
    gen.generate()
    path = tmp_path / "test_maze.txt"
    gen.save(str(path))
    maze = Maze(str(path))
    result = BFSSolver(maze).solve()
    assert result["found"] is True

def test_generator_outer_border_is_walls(tmp_path):
    gen = RecursiveBacktrackGenerator(11, 11, seed=1)
    gen.generate()
    for c in range(gen.cols):
        assert gen.grid[0][c] == "#"
        assert gen.grid[gen.rows - 1][c] == "#"
    for r in range(gen.rows):
        assert gen.grid[r][0] == "#"
        assert gen.grid[r][gen.cols - 1] == "#"

def test_generator_has_start_and_goal(tmp_path):
    gen = RecursiveBacktrackGenerator(11, 11)
    gen.generate()
    path = tmp_path / "maze.txt"
    gen.save(str(path))
    maze = Maze(str(path))
    assert maze.start is not None
    assert maze.goal is not None
```
