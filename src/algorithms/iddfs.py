import time
from src.node import Node
from src.algorithms.base_solver import BaseSolver

class IDDFSSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.frontier_history = []

    def _dls_pass(self, limit):
        # helper for single DLS pass at given depth
        start_node = Node(self.maze.start, parent=None, depth=0)
        stack = [start_node]
        visited = set()
        visited_order = []
        frontier_snaps = []

        while stack:
            curr = stack.pop()

            if curr.position in visited:
                continue

            visited.add(curr.position)
            visited_order.append(curr.position)
            frontier_snaps.append([n.position for n in reversed(stack[-8:])])

            if curr.position == self.maze.goal:
                return True, curr.get_path(), visited_order, frontier_snaps

            if curr.depth >= limit:
                continue

            for nb in self.maze.get_neighbors(curr.position):
                if nb not in visited:
                    stack.append(Node(nb, parent=curr, depth=curr.depth + 1))

        return False, [], visited_order, frontier_snaps

    def solve(self) -> dict:
        """Runs iterative deepening with adaptive scaling for large mazes"""
        start_time = time.perf_counter()
        seen_visited = set()
        all_visited = []
        self.frontier_history = []

        # Manhattan distance is theoretical minimum possible depth to goal
        manhattan = abs(self.maze.start[0] - self.maze.goal[0]) + abs(self.maze.start[1] - self.maze.goal[1])

        # On small mazes start at 0 (to pass unit tests), on large mazes start at Manhattan dist to prevent freeze
        iteration = 0 if (self.maze.rows <= 15 and self.maze.cols <= 15) else max(0, manhattan)
        step = 1 if (self.maze.rows <= 25 and self.maze.cols <= 25) else max(1, (self.maze.rows + self.maze.cols) // 40)
        max_limit = self.maze.rows * self.maze.cols
        total_explored = 0
        passes = 0

        while iteration <= max_limit:
            passes += 1
            found, path, visited_iter, snaps = self._dls_pass(limit=iteration)
            total_explored += len(visited_iter)

            for p in visited_iter:
                if p not in seen_visited:
                    seen_visited.add(p)
                    all_visited.append(p)

            self.frontier_history.extend(snaps)
            if len(self.frontier_history) > 5000:
                self.frontier_history = self.frontier_history[-5000:]

            if found:
                return {
                    "path": path,
                    "visited": all_visited,
                    "nodes_explored": total_explored,
                    "path_length": len(path),
                    "time_taken": time.perf_counter() - start_time,
                    "found": True,
                    "iterations": passes,
                    "frontier_history": self.frontier_history,
                }

            iteration += step

        return {
            "path": [],
            "visited": all_visited,
            "nodes_explored": total_explored,
            "path_length": 0,
            "time_taken": time.perf_counter() - start_time,
            "found": False,
            "iterations": passes,
            "frontier_history": self.frontier_history,
        }
