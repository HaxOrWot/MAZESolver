"""
MAZESolver — Shared Test Fixtures
===================================
Run: pytest tests/ -v
"""
import pytest
from src.maze import Maze

# ── Maze strings ──────────────────────────────────────────────────────────────

SIMPLE_MAZE = (
    "#####\n"
    "#S  #\n"
    "### #\n"
    "#G  #\n"
    "#####"
)

NO_PATH_MAZE = (
    "#####\n"
    "#S ##\n"
    "#####\n"
    "## G#\n"
    "#####"
)

OPEN_MAZE = (
    "#######\n"
    "#S    #\n"
    "#     #\n"
    "#     #\n"
    "#    G#\n"
    "#######"
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def simple_maze(tmp_path):
    f = tmp_path / "simple.txt"
    f.write_text(SIMPLE_MAZE)
    return Maze(str(f))

@pytest.fixture
def no_path_maze(tmp_path):
    f = tmp_path / "nopath.txt"
    f.write_text(NO_PATH_MAZE)
    return Maze(str(f))

@pytest.fixture
def open_maze(tmp_path):
    f = tmp_path / "open.txt"
    f.write_text(OPEN_MAZE)
    return Maze(str(f))
