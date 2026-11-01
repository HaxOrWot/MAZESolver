# 🟢 Depth-First Search (DFS) — Deep Dive

## 1. Theory

DFS is an **uninformed search algorithm** that dives deep into one branch before backtracking. It follows a path to its end, and only when it hits a dead end does it step back and try another branch. It is **complete** (for finite mazes) but **not optimal** — it may find a longer path than BFS.

**Why it's not optimal:**  
DFS doesn't consider path length. It commits fully to whichever branch it picks first. If that branch reaches the goal via a long winding route, DFS will return that — even if a shorter route exists elsewhere.

---

## 2. Key Properties

| Property | Value |
|----------|-------|
| Data Structure | Stack (LIFO) — Python list with `.append()` / `.pop()` |
| Time Complexity | O(V + E) where V = cells, E = edges |
| Space Complexity | O(depth) — only current path + frontier on stack |
| Optimal? | ❌ No — may not find shortest path |
| Complete? | ✅ Yes (for finite, acyclic mazes with visited tracking) |
| Best for? | Exhaustive exploration, memory efficiency |

---

## 3. Pseudocode

```
function DFS(maze, start, goal):
    stack ← empty LIFO stack
    visited ← empty set
    visited_order ← empty list

    start_node ← Node(start, parent=None, depth=0)
    stack.push(start_node)

    while stack is not empty:
        current ← stack.pop()              // remove from TOP

        if current.position in visited:
            continue
        
        visited.add(current.position)
        visited_order.append(current.position)

        if current.position == goal:
            path ← current.get_path()
            return SUCCESS(path, visited_order)

        for neighbor in maze.get_neighbors(current.position):
            if neighbor not in visited:
                child ← Node(neighbor, parent=current, depth=current.depth+1)
                stack.push(child)           // add to TOP

    return FAILURE(visited_order)
```

> **Note:** The visited check happens at pop-time (not push-time) for DFS, because the same cell may be pushed multiple times from different paths. This is fine for correctness and is standard DFS practice.

---

## 4. Python Implementation Skeleton

```python
from src.node import Node
from src.algorithms.base_solver import BaseSolver
import time

class DFSSolver(BaseSolver):
    def solve(self):
        start_time = time.perf_counter()
        
        start_node = Node(self.maze.start, parent=None, depth=0)
        stack = [start_node]                # Python list as LIFO stack
        visited = set()
        visited_order = []

        while stack:
            current = stack.pop()           # LIFO: pop from RIGHT (top)

            if current.position in visited:
                continue                    # skip already-explored cells

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
                    "found": True
                }

            for neighbor in self.maze.get_neighbors(current.position):
                if neighbor not in visited:
                    stack.append(Node(neighbor, parent=current, depth=current.depth+1))

        return {
            "path": [],
            "visited": visited_order,
            "nodes_explored": len(visited_order),
            "path_length": 0,
            "time_taken": time.perf_counter() - start_time,
            "found": False
        }
```

---

## 5. Worked Example

Maze (5×5):
```
#####
#S  #
### #
#G  #
#####
```
Grid coords (row, col), Start=(1,1), Goal=(3,1)

DFS Exploration (neighbors pushed RIGHT first, so RIGHT explored last = LEFT explored first):
```
Stack: [(1,1)]
Pop (1,1) → push neighbors: (1,2)
Stack: [(1,2)]
Pop (1,2) → push neighbors: (1,3), (1,1)[visited]
Stack: [(1,3)]
Pop (1,3) → push neighbors: (2,3)
Stack: [(2,3)]
Pop (2,3) → push neighbors: (3,3)
Stack: [(3,3)]
Pop (3,3) → push neighbors: (3,2)
Stack: [(3,2)]
Pop (3,2) → push neighbors: (3,1)
Stack: [(3,1)]
Pop (3,1) → GOAL! ✅
```

Solution path: `(1,1)→(1,2)→(1,3)→(2,3)→(3,3)→(3,2)→(3,1)` — 7 steps.

> In this simple maze, BFS and DFS happen to find the same path. In complex mazes, DFS often finds longer paths.

---

## 6. BFS vs DFS Visual Difference

| | BFS | DFS |
|--|-----|-----|
| Pattern | Expands outward in rings | Dives straight into one branch |
| Memory | Higher (wide frontier) | Lower (just current path) |
| Path quality | Shortest path | Any valid path |
| Good for | Shortest path needed | Memory-constrained, deep mazes |

---

## 7. Important Edge Cases

- **Cycle prevention**: Always maintain a `visited` set. Without it, DFS on a maze with loops will run forever.
- **Direction order effect**: Changing the order you push neighbors onto the stack changes which path DFS finds (but not whether it finds one).
- **Large mazes**: DFS uses O(depth) memory vs BFS's O(width) — for very wide mazes, DFS wins on memory.
