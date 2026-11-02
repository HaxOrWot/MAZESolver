import random
import sys
from src.generator.base_generator import BaseGenerator

class RecursiveBacktrackGenerator(BaseGenerator):
    def generate(self):
        """randomized DFS to carve corridors"""
        # bump recursion limit in case of huge mazes
        depth = (self.rows * self.cols) // 2 + 1000
        if depth > sys.getrecursionlimit():
            sys.setrecursionlimit(depth)

        visited = set()

        def dfs(r, c):
            visited.add((r, c))
            self._carve(r, c)

            dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            random.shuffle(dirs)

            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.rows - 1 and 0 < nc < self.cols - 1:
                    if (nr, nc) not in visited:
                        # knock down wall in-between
                        self._carve(r + dr // 2, c + dc // 2)
                        dfs(nr, nc)

        dfs(1, 1)
        self._place_start_goal()
        return self.grid
