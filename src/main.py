"""
MAZESolver — CLI Entry Point
============================
Parses command-line arguments, runs selected search algorithms,
displays results (terminal or Pygame), and logs runs to output/results_log.txt.
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

    print("\n" + "=" * 40)
    print(f"Algorithm : {algo_name.upper()}")
    print(f"Maze File : {os.path.basename(maze_file)}")
    print("─" * 40)
    print(f"Found      : {found_str}")
    print(f"Path Length: {result.get('path_length', 0)} steps")
    print(f"Nodes Exp. : {result.get('nodes_explored', 0)}")
    print(f"Time Taken : {time_ms:.2f} ms ({time_sec:.6f} s)")
    if "depth_limit" in result:
        print(f"Depth Limit: {result['depth_limit']}")
    print("=" * 40 + "\n")


def print_comparison(results: List[Dict[str, Any]], algo_names: List[str]) -> None:
    """
    Prints a formatted comparison table for multiple algorithm results.
    """
    col_algo = 14
    col_found = 9
    col_nodes = 15
    col_path = 13
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
        + "║" + " Nodes Explored".ljust(col_nodes)
        + "║" + " Path Length ".ljust(col_path)
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
        description="MAZESolver — Solve mazes using BFS, DFS, or DLS"
    )
    parser.add_argument("--maze", required=True, help="Path to maze .txt file")
    parser.add_argument(
        "--algo",
        choices=["bfs", "dfs", "dls"],
        help="Algorithm to run: bfs, dfs, or dls",
    )
    parser.add_argument(
        "--visual", action="store_true", help="Launch interactive Pygame visualization"
    )
    parser.add_argument(
        "--limit", type=int, help="Depth limit for DLS (default: rows + cols)"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run BFS, DFS, and DLS side-by-side and display comparison table",
    )

    args = parser.parse_args()

    if not args.compare and not args.algo:
        parser.error("You must specify either --algo [bfs|dfs|dls] or --compare")

    if not os.path.exists(args.maze):
        print(f"Error: Maze file '{args.maze}' not found.")
        sys.exit(1)

    maze = Maze(args.maze)

    if args.compare:
        print(f"\nRunning comparison on '{os.path.basename(args.maze)}'...")
        bfs_res = BFSSolver(maze).solve()
        dfs_res = DFSSolver(maze).solve()
        dls_limit = args.limit if args.limit is not None else (maze.rows + maze.cols)
        dls_res = DLSSolver(maze, limit=dls_limit).solve()

        algo_names = ["BFS", "DFS", f"DLS (L={dls_limit})"]
        results = [bfs_res, dfs_res, dls_res]

        print_comparison(results, algo_names)

        append_to_log("BFS", args.maze, bfs_res)
        append_to_log("DFS", args.maze, dfs_res)
        append_to_log(f"DLS (L={dls_limit})", args.maze, dls_res)
        return

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
    else:
        parser.error(f"Unknown algorithm: {args.algo}")

    result = solver.solve()
    print_result(display_name, args.maze, result)
    append_to_log(display_name, args.maze, result)

    if args.visual:
        from src.visualization.renderer import Renderer

        renderer = Renderer(maze, result, display_name)
        renderer.run()


if __name__ == "__main__":
    main()
