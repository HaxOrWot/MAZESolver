"""
MAZESolver — DFS (Depth-First Search) Solver
============================================
Explores deeply along each branch before backtracking.
Uses a Python list as a LIFO stack.
Checks visited upon popping to handle multiple insertions.
"""
import time
from typing import Dict, Any, List, Tuple
from src.node import Node
from src.algorithms.base_solver import BaseSolver


class DFSSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.frontier_history: List[List[Tuple[int, int]]] = []

    def solve(self) -> Dict[str, Any]:
        """
        Executes Depth-First Search on the maze.
        Returns a result dictionary adhering to the contract.
        """
        start_time = time.perf_counter()

        start_node = Node(self.maze.start, parent=None, depth=0)
        stack = [start_node]
        visited = set()
        visited_order = []
        self.frontier_history = []

        while stack:
            current = stack.pop()

            if current.position in visited:
                continue

            visited.add(current.position)
            visited_order.append(current.position)
            self.frontier_history.append([n.position for n in reversed(stack[-8:])])

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
                    stack.append(Node(neighbor, parent=current, depth=current.depth + 1))

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
