"""
MAZESolver — DLS (Depth-Limited Search) Solver
==============================================
A variant of DFS that terminates search branches exceeding a specified depth limit.
Prevents infinite looping in unbounded search spaces.
"""
import time
from typing import Dict, Any, Optional
from src.node import Node
from src.algorithms.base_solver import BaseSolver
from src.maze import Maze


class DLSSolver(BaseSolver):
    def __init__(self, maze: Maze, limit: Optional[int] = None):
        super().__init__(maze)
        self.limit: int = limit if limit is not None else (maze.rows + maze.cols)

    def solve(self) -> Dict[str, Any]:
        """
        Executes Depth-Limited Search on the maze up to self.limit depth.
        Returns a result dictionary including 'depth_limit'.
        """
        start_time = time.perf_counter()

        start_node = Node(self.maze.start, parent=None, depth=0)
        stack = [start_node]
        visited = set()
        visited_order = []

        while stack:
            current = stack.pop()

            if current.position in visited:
                continue

            visited.add(current.position)
            visited_order.append(current.position)

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
                    "depth_limit": self.limit,
                }

            if current.depth >= self.limit:
                continue

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
            "depth_limit": self.limit,
        }
