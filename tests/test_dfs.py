"""
Tests for DFS Solver (src/algorithms/dfs.py)
Run: pytest tests/test_dfs.py -v
"""
import pytest
from src.algorithms.dfs import DFSSolver


def test_dfs_finds_path(simple_maze):
    result = DFSSolver(simple_maze).solve()
    assert result["found"] is True


def test_dfs_path_is_valid(simple_maze):
    result = DFSSolver(simple_maze).solve()
    path = result["path"]
    for i in range(len(path) - 1):
        dr = abs(path[i+1][0] - path[i][0])
        dc = abs(path[i+1][1] - path[i][1])
        assert dr + dc == 1


def test_dfs_path_starts_at_start(simple_maze):
    result = DFSSolver(simple_maze).solve()
    assert result["path"][0] == simple_maze.start


def test_dfs_path_ends_at_goal(simple_maze):
    result = DFSSolver(simple_maze).solve()
    assert result["path"][-1] == simple_maze.goal


def test_dfs_no_path(no_path_maze):
    result = DFSSolver(no_path_maze).solve()
    assert result["found"] is False
    assert result["path"] == []


def test_dfs_visited_no_revisit(simple_maze):
    """No cell should appear more than once in visited."""
    result = DFSSolver(simple_maze).solve()
    assert len(set(result["visited"])) == len(result["visited"])


def test_dfs_result_keys(simple_maze):
    result = DFSSolver(simple_maze).solve()
    for key in ["path", "visited", "nodes_explored", "path_length", "time_taken", "found"]:
        assert key in result
