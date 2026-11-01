"""
MAZESolver — Maze Class
=======================
Handles maze loading, parsing, validation, and neighbor generation.
"""
from typing import List, Tuple, Optional


class Maze:
    # 4 cardinal directions: UP, DOWN, LEFT, RIGHT
    DIRECTIONS: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def __init__(self, filepath: str):
        self.grid: List[List[str]] = []
        self.rows: int = 0
        self.cols: int = 0
        self.start: Optional[Tuple[int, int]] = None
        self.goal: Optional[Tuple[int, int]] = None
        self.filepath: str = filepath
        self.load_from_file(filepath)

    def load_from_file(self, filepath: str) -> None:
        """
        Loads maze grid from a .txt file, locates start 'S' and goal 'G'.
        Raises ValueError if 'S' or 'G' is not found.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\r\n") for line in f]

        # Filter empty lines at beginning/end if any
        lines = [line for line in lines if line]

        if not lines:
            raise ValueError("Maze file is empty.")

        self.grid = [list(line) for line in lines]
        self.rows = len(self.grid)
        self.cols = max(len(row) for row in self.grid)

        # Pad shorter rows with spaces if any lines differ in length
        for r in range(self.rows):
            if len(self.grid[r]) < self.cols:
                self.grid[r].extend([" "] * (self.cols - len(self.grid[r])))

        start_found = False
        goal_found = False

        for r in range(self.rows):
            for c in range(self.cols):
                char = self.grid[r][c]
                if char == "S":
                    self.start = (r, c)
                    start_found = True
                elif char == "G":
                    self.goal = (r, c)
                    goal_found = True

        if not start_found:
            raise ValueError("Start position 'S' not found in maze file.")
        if not goal_found:
            raise ValueError("Goal position 'G' not found in maze file.")

    def is_in_bounds(self, pos: Tuple[int, int]) -> bool:
        """Check if (r, c) is within the grid boundary."""
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_wall(self, pos: Tuple[int, int]) -> bool:
        """Check if (r, c) is a wall '#'."""
        if not self.is_in_bounds(pos):
            return False
        return self.grid[pos[0]][pos[1]] == "#"

    def is_valid(self, pos: Tuple[int, int]) -> bool:
        """A cell is valid if in bounds and not a wall."""
        return self.is_in_bounds(pos) and not self.is_wall(pos)

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns passable adjacent neighbors (UP, DOWN, LEFT, RIGHT).
        """
        neighbors = []
        r, c = pos
        for dr, dc in self.DIRECTIONS:
            neighbor = (r + dr, c + dc)
            if self.is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def display(self) -> None:
        """Prints the maze grid to terminal."""
        for row in self.grid:
            print("".join(row))
