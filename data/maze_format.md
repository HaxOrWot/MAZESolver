# Maze File Format

## Overview

Mazes are stored as plain `.txt` files in the `data/` directory.  
Each character in the file represents one cell in the grid.

## Character Key

| Character | Meaning |
|-----------|---------|
| `#` | Wall — impassable |
| ` ` (space) | Open path — passable |
| `S` | Start position (exactly 1 per file) |
| `G` | Goal position (exactly 1 per file) |

## Rules

1. Every row must have the **same length** (rectangular grid only)
2. The maze should be **fully enclosed by walls** (`#`) on all 4 sides
3. There must be **exactly one** `S` and **exactly one** `G`
4. `S` and `G` count as open (passable) cells

## Example — 5×5 Maze

```
#####
#S  #
### #
#G  #
#####
```

## Example — 10×10 Maze

```
##########
#S       #
# ######  #
#    #   #
#### # ###
#    #   #
# ## ### #
#  #     #
## # ### #
#       G#
##########
```

## Loading in Python

```python
from src.maze import Maze
maze = Maze("data/maze_10x10.txt")
print(maze.start)   # (1, 1)
print(maze.goal)    # (9, 8)
```

## Creating Your Own Maze

You can create a maze in any text editor. Tips:
- Keep the outer border all `#`
- Make sure there is at least one connected path from `S` to `G`
- Test it with: `python src/main.py --maze data/your_maze.txt --algo bfs`
