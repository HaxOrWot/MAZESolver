"""
MAZESolver — BFS (Breadth-First Search) Solver
==============================================
Guarantees optimal (shortest) path and completeness for unweighted grids.
Uses collections.deque as a FIFO queue.
"""
import time
from collections import deque
from typing import Dict, Any, List, Tuple
from src.node import Node
from src.algorithms.base_solver import BaseSolver


class BFSSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.frontier_history: List[List[Tuple[int, int]]] = []

    def solve(self) -> Dict[str, Any]:
        """
        Executes Breadth-First Search on the maze.
        Returns a result dictionary adhering to the contract.
        """
        start_time = time.perf_counter()

        start_node = Node(self.maze.start, parent=None, depth=0)
        queue = deque([start_node])
        visited = {self.maze.start}
        visited_order = []
        self.frontier_history = []

        while queue:
            current = queue.popleft()
            visited_order.append(current.position)
            self.frontier_history.append([n.position for n in list(queue)[:8]])

            if current.position == self.maze.goal:
                path = current.get_path()
                elapsed = time.perf_counter() - start_time
                return {
                    "path": path,
                    "visited": visited_order,
                    "nodes_explored": len(visited_order),
                    "path_length": len(path),
                    "time_taken": elapsed,
                    "found": True,
                    "frontier_history": self.frontier_history,
                }

            for neighbor in self.maze.get_neighbors(current.position):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(Node(neighbor, parent=current, depth=current.depth + 1))

        elapsed = time.perf_counter() - start_time
        return {
            "path": [],
            "visited": visited_order,
            "nodes_explored": len(visited_order),
            "path_length": 0,
            "time_taken": elapsed,
            "found": False,
            "frontier_history": self.frontier_history,
        }
