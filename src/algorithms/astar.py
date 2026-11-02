import heapq
import time
from src.node import Node
from src.algorithms.base_solver import BaseSolver

class AStarSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.frontier_history = []

    def heuristic(self, pos: tuple) -> int:
        # manhattan distance to goal
        return abs(pos[0] - self.maze.goal[0]) + abs(pos[1] - self.maze.goal[1])

    def solve(self) -> dict:
        """A* search with manhattan distance heuristic"""
        start_time = time.perf_counter()

        start_node = Node(self.maze.start, parent=None, depth=0)
        h_start = self.heuristic(self.maze.start)

        # entry format: (f_score, counter, node)
        # counter needed so heapq doesn't try to compare Node objects directly if f scores tie
        counter = 0
        heap = [(h_start, counter, start_node)]

        visited = set()
        visited_order = []
        self.frontier_history = []

        while heap:
            f, _, curr = heapq.heappop(heap)

            if curr.position in visited:
                continue

            visited.add(curr.position)
            visited_order.append(curr.position)
            self.frontier_history.append([item[2].position for item in heap[:8]])

            if curr.position == self.maze.goal:
                path = curr.get_path()
                return {
                    "path": path,
                    "visited": visited_order,
                    "nodes_explored": len(visited_order),
                    "path_length": len(path),
                    "time_taken": time.perf_counter() - start_time,
                    "found": True,
                    "frontier_history": self.frontier_history,
                }

            for nb in self.maze.get_neighbors(curr.position):
                if nb not in visited:
                    counter += 1
                    child = Node(nb, parent=curr, depth=curr.depth + 1)
                    g = child.depth
                    h = self.heuristic(nb)
                    heapq.heappush(heap, (g + h, counter, child))

        return {
            "path": [],
            "visited": visited_order,
            "nodes_explored": len(visited_order),
            "path_length": 0,
            "time_taken": time.perf_counter() - start_time,
            "found": False,
            "frontier_history": self.frontier_history,
        }
