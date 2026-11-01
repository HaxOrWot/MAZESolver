"""
Tests for A* Solver (src/algorithms/astar.py)
"""
import pytest
from src.algorithms.astar import AStarSolver
from src.algorithms.bfs import BFSSolver


def test_astar_finds_path(simple_maze):
    result = AStarSolver(simple_maze).solve()
    assert result["found"] is True
    assert result["path_length"] == 7  # optimal path


def test_astar_path_is_valid(simple_maze):
    result = AStarSolver(simple_maze).solve()
    path = result["path"]
    for i in range(len(path) - 1):
        dr = abs(path[i+1][0] - path[i][0])
        dc = abs(path[i+1][1] - path[i][1])
        assert dr + dc == 1


def test_astar_no_path(no_path_maze):
    result = AStarSolver(no_path_maze).solve()
    assert result["found"] is False
    assert result["path"] == []


def test_astar_heuristic_admissible(simple_maze):
    solver = AStarSolver(simple_maze)
    assert solver.heuristic(simple_maze.goal) == 0
    assert solver.heuristic(simple_maze.start) >= 0


def test_astar_efficiency_on_open_maze(open_maze):
    bfs_res = BFSSolver(open_maze).solve()
    astar_res = AStarSolver(open_maze).solve()
    # A* guided by Manhattan distance explores fewer nodes than unguided BFS on an open grid
    assert astar_res["nodes_explored"] <= bfs_res["nodes_explored"]
