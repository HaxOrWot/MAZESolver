import random
from src.generator.base_generator import BaseGenerator

class PrimsGenerator(BaseGenerator):
    def generate(self):
        # randomized prim's algorithm for maze gen
        visited = set()
        frontier = []

        def add_frontiers(r, c):
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.rows - 1 and 0 < nc < self.cols - 1:
                    if (nr, nc) not in visited:
                        frontier.append((r, c, nr, nc))

        start_r, start_c = 1, 1
        visited.add((start_r, start_c))
        self._carve(start_r, start_c)
        add_frontiers(start_r, start_c)

        while frontier:
            idx = random.randrange(len(frontier))
            r1, c1, r2, c2 = frontier.pop(idx)

            if (r2, c2) not in visited:
                visited.add((r2, c2))
                self._carve(r2, c2)
                self._carve((r1 + r2) // 2, (c1 + c2) // 2)
                add_frontiers(r2, c2)

        self._place_start_goal()
        return self.grid
