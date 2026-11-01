# 🔵 Breadth-First Search (BFS) — Deep Dive

## 1. Theory

BFS is an **uninformed search algorithm** that explores the maze level by level — all cells at distance 1 from start, then all at distance 2, and so on. It is **complete** and **optimal** (always finds the shortest path in an unweighted maze).

**Why it finds the shortest path:**  
BFS expands nodes in order of their distance from the start. The first time it reaches the goal, it has necessarily taken the fewest steps possible.

---

## 2. Key Properties

| Property | Value |
|----------|-------|
| Data Structure | Queue (FIFO) — `collections.deque` |
| Time Complexity | O(V + E) where V = cells, E = edges (adjacencies) |
| Space Complexity | O(V) — worst case, all cells in queue |
| Optimal? | ✅ Yes — shortest path guaranteed |
| Complete? | ✅ Yes — will find solution if one exists |
| Best for? | Finding the **shortest** path |

---

## 3. Pseudocode

```
function BFS(maze, start, goal):
    queue ← empty FIFO queue
    visited ← empty set
    visited_order ← empty list

    start_node ← Node(start, parent=None, depth=0)
    queue.enqueue(start_node)
    visited.add(start)

    while queue is not empty:
        current ← queue.dequeue()          // remove from FRONT
        visited_order.append(current.position)

        if current.position == goal:
            path ← current.get_path()      // backtrack parents
            return SUCCESS(path, visited_order)

        for neighbor in maze.get_neighbors(current.position):
            if neighbor not in visited:
                visited.add(neighbor)
                child ← Node(neighbor, parent=current, depth=current.depth+1)
                queue.enqueue(child)        // add to BACK

    return FAILURE(visited_order)           // no path found
```

---

## 4. Python Implementation Skeleton

```python
from collections import deque
from src.node import Node
from src.algorithms.base_solver import BaseSolver
import time

class BFSSolver(BaseSolver):
    def solve(self):
        start_time = time.perf_counter()
        
        start_node = Node(self.maze.start, parent=None, depth=0)
        queue = deque([start_node])
        visited = {self.maze.start}
        visited_order = []

        while queue:
            current = queue.popleft()           # FIFO: pop from LEFT
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
                    visited.add(neighbor)
                    queue.append(Node(neighbor, parent=current, depth=current.depth+1))

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

BFS Exploration Order:
```
Step 1: Dequeue (1,1) → neighbors: (1,2)
Step 2: Dequeue (1,2) → neighbors: (1,3)
Step 3: Dequeue (1,3) → neighbors: (2,3)   ← wall at (2,2) blocked!
Step 4: Dequeue (2,3) → neighbors: (3,3)
Step 5: Dequeue (3,3) → neighbors: (3,2)
Step 6: Dequeue (3,2) → neighbors: (3,1)
Step 7: Dequeue (3,1) → GOAL! ✅
```

Solution path: `(1,1)→(1,2)→(1,3)→(2,3)→(3,3)→(3,2)→(3,1)` — 7 steps (optimal).

---

## 6. Visualization Color Coding

During animation:
- **Blue cells**: Nodes dequeued and explored (visited_order)
- **Yellow cells**: Final solution path
- **Orange cell**: Current frontier head being processed

---

## 7. Comparison with DFS on Same Maze

BFS explores fewer cells when the path is short and direct.  
DFS may explore many dead ends before backtracking.  
**On the same 10×10 maze, BFS typically explores 30–60% fewer nodes than DFS.**
