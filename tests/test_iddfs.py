"""
Tests for IDDFS Solver (src/algorithms/iddfs.py)
"""
import pytest
from src.algorithms.iddfs import IDDFSSolver


def test_iddfs_finds_path(simple_maze):
    result = IDDFSSolver(simple_maze).solve()
    assert result["found"] is True
    assert result["path_length"] == 7  # IDDFS is optimal like BFS
    assert "iterations" in result
    assert result["iterations"] >= 1


def test_iddfs_path_is_valid(simple_maze):
    result = IDDFSSolver(simple_maze).solve()
    path = result["path"]
    for i in range(len(path) - 1):
        dr = abs(path[i+1][0] - path[i][0])
        dc = abs(path[i+1][1] - path[i][1])
        assert dr + dc == 1


def test_iddfs_no_path(no_path_maze):
    result = IDDFSSolver(no_path_maze).solve()
    assert result["found"] is False
    assert result["path"] == []
