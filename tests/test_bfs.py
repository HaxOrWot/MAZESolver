"""
Tests for BFS Solver (src/algorithms/bfs.py)
Run: pytest tests/test_bfs.py -v
"""
import pytest
from src.algorithms.bfs import BFSSolver


# ── B-01 ──────────────────────────────────────────────────────────────────────
def test_bfs_finds_path(simple_maze):
    result = BFSSolver(simple_maze).solve()
    assert result["found"] is True


# ── B-02 ──────────────────────────────────────────────────────────────────────
def test_bfs_path_is_valid(simple_maze):
    """Each consecutive step in the path must be exactly 1 cell apart."""
    result = BFSSolver(simple_maze).solve()
    path = result["path"]
    for i in range(len(path) - 1):
        dr = abs(path[i+1][0] - path[i][0])
        dc = abs(path[i+1][1] - path[i][1])
        assert dr + dc == 1, f"Non-adjacent step: {path[i]} -> {path[i+1]}"


# ── B-03 ──────────────────────────────────────────────────────────────────────
def test_bfs_path_starts_at_start(simple_maze):
    result = BFSSolver(simple_maze).solve()
    assert result["path"][0] == simple_maze.start


# ── B-04 ──────────────────────────────────────────────────────────────────────
def test_bfs_path_ends_at_goal(simple_maze):
    result = BFSSolver(simple_maze).solve()
    assert result["path"][-1] == simple_maze.goal


# ── B-05 ──────────────────────────────────────────────────────────────────────
def test_bfs_optimal_path(simple_maze):
    """BFS must find the shortest path (length 7 for simple_maze)."""
    result = BFSSolver(simple_maze).solve()
    assert result["path_length"] == 7


# ── B-06 ──────────────────────────────────────────────────────────────────────
def test_bfs_no_path(no_path_maze):
    result = BFSSolver(no_path_maze).solve()
    assert result["found"] is False
    assert result["path"] == []
    assert result["path_length"] == 0


# ── B-07 ──────────────────────────────────────────────────────────────────────
def test_bfs_visited_contains_start(simple_maze):
    result = BFSSolver(simple_maze).solve()
    assert simple_maze.start in result["visited"]


# ── B-08 ──────────────────────────────────────────────────────────────────────
def test_bfs_nodes_explored_count(simple_maze):
    result = BFSSolver(simple_maze).solve()
    assert result["nodes_explored"] == len(result["visited"])


# ── B-09 ──────────────────────────────────────────────────────────────────────
def test_bfs_result_keys(simple_maze):
    """Result dict must contain all required keys."""
    result = BFSSolver(simple_maze).solve()
    for key in ["path", "visited", "nodes_explored", "path_length", "time_taken", "found"]:
        assert key in result, f"Missing key: {key}"
