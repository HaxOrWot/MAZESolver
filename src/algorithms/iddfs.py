"""
MAZESolver — IDDFS (Iterative Deepening Depth-First Search) Solver
=================================================================
Combines BFS's optimality (shortest path in unweighted graphs)
with DFS's memory efficiency by progressively deepening the search limit.
"""
import time
from typing import Dict, Any, List, Tuple
from src.node import Node
from src.algorithms.base_solver import BaseSolver


class IDDFSSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.frontier_history: List[List[Tuple[int, int]]] = []

    def _dls_pass(
        self, limit: int
    ) -> Tuple[bool, List[Tuple[int, int]], List[Tuple[int, int]], List[List[Tuple[int, int]]]]:
        """Executes a single depth-limited search pass."""
        start_node = Node(self.maze.start, parent=None, depth=0)
        stack = [start_node]
        visited = set()
        visited_order = []
        frontier_snaps = []

        while stack:
            current = stack.pop()

            if current.position in visited:
                continue

            visited.add(current.position)
            visited_order.append(current.position)
            frontier_snaps.append([n.position for n in reversed(stack[-8:])])

            if current.position == self.maze.goal:
                return True, current.get_path(), visited_order, frontier_snaps

            if current.depth >= limit:
                continue

            for neighbor in self.maze.get_neighbors(current.position):
                if neighbor not in visited:
                    stack.append(Node(neighbor, parent=current, depth=current.depth + 1))

        return False, [], visited_order, frontier_snaps

    def solve(self) -> Dict[str, Any]:
        """
        Runs DLS with increasing limits (L = 0, 1, 2, ...) until goal is found
        or the max possible search depth is exceeded.
        """
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
                elapsed = time.perf_counter() - start_time
                return {
                    "path": path,
                    "visited": all_visited,
                    "nodes_explored": len(all_visited),
                    "path_length": len(path),
                    "time_taken": elapsed,
                    "found": True,
                    "iterations": iteration + 1,
                    "frontier_history": self.frontier_history,
                }

            iteration += 1

        elapsed = time.perf_counter() - start_time
        return {
            "path": [],
            "visited": all_visited,
            "nodes_explored": len(all_visited),
            "path_length": 0,
            "time_taken": elapsed,
            "found": False,
            "iterations": iteration,
            "frontier_history": self.frontier_history,
        }
