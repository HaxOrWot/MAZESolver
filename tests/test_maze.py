"""
Tests for Maze class (src/maze.py)
Run: pytest tests/test_maze.py -v
"""
import pytest
from src.maze import Maze


# ── M-01 ──────────────────────────────────────────────────────────────────────
def test_load_start_goal(simple_maze):
    """Maze correctly identifies start and goal positions."""
    assert simple_maze.start == (1, 1)
    assert simple_maze.goal  == (3, 1)


# ── M-02 ──────────────────────────────────────────────────────────────────────
def test_grid_dimensions(simple_maze):
    """Grid rows and cols match the file dimensions."""
    assert simple_maze.rows == 5
    assert simple_maze.cols == 5


# ── M-03 ──────────────────────────────────────────────────────────────────────
def test_is_wall_true(simple_maze):
    """Corner cells (walls) return True."""
    assert simple_maze.is_wall((0, 0)) is True
    assert simple_maze.is_wall((0, 4)) is True


# ── M-04 ──────────────────────────────────────────────────────────────────────
def test_is_wall_false(simple_maze):
    """Start cell is not a wall."""
    assert simple_maze.is_wall((1, 1)) is False


# ── M-05 ──────────────────────────────────────────────────────────────────────
def test_is_valid_out_of_bounds(simple_maze):
    """Out-of-bounds positions are invalid."""
    assert simple_maze.is_valid((-1,  0)) is False
    assert simple_maze.is_valid(( 0, -1)) is False
    assert simple_maze.is_valid(( 5,  0)) is False
    assert simple_maze.is_valid(( 0,  5)) is False


# ── M-06 ──────────────────────────────────────────────────────────────────────
def test_get_neighbors_count(simple_maze):
    """Start cell (1,1) has at least 1 valid neighbor."""
    neighbors = simple_maze.get_neighbors((1, 1))
    assert len(neighbors) >= 1


# ── M-07 ──────────────────────────────────────────────────────────────────────
def test_get_neighbors_no_wall(simple_maze):
    """All returned neighbors must be passable cells."""
    for pos in [(1,1), (1,2), (1,3)]:
        for n in simple_maze.get_neighbors(pos):
            assert simple_maze.is_wall(n) is False


# ── M-08 ──────────────────────────────────────────────────────────────────────
def test_missing_start_raises(tmp_path):
    """File with no 'S' raises ValueError."""
    f = tmp_path / "no_start.txt"
    f.write_text("#####\n#   #\n#   #\n#  G#\n#####")
    with pytest.raises(ValueError, match="[Ss]tart"):
        Maze(str(f))


# ── M-09 ──────────────────────────────────────────────────────────────────────
def test_missing_goal_raises(tmp_path):
    """File with no 'G' raises ValueError."""
    f = tmp_path / "no_goal.txt"
    f.write_text("#####\n#S  #\n#   #\n#   #\n#####")
    with pytest.raises(ValueError, match="[Gg]oal"):
        Maze(str(f))
