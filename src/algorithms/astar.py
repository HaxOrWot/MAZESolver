"""
MAZESolver — A* (A-Star) Search Solver
======================================
Informed search algorithm utilizing the Manhattan distance heuristic.
Guarantees optimal solution paths while significantly pruning explored nodes.
"""
import heapq
import time
from typing import Dict, Any, List, Tuple
from src.node import Node
from src.algorithms.base_solver import BaseSolver


class AStarSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.frontier_history: List[List[Tuple[int, int]]] = []

    def heuristic(self, pos: Tuple[int, int]) -> int:
        """Manhattan distance heuristic to goal."""
        return abs(pos[0] - self.maze.goal[0]) + abs(pos[1] - self.maze.goal[1])

    def solve(self) -> Dict[str, Any]:
        """
        Executes A* Search on the maze.
        Returns a result dictionary adhering to the contract.
        """
        start_time = time.perf_counter()

        start_node = Node(self.maze.start, parent=None, depth=0)
        h_start = self.heuristic(self.maze.start)
        # Entry: (f_score, tie_breaker_counter, Node)
        counter = 0
        heap: List[Tuple[int, int, Node]] = [(h_start, counter, start_node)]

        visited = set()
        visited_order = []
        self.frontier_history = []

        while heap:
            f, _, current = heapq.heappop(heap)

            if current.position in visited:
                continue

            visited.add(current.position)
            visited_order.append(current.position)
            self.frontier_history.append([item[2].position for item in heap[:8]])

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
                    counter += 1
                    child = Node(neighbor, parent=current, depth=current.depth + 1)
                    g = child.depth
                    h = self.heuristic(neighbor)
                    heapq.heappush(heap, (g + h, counter, child))

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
