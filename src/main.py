"""
MAZESolver — CLI & Execution Coordinator (v2.0)
================================================
Entry point supporting:
- Single algorithm execution (BFS, DFS, DLS, IDDFS, A*)
- 5-Algorithm Comprehensive Comparison Mode
- Synchronized Split-Screen Side-by-Side Visualization
- Procedural Maze Generation on demand
- Interactive GUI Maze Editor
- Animated GIF and High-Resolution PNG export
"""
import argparse
import datetime
import os
import sys
from typing import List, Dict, Any

# Ensure project root is in python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.maze import Maze
from src.algorithms.bfs import BFSSolver
from src.algorithms.dfs import DFSSolver
from src.algorithms.dls import DLSSolver
from src.algorithms.iddfs import IDDFSSolver
from src.algorithms.astar import AStarSolver
from src.generator.recursive_backtrack import RecursiveBacktrackGenerator
from src.generator.prims import PrimsGenerator


def append_to_log(algo_name: str, maze_file: str, result: dict) -> None:
    """
    Appends execution stats to output/results_log.txt.
    Format: [YYYY-MM-DD HH:MM] | ALGO | filename | FOUND/NOT FOUND | X steps | Y nodes | Zms
    """
    out_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "results_log.txt")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    basename = os.path.basename(maze_file)
    status_str = "FOUND" if result.get("found") else "NOT FOUND"
    steps = f"{result.get('path_length', 0)} steps"
    nodes = f"{result.get('nodes_explored', 0)} nodes"
    time_ms = f"{result.get('time_taken', 0.0) * 1000:.2f}ms"

    log_line = f"[{timestamp}] | {algo_name.upper()} | {basename} | {status_str} | {steps} | {nodes} | {time_ms}\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_line)


def print_result(algo_name: str, maze_file: str, result: dict) -> None:
    """Pretty-prints a single algorithm run to the terminal."""
    found_str = "YES" if result.get("found") else "NO"
    time_sec = result.get("time_taken", 0.0)
    time_ms = time_sec * 1000

    print("\n" + "=" * 44)
    print(f"Algorithm : {algo_name.upper()}")
    print(f"Maze File : {os.path.basename(maze_file)}")
    print("─" * 44)
    print(f"Found      : {found_str}")
    print(f"Path Length: {result.get('path_length', 0)} steps")
    print(f"Nodes Exp. : {result.get('nodes_explored', 0)}")
    print(f"Time Taken : {time_ms:.2f} ms ({time_sec:.6f} s)")
    if "depth_limit" in result:
        print(f"Depth Limit: {result['depth_limit']}")
    if "iterations" in result:
        print(f"Iterations : {result['iterations']}")
    print("=" * 44 + "\n")


def print_comparison(results: List[Dict[str, Any]], algo_names: List[str]) -> None:
    """Prints a formatted comparison table for multiple algorithm results."""
    col_algo = 16
    col_found = 9
    col_nodes = 16
    col_path = 14
    col_time = 14

    top_border = (
        "╔" + "═" * col_algo
        + "╦" + "═" * col_found
        + "╦" + "═" * col_nodes
        + "╦" + "═" * col_path
        + "╦" + "═" * col_time + "╗"
    )
    header = (
        "║" + "  Algorithm".ljust(col_algo)
        + "║" + "  Found? ".ljust(col_found)
        + "║" + " Nodes Explored ".ljust(col_nodes)
        + "║" + " Path Length  ".ljust(col_path)
        + "║" + "  Time (ms)   ".ljust(col_time) + "║"
    )
    mid_border = (
        "╠" + "═" * col_algo
        + "╬" + "═" * col_found
        + "╬" + "═" * col_nodes
        + "╬" + "═" * col_path
        + "╬" + "═" * col_time + "╣"
    )
    bot_border = (
        "╚" + "═" * col_algo
        + "╩" + "═" * col_found
        + "╩" + "═" * col_nodes
        + "╩" + "═" * col_path
        + "╩" + "═" * col_time + "╝"
    )

    print("\n" + top_border)
    print(header)
    print(mid_border)

    for name, res in zip(algo_names, results):
        found = "YES" if res.get("found") else "NO"
        nodes = str(res.get("nodes_explored", 0))
        path_len = str(res.get("path_length", 0))
        time_ms = f"{res.get('time_taken', 0.0) * 1000:.2f}"

        row_str = (
            "║  " + name.ljust(col_algo - 2)
            + "║  " + found.ljust(col_found - 2)
            + "║     " + nodes.ljust(col_nodes - 5)
            + "║     " + path_len.ljust(col_path - 5)
            + "║    " + time_ms.ljust(col_time - 4) + "║"
        )
        print(row_str)

    print(bot_border + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MAZESolver 2.0 — Uninformed and Informed Search Suite"
    )
    parser.add_argument("--maze", help="Path to maze .txt file")
    parser.add_argument(
        "--algo",
        choices=["bfs", "dfs", "dls", "iddfs", "astar"],
        help="Algorithm: bfs, dfs, dls, iddfs, or astar",
    )
    parser.add_argument(
        "--visual", action="store_true", help="Launch interactive visual animation"
    )
    parser.add_argument(
        "--limit", type=int, help="Depth limit for DLS (default: rows + cols)"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run 5 algorithms side-by-side (BFS, DFS, DLS, IDDFS, A*)",
    )
    parser.add_argument(
        "--splitview",
        action="store_true",
        help="Open 3-panel synchronized comparison window (BFS, DFS, DLS)",
    )
    parser.add_argument(
        "--theme",
        choices=["dark", "neon", "retro", "light"],
        default=None,
        help="Visual theme (overrides config.json)",
    )
    parser.add_argument(
        "--export-gif", action="store_true", help="Capture and save animated GIF"
    )
    parser.add_argument(
        "--generate", action="store_true", help="Procedurally generate a maze first"
    )
    parser.add_argument(
        "--maze-size", type=int, default=21, help="Dimension NxN for generated maze (default: 21)"
    )
    parser.add_argument(
        "--gen-algo",
        choices=["recursive_backtrack", "prims"],
        default="recursive_backtrack",
        help="Generation algorithm (default: recursive_backtrack)",
    )
    parser.add_argument(
        "--edit", action="store_true", help="Open the interactive maze editor"
    )

    args = parser.parse_args()

    # 1. Interactive Maze Editor Mode
    if args.edit:
        from src.editor.maze_editor import MazeEditor
        editor = MazeEditor(rows=args.maze_size, cols=args.maze_size, theme_name=args.theme or "dark")
        editor.run()
        return

    # 2. Procedural Maze Generation
    if args.generate:
        gen_dir = os.path.join(PROJECT_ROOT, "data", "generated")
        os.makedirs(gen_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        gen_file = os.path.join(gen_dir, f"maze_{args.maze_size}x{args.maze_size}_{args.gen_algo}_{ts}.txt")

        if args.gen_algo == "prims":
            gen = PrimsGenerator(rows=args.maze_size, cols=args.maze_size)
        else:
            gen = RecursiveBacktrackGenerator(rows=args.maze_size, cols=args.maze_size)

        gen.generate()
        gen.save(gen_file)
        args.maze = gen_file
        print(f"[Generate] Generated solvable maze -> {args.maze}")

    if not args.maze:
        parser.error("You must specify a maze file via --maze, or use --generate, or use --edit")

    if not os.path.exists(args.maze):
        print(f"Error: Maze file '{args.maze}' not found.")
        sys.exit(1)

    maze = Maze(args.maze)

    # 3. Split-Screen Comparison Mode
    if args.splitview:
        from src.visualization.split_view import SplitRenderer
        bfs_res = BFSSolver(maze).solve()
        dfs_res = DFSSolver(maze).solve()
        dls_limit = args.limit if args.limit is not None else (maze.rows + maze.cols)
        dls_res = DLSSolver(maze, limit=dls_limit).solve()

        renderer = SplitRenderer(
            maze,
            {"bfs": bfs_res, "dfs": dfs_res, "dls": dls_res},
            theme_name=args.theme or "dark",
        )
        renderer.run()
        return

    # 4. Comprehensive Compare Mode (5 Algorithms)
    if args.compare:
        print(f"\nRunning 5-Algorithm Comparison on '{os.path.basename(args.maze)}'...")
        bfs_res = BFSSolver(maze).solve()
        dfs_res = DFSSolver(maze).solve()
        dls_limit = args.limit if args.limit is not None else (maze.rows + maze.cols)
        dls_res = DLSSolver(maze, limit=dls_limit).solve()
        iddfs_res = IDDFSSolver(maze).solve()
        astar_res = AStarSolver(maze).solve()

        algo_names = ["BFS", "DFS", f"DLS (L={dls_limit})", "IDDFS", "A* (Heuristic)"]
        results = [bfs_res, dfs_res, dls_res, iddfs_res, astar_res]

        print_comparison(results, algo_names)

        for name, res in zip(algo_names, results):
            append_to_log(name, args.maze, res)
        return

    # 5. Single Algorithm Execution
    if not args.algo:
        parser.error("Must specify --algo [bfs|dfs|dls|iddfs|astar], or --compare, or --splitview")

    algo_name = args.algo.lower()
    if algo_name == "bfs":
        solver = BFSSolver(maze)
        display_name = "BFS"
    elif algo_name == "dfs":
        solver = DFSSolver(maze)
        display_name = "DFS"
    elif algo_name == "dls":
        dls_limit = args.limit if args.limit is not None else (maze.rows + maze.cols)
        solver = DLSSolver(maze, limit=dls_limit)
        display_name = f"DLS (L={dls_limit})"
    elif algo_name == "iddfs":
        solver = IDDFSSolver(maze)
        display_name = "IDDFS"
    elif algo_name == "astar":
        solver = AStarSolver(maze)
        display_name = "A*"
    else:
        parser.error(f"Unknown algorithm: {args.algo}")

    result = solver.solve()
    print_result(display_name, args.maze, result)
    append_to_log(display_name, args.maze, result)

    if args.visual or args.export_gif:
        from src.visualization.renderer import Renderer
        renderer = Renderer(
            maze,
            result,
            display_name,
            theme_name=args.theme,
            export_gif=args.export_gif,
        )
        renderer.run()


if __name__ == "__main__":
    main()
