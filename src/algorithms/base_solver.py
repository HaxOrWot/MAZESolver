"""
MAZESolver — Abstract Base Solver
===================================
All solver classes (BFSSolver, DFSSolver, DLSSolver) must inherit from this.

RESULT DICT CONTRACT (every solver must return this exact shape):
{
    "path":           list[tuple],   # Solution path [(r,c),...] or [] if not found
    "visited":        list[tuple],   # All explored nodes in exploration order
    "nodes_explored": int,           # Count of unique nodes popped from frontier
    "path_length":    int,           # len(path), or 0 if not found
    "time_taken":     float,         # seconds (use time.perf_counter)
    "found":          bool           # True if solution was found
}
"""

from abc import ABC, abstractmethod
from src.maze import Maze


class BaseSolver(ABC):
    def __init__(self, maze: Maze):
        self.maze = maze

    @abstractmethod
    def solve(self) -> dict:
        """Run the search and return the result dictionary."""
        pass
