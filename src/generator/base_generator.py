"""
MAZESolver — Base Maze Generator
================================
Abstract base class for procedural maze generation algorithms.
Ensures odd grid dimensions and guaranteed outer perimeter walls.
"""
import os
import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class BaseGenerator(ABC):
    def __init__(self, rows: int, cols: int, seed: Optional[int] = None):
        # Force odd dimensions so alternating room/wall structure is mathematically consistent
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        # Initialize full wall matrix
        self.grid: List[List[str]] = [["#"] * self.cols for _ in range(self.rows)]
        self.start: Optional[Tuple[int, int]] = None
        self.goal: Optional[Tuple[int, int]] = None

    @abstractmethod
    def generate(self) -> List[List[str]]:
        """Generates the maze paths inside self.grid. Returns the grid."""
        pass

    def _carve(self, r: int, c: int) -> None:
        """Sets a grid cell to open passable space."""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = " "

    def _place_start_goal(self) -> None:
        """Guarantees start 'S' at (1, 1) and goal 'G' at (rows-2, cols-2)."""
        self.grid[1][1] = "S"
        self.start = (1, 1)
        self.grid[self.rows - 2][self.cols - 2] = "G"
        self.goal = (self.rows - 2, self.cols - 2)

    def to_txt_string(self) -> str:
        """Converts the grid 2D list into a formatted string."""
        return "\n".join("".join(row) for row in self.grid)

    def save(self, filepath: str) -> str:
        """Writes the generated maze to a .txt file."""
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_txt_string())
        print(f"[Generator] Saved maze to {filepath}")
        return filepath
