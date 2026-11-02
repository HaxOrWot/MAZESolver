import time
from src.node import Node
from src.algorithms.base_solver import BaseSolver
from src.maze import Maze

class DLSSolver(BaseSolver):
    def __init__(self, maze: Maze, limit=None):
        super().__init__(maze)
        # default limit is rows + cols if none passed
        self.limit = limit if limit is not None else (maze.rows + maze.cols)
        self.frontier_history = []

    def solve(self) -> dict:
        """DFS with depth cap to prevent going in circles forever"""
        start_time = time.perf_counter()

        start_node = Node(self.maze.start, parent=None, depth=0)
        stack = [start_node]
        visited = set()
        visited_order = []
        self.frontier_history = []

        while stack:
            curr = stack.pop()

            if curr.position in visited:
                continue

            visited.add(curr.position)
            visited_order.append(curr.position)
            self.frontier_history.append([n.position for n in reversed(stack[-8:])])

            if curr.position == self.maze.goal:
                path = curr.get_path()
                return {
                    "path": path,
                    "visited": visited_order,
                    "nodes_explored": len(visited_order),
                    "path_length": len(path),
                    "time_taken": time.perf_counter() - start_time,
                    "found": True,
                    "depth_limit": self.limit,
                    "frontier_history": self.frontier_history,
                }

            # prune if depth limit reached
            if curr.depth >= self.limit:
                continue

            for nb in self.maze.get_neighbors(curr.position):
                if nb not in visited:
                    stack.append(Node(nb, parent=curr, depth=curr.depth + 1))

        return {
            "path": [],
            "visited": visited_order,
            "nodes_explored": len(visited_order),
            "path_length": 0,
            "time_taken": time.perf_counter() - start_time,
            "found": False,
            "depth_limit": self.limit,
            "frontier_history": self.frontier_history,
        }
