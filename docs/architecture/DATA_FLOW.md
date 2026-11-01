# 🔄 Data Flow — MAZESolver

This document traces exactly how data flows through the system from CLI input to visual output.

---

## Step-by-Step Data Flow

```
Step 1: User Input
══════════════════
User runs:
  python src/main.py --maze data/maze_20x20.txt --algo bfs --visual

                     │
                     ▼

Step 2: Argument Parsing (main.py)
═══════════════════════════════════
argparse produces:
  args.maze  = "data/maze_20x20.txt"
  args.algo  = "bfs"
  args.visual = True
  args.limit = None   (only for DLS)

                     │
                     ▼

Step 3: Maze Loading (maze.py)
═══════════════════════════════
  maze = Maze("data/maze_20x20.txt")
  
  Internally reads file → builds:
    maze.grid  = [['#','#',...], [' ','S',...], ...]   (2D list of chars)
    maze.start = (1, 1)    ← row, col of 'S'
    maze.goal  = (18, 18)  ← row, col of 'G'
    maze.rows  = 20
    maze.cols  = 20

                     │
                     ▼

Step 4: Solver Instantiation & Execution (bfs.py)
══════════════════════════════════════════════════
  solver = BFSSolver(maze)
  result = solver.solve()
  
  BFS internally:
    frontier = deque([Node(start, parent=None, depth=0)])
    visited  = set()
    visited_order = []   ← records exploration order for animation
    
    while frontier:
        node = frontier.popleft()       ← pop from LEFT (FIFO)
        visited_order.append(node.position)
        
        if node.position == goal:
            return build_result(node, visited_order, timer)
        
        for neighbor_pos in maze.get_neighbors(node.position):
            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                frontier.append(Node(neighbor_pos, parent=node, depth=node.depth+1))
    
    return no_path_result(visited_order, timer)

  result = {
    "path":           [(1,1),(1,2),(1,3),...,(18,18)],
    "visited":        [(1,1),(1,2),(2,2),...],
    "nodes_explored": 87,
    "path_length":    34,
    "time_taken":     0.000821,
    "found":          True
  }

                     │
                     ▼

Step 5A: Text Output (if no --visual)
══════════════════════════════════════
  main.py prints result to terminal:
  
  Algorithm : BFS
  Found     : YES
  Path Len  : 34 steps
  Explored  : 87 nodes
  Time      : 0.82 ms

                     │
                     ▼  (only if --visual)

Step 5B: Renderer Initialization (renderer.py)
═══════════════════════════════════════════════
  renderer = Renderer(maze, result)
  renderer.run()
  
  Pygame window opens:
    - Window size = cols * CELL_SIZE + 250 (HUD panel)  ×  rows * CELL_SIZE
    - CELL_SIZE = max(15, 500 // max(rows, cols))  (auto-scales to maze size)

                     │
                     ▼

Step 6: Animation Loop (renderer.py)
══════════════════════════════════════
  animation_step = 0
  
  Each frame:
    if animation_step < len(result["visited"]):
        draw cell result["visited"][animation_step] in BLUE
        update HUD "Nodes Explored" counter
        animation_step += 1
    
    elif not path_drawn:
        for pos in result["path"]:
            draw cell in YELLOW
        path_drawn = True
    
    HUD always shows:
        Algorithm, Maze file, Nodes Explored, Path Length, Time, Status

                     │
                     ▼

Step 7: User Interaction
═════════════════════════
    SPACE   → pause / resume animation
    S key   → save screenshot to output/screenshots/bfs_maze20x20_<timestamp>.png
    R key   → re-run solver and restart animation
    ESC     → quit Pygame

                     │  (on S key)
                     ▼

Step 8: Screenshot Export (renderer.py)
═════════════════════════════════════════
  pygame.image.save(screen, "output/screenshots/bfs_maze20x20_20261101.png")
  
  Also appends to output/results_log.txt:
    [2026-11-01 17:55] | BFS | maze_20x20.txt | FOUND | 34 steps | 87 nodes | 0.82ms
```

---

## Maze Neighbor Generation Detail

`maze.get_neighbors((row, col))` checks 4 directions:

```python
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#             UP       DOWN    LEFT     RIGHT

for dr, dc in DIRECTIONS:
    new_pos = (row + dr, col + dc)
    if is_valid(new_pos):   # in-bounds AND not a wall
        yield new_pos
```

Order matters for DFS — it determines which branch is explored first.

---

## Node Path Backtracking

When the goal is reached, `Node.get_path()` walks the parent chain:

```
Goal Node (18,18) → parent → (18,17) → parent → ... → Start Node (1,1)
                                                               │
                                                          parent = None
                                                         (stop here)

Result: reversed list = [(1,1), ..., (18,18)]
```

---

## --compare Mode Data Flow

```
main.py
  ├── run BFS  → result_bfs
  ├── run DFS  → result_dfs
  └── run DLS  → result_dls
        │
        ▼
  print_comparison_table([result_bfs, result_dfs, result_dls])
        │
        ▼
  Save comparison to output/results_log.txt
```
