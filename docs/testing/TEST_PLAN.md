# 🧪 Test Plan — MAZESolver

## 1. Testing Strategy

All tests are written with **pytest** and live in the `tests/` directory. Tests are grouped by module and cover:
- **Unit tests** — individual classes and functions
- **Integration tests** — algorithm solving a full maze end-to-end
- **Edge cases** — no solution, single cell, limit boundaries

Run all tests:
```bash
pytest tests/ -v
```

Run a specific file:
```bash
pytest tests/test_bfs.py -v
```

---

## 2. Test Mazes

Create small deterministic mazes inside test files as string constants — no file I/O needed:

```python
# tests/conftest.py (shared fixtures)

import pytest
from src.maze import Maze

SIMPLE_MAZE_STR = """
#####
#S  #
### #
#G  #
#####
""".strip()

NO_PATH_MAZE_STR = """
#####
#S #
###  
# G#
#####
""".strip()

OPEN_MAZE_STR = """
#######
#S    #
#     #
#     #
#    G#
#######
""".strip()

@pytest.fixture
def simple_maze(tmp_path):
    f = tmp_path / "simple.txt"
    f.write_text(SIMPLE_MAZE_STR)
    return Maze(str(f))

@pytest.fixture
def no_path_maze(tmp_path):
    f = tmp_path / "nopath.txt"
    f.write_text(NO_PATH_MAZE_STR)
    return Maze(str(f))

@pytest.fixture
def open_maze(tmp_path):
    f = tmp_path / "open.txt"
    f.write_text(OPEN_MAZE_STR)
    return Maze(str(f))
```

---

## 3. Maze Class Tests (`tests/test_maze.py`)

| Test ID | Test Name | Description | Expected |
|---------|-----------|-------------|----------|
| M-01 | `test_load_start_goal` | Maze loads correct start & goal coords | start=(1,1), goal=(3,1) |
| M-02 | `test_grid_dimensions` | Grid rows and cols match file | rows=5, cols=5 |
| M-03 | `test_is_wall_true` | Wall cells return True | is_wall((0,0)) == True |
| M-04 | `test_is_wall_false` | Open cells return False | is_wall((1,1)) == False |
| M-05 | `test_is_valid_out_of_bounds` | Negative or oversized coords invalid | is_valid((-1,0)) == False |
| M-06 | `test_get_neighbors_count` | Open cell returns correct neighbor count | 1–4 neighbors |
| M-07 | `test_get_neighbors_no_wall` | Neighbors never include walls | all cells passable |
| M-08 | `test_missing_start_raises` | File with no 'S' raises ValueError | ValueError |
| M-09 | `test_missing_goal_raises` | File with no 'G' raises ValueError | ValueError |

---

## 4. BFS Tests (`tests/test_bfs.py`)

| Test ID | Test Name | Description | Expected |
|---------|-----------|-------------|----------|
| B-01 | `test_bfs_finds_path` | BFS solves simple maze | result["found"] == True |
| B-02 | `test_bfs_path_is_valid` | Every step in path is adjacent | no teleports |
| B-03 | `test_bfs_path_starts_at_start` | Path begins at start | path[0] == maze.start |
| B-04 | `test_bfs_path_ends_at_goal` | Path ends at goal | path[-1] == maze.goal |
| B-05 | `test_bfs_optimal_path` | BFS finds shortest path | path_length == known_min |
| B-06 | `test_bfs_no_path` | BFS returns found=False when no solution | result["found"] == False |
| B-07 | `test_bfs_visited_contains_start` | Visited list starts with start node | visited[0] == maze.start |
| B-08 | `test_bfs_nodes_explored_count` | nodes_explored matches len(visited) | consistent |
| B-09 | `test_bfs_open_maze` | BFS on wide-open maze finds short path | path efficient |

---

## 5. DFS Tests (`tests/test_dfs.py`)

| Test ID | Test Name | Description | Expected |
|---------|-----------|-------------|----------|
| D-01 | `test_dfs_finds_path` | DFS solves simple maze | result["found"] == True |
| D-02 | `test_dfs_path_is_valid` | Every step in path is adjacent | no teleports |
| D-03 | `test_dfs_path_starts_at_start` | Path begins at start | path[0] == maze.start |
| D-04 | `test_dfs_path_ends_at_goal` | Path ends at goal | path[-1] == maze.goal |
| D-05 | `test_dfs_no_path` | DFS returns found=False when no solution | result["found"] == False |
| D-06 | `test_dfs_visited_no_revisit` | No cell appears twice in visited | len(set(visited)) == len(visited) |
| D-07 | `test_dfs_result_dict_keys` | Result has all required keys | all keys present |

---

## 6. DLS Tests (`tests/test_dls.py`)

| Test ID | Test Name | Description | Expected |
|---------|-----------|-------------|----------|
| L-01 | `test_dls_finds_path_sufficient_limit` | Limit > path length → finds path | result["found"] == True |
| L-02 | `test_dls_no_path_small_limit` | Limit < path length → not found | result["found"] == False |
| L-03 | `test_dls_exact_limit` | Limit == exact path length → finds path | result["found"] == True |
| L-04 | `test_dls_limit_zero` | Limit = 0 (only checks start cell) | found only if start==goal |
| L-05 | `test_dls_path_valid` | Found path is adjacent-only | no teleports |
| L-06 | `test_dls_respects_depth` | No node in visited has depth > limit | max(node.depth) <= limit |
| L-07 | `test_dls_no_path_maze` | DLS on unsolvable maze | result["found"] == False |
| L-08 | `test_dls_default_limit` | Default limit = rows + cols | no crash, reasonable result |

---

## 7. Node Class Tests (inside `test_maze.py` or separate `test_node.py`)

| Test ID | Test Name | Description | Expected |
|---------|-----------|-------------|----------|
| N-01 | `test_node_get_path_single` | Node with no parent returns [position] | `[(r,c)]` |
| N-02 | `test_node_get_path_chain` | 3-node chain returns correct path | `[start, mid, end]` |
| N-03 | `test_node_equality` | Two nodes with same position are equal | `node1 == node2` |
| N-04 | `test_node_hashable` | Node can be used in a set | no TypeError |
| N-05 | `test_node_depth` | Depth increments correctly down chain | `child.depth == parent.depth + 1` |

---

## 8. Running Tests in CI (Optional GitHub Actions)

Add `.github/workflows/test.yml`:
```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: pip install pytest colorama
      - run: pytest tests/ -v
```

> Pygame is excluded from CI tests (requires display). Wrap any test that imports renderer with `@pytest.mark.skipif` or mock it.

---

## 9. Coverage Target

| Module | Target Coverage |
|--------|----------------|
| `maze.py` | 90%+ |
| `node.py` | 100% |
| `algorithms/bfs.py` | 90%+ |
| `algorithms/dfs.py` | 90%+ |
| `algorithms/dls.py` | 90%+ |
| `visualization/` | Not tested (UI layer) |

```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=term-missing
```
