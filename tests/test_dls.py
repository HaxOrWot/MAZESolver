"""
Tests for DLS Solver (src/algorithms/dls.py)
Run: pytest tests/test_dls.py -v
"""
import pytest
from src.algorithms.dls import DLSSolver


def test_dls_finds_path_sufficient_limit(simple_maze):
    """With limit=20 (way more than needed), DLS finds the path."""
    result = DLSSolver(simple_maze, limit=20).solve()
    assert result["found"] is True


def test_dls_no_path_small_limit(simple_maze):
    """With limit=2 (less than actual path depth of 6), DLS fails."""
    result = DLSSolver(simple_maze, limit=2).solve()
    assert result["found"] is False


def test_dls_exact_limit(simple_maze):
    """With limit exactly equal to path length (6), DLS just barely finds it."""
    result = DLSSolver(simple_maze, limit=6).solve()
    assert result["found"] is True


def test_dls_limit_zero(simple_maze):
    """Limit=0 means only the start cell is explored. Not found (unless start==goal)."""
    result = DLSSolver(simple_maze, limit=0).solve()
    assert result["found"] is False


def test_dls_path_valid(simple_maze):
    result = DLSSolver(simple_maze, limit=20).solve()
    path = result["path"]
    for i in range(len(path) - 1):
        dr = abs(path[i+1][0] - path[i][0])
        dc = abs(path[i+1][1] - path[i][1])
        assert dr + dc == 1


def test_dls_no_path_maze(no_path_maze):
    result = DLSSolver(no_path_maze, limit=50).solve()
    assert result["found"] is False


def test_dls_default_limit(simple_maze):
    """No limit arg → defaults to rows+cols without crashing."""
    result = DLSSolver(simple_maze).solve()
    assert "found" in result
    assert result["depth_limit"] == simple_maze.rows + simple_maze.cols


def test_dls_result_keys(simple_maze):
    result = DLSSolver(simple_maze, limit=20).solve()
    for key in ["path", "visited", "nodes_explored", "path_length", "time_taken", "found", "depth_limit"]:
        assert key in result
