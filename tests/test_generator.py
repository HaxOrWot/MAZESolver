"""
Tests for Maze Generators (src/generator/)
"""
import pytest
from src.generator.recursive_backtrack import RecursiveBacktrackGenerator
from src.generator.prims import PrimsGenerator
from src.maze import Maze
from src.algorithms.bfs import BFSSolver


@pytest.mark.parametrize("GeneratorClass", [RecursiveBacktrackGenerator, PrimsGenerator])
def test_generator_produces_solvable_maze(tmp_path, GeneratorClass):
    gen = GeneratorClass(rows=15, cols=15, seed=42)
    gen.generate()
    path = tmp_path / "test_maze.txt"
    gen.save(str(path))
    maze = Maze(str(path))
    result = BFSSolver(maze).solve()
    assert result["found"] is True
    assert result["path_length"] > 0


def test_generator_outer_border_is_walls(tmp_path):
    gen = RecursiveBacktrackGenerator(15, 15, seed=123)
    gen.generate()
    for c in range(gen.cols):
        assert gen.grid[0][c] == "#"
        assert gen.grid[gen.rows - 1][c] == "#"
    for r in range(gen.rows):
        assert gen.grid[r][0] == "#"
        assert gen.grid[r][gen.cols - 1] == "#"


def test_generator_has_start_and_goal(tmp_path):
    gen = PrimsGenerator(11, 11)
    gen.generate()
    path = tmp_path / "prims_maze.txt"
    gen.save(str(path))
    maze = Maze(str(path))
    assert maze.start == (1, 1)
    assert maze.goal == (gen.rows - 2, gen.cols - 2)
