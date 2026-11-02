# base class for maze generators
import os
import random
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    def __init__(self, rows: int, cols: int, seed=None):
        # make sure rows and cols are odd numbers so walls/paths align properly
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        # fill everything with walls first
        self.grid = [["#"] * self.cols for _ in range(self.rows)]
        self.start = None
        self.goal = None

    @abstractmethod
    def generate(self):
        pass

    def _carve(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = " "

    def _place_start_goal(self):
        # start at top-left inner cell, goal at bottom-right
        self.grid[1][1] = "S"
        self.start = (1, 1)
        self.grid[self.rows - 2][self.cols - 2] = "G"
        self.goal = (self.rows - 2, self.cols - 2)

    def to_txt_string(self):
        return "\n".join("".join(row) for row in self.grid)

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_txt_string())
        print(f"[Generator] Saved maze to {filepath}")
        return filepath
