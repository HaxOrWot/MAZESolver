"""
MAZESolver — Recursive Backtracking Maze Generator
===================================================
Generates intricate, winding mazes with long corridors using randomized DFS.
"""
import random
import sys
from typing import List
from src.generator.base_generator import BaseGenerator


class RecursiveBacktrackGenerator(BaseGenerator):
    def generate(self) -> List[List[str]]:
        # Increase recursion limit for large mazes
        required_depth = (self.rows * self.cols) // 2 + 1000
        if required_depth > sys.getrecursionlimit():
            sys.setrecursionlimit(required_depth)

        visited = set()

        def dfs(r: int, c: int) -> None:
            visited.add((r, c))
            self._carve(r, c)

            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            random.shuffle(directions)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.rows - 1 and 0 < nc < self.cols - 1:
                    if (nr, nc) not in visited:
                        # Carve intermediate wall cell between (r, c) and (nr, nc)
                        self._carve(r + dr // 2, c + dc // 2)
                        dfs(nr, nc)

        dfs(1, 1)
        self._place_start_goal()
        return self.grid
