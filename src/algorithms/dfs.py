import time
from src.node import Node
from src.algorithms.base_solver import BaseSolver

class DFSSolver(BaseSolver):
    def __init__(self, maze):
        super().__init__(maze)
        self.frontier_history = []

    def solve(self) -> dict:
        """DFS using stack (LIFO)"""
        start_time = time.perf_counter()

        start_node = Node(self.maze.start, parent=None, depth=0)
        st = [start_node]
        visited = set()
        visited_order = []
        self.frontier_history = []

        while len(st) > 0:
            current = st.pop()

            # check visited upon popping because multiple copies can be pushed
            if current.position in visited:
                continue

            visited.add(current.position)
            visited_order.append(current.position)
            self.frontier_history.append([n.position for n in reversed(st[-8:])])

            if current.position == self.maze.goal:
                path = current.get_path()
                return {
                    "path": path,
                    "visited": visited_order,
                    "nodes_explored": len(visited_order),
                    "path_length": len(path),
                    "time_taken": time.perf_counter() - start_time,
                    "found": True,
                    "frontier_history": self.frontier_history,
                }

            # get adjacent free cells
            neighbors = self.maze.get_neighbors(current.position)
            for nb in neighbors:
                if nb not in visited:
                    st.append(Node(nb, parent=current, depth=current.depth + 1))

        return {
            "path": [],
            "visited": visited_order,
            "nodes_explored": len(visited_order),
            "path_length": 0,
            "time_taken": time.perf_counter() - start_time,
            "found": False,
            "frontier_history": self.frontier_history,
        }
