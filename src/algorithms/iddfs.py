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
        """Runs iterative deepening: L=0, 1, 2... until we hit goal"""
        start_time = time.perf_counter()
        all_visited = []
        self.frontier_history = []
        iteration = 0
        max_limit = self.maze.rows * self.maze.cols

        while iteration <= max_limit:
            found, path, visited_iter, snaps = self._dls_pass(limit=iteration)
            all_visited.extend(visited_iter)
            self.frontier_history.extend(snaps)

            if found:
                return {
                    "path": path,
                    "visited": all_visited,
                    "nodes_explored": len(all_visited),
                    "path_length": len(path),
                    "time_taken": time.perf_counter() - start_time,
                    "found": True,
                    "iterations": iteration + 1,
                    "frontier_history": self.frontier_history,
                }

            iteration += 1

        return {
            "path": [],
            "visited": all_visited,
            "nodes_explored": len(all_visited),
            "path_length": 0,
            "time_taken": time.perf_counter() - start_time,
            "found": False,
            "iterations": iteration,
            "frontier_history": self.frontier_history,
        }
