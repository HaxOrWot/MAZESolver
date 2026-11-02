# base class — all solvers inherit this
from abc import ABC, abstractmethod
from src.maze import Maze

class BaseSolver(ABC):
    def __init__(self, maze: Maze):
        self.maze = maze

    @abstractmethod
    def solve(self) -> dict:
        pass
