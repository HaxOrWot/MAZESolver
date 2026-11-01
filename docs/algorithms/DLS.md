# 🟡 Depth-Limited Search (DLS) — Deep Dive

## 1. Theory

DLS is a **variant of DFS** that introduces a hard depth limit `L`. The algorithm works identically to DFS, but it refuses to explore any node deeper than `L` levels from the start. This prevents DFS from going infinitely deep in large or infinite search spaces.

**Why it's useful:**  
In an infinite or very large maze, plain DFS might never return. DLS guarantees termination by cutting off branches that exceed the depth limit. The tradeoff: if the goal is deeper than `L`, DLS will return "no path found" even when one exists.

---

## 2. Key Properties

| Property | Value |
|----------|-------|
| Data Structure | Stack (LIFO) with depth tracking |
| Time Complexity | O(L × b^L) where b = branching factor |
| Space Complexity | O(L) — only current path to depth L |
| Optimal? | ❌ No |
| Complete? | ❌ No — may miss solutions deeper than L |
| Best for? | Bounded search when max depth is known |

---

## 3. Pseudocode

```
function DLS(maze, start, goal, limit):
    stack ← empty LIFO stack
    visited ← empty set
    visited_order ← empty list

    start_node ← Node(start, parent=None, depth=0)
    stack.push(start_node)

    while stack is not empty:
        current ← stack.pop()

        if current.position in visited:
            continue

        visited.add(current.position)
        visited_order.append(current.position)

        if current.position == goal:
            path ← current.get_path()
            return SUCCESS(path, visited_order)

        if current.depth >= limit:
            continue                        // ← KEY DIFFERENCE: don't expand deeper

        for neighbor in maze.get_neighbors(current.position):
            if neighbor not in visited:
                child ← Node(neighbor, parent=current, depth=current.depth+1)
                stack.push(child)

    return FAILURE(visited_order)
```

The **only difference from DFS** is the check:
```
if current.depth >= limit:
    continue
```

---

## 4. Python Implementation Skeleton

```python
from src.node import Node
from src.algorithms.base_solver import BaseSolver
import time

class DLSSolver(BaseSolver):
    def __init__(self, maze, limit: int = 20):
        super().__init__(maze)
        self.limit = limit

    def solve(self):
        start_time = time.perf_counter()
        
        start_node = Node(self.maze.start, parent=None, depth=0)
        stack = [start_node]
        visited = set()
        visited_order = []

        while stack:
            current = stack.pop()

            if current.position in visited:
                continue

            visited.add(current.position)
            visited_order.append(current.position)

            if current.position == self.maze.goal:
                path = current.get_path()
                return {
                    "path": path,
                    "visited": visited_order,
                    "nodes_explored": len(visited_order),
                    "path_length": len(path),
                    "time_taken": time.perf_counter() - start_time,
                    "found": True,
                    "depth_limit": self.limit
                }

            if current.depth >= self.limit:
                continue                    # depth cutoff — don't expand

            for neighbor in self.maze.get_neighbors(current.position):
                if neighbor not in visited:
                    stack.append(Node(neighbor, parent=current, depth=current.depth + 1))

        return {
            "path": [],
            "visited": visited_order,
            "nodes_explored": len(visited_order),
            "path_length": 0,
            "time_taken": time.perf_counter() - start_time,
            "found": False,
            "depth_limit": self.limit
        }
```

---

## 5. Choosing the Right Depth Limit

| Scenario | Result |
|----------|--------|
| `limit` too small (< actual path length) | `found = False` — goal unreachable within limit |
| `limit` = exact path length | `found = True` — barely makes it |
| `limit` too large (>> path length) | Behaves like plain DFS, wastes memory |
| `limit` = optimal path length | Equivalent to IDDFS one iteration |

**Recommended `limit` for this project:**  
Use `rows + cols` as a reasonable default (Manhattan-distance upper bound for a simple maze).

```python
default_limit = maze.rows + maze.cols
```

---

## 6. DLS in the CLI

```bash
# Run DLS with limit of 15
python src/main.py --maze data/maze_10x10.txt --algo dls --limit 15 --visual

# Run DLS with default limit (rows + cols)
python src/main.py --maze data/maze_10x10.txt --algo dls --visual
```

If no `--limit` is provided, `DLSSolver` defaults to `maze.rows + maze.cols`.

---

## 7. DLS vs DFS Comparison

```
Maze 10×10, Goal at depth 22

DFS Result:
  found = True
  nodes_explored = 63
  path_length = 31

DLS (limit=10) Result:
  found = False  ← goal is at depth 22, limit is 10
  nodes_explored = 24  ← stopped early

DLS (limit=25) Result:
  found = True
  nodes_explored = 58
  path_length = 31
```

---

## 8. Academic Talking Points

For your college presentation / report, highlight these:

1. **DLS solves DFS's infinite-depth problem** in unbounded or cyclic graphs
2. **Completeness tradeoff**: DLS sacrifices completeness for bounded resources
3. **DLS is the building block of IDDFS** (Iterative Deepening DFS), which achieves both optimal paths and low memory by running DLS with L=0,1,2,3,... until the goal is found
4. **Real-world analogy**: A GPS with a "don't route paths longer than 50km" filter — faster, but may miss routes for far destinations
