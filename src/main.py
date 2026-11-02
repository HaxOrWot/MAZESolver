# main CLI driver for the project
import argparse
import datetime
import os
import sys

# add root to path so imports work from anywhere
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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

def append_to_log(algo_name, maze_file, result):
    # logs run to results_log.txt
    out_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(out_dir, exist_ok=True)
    log_path = os.path.join(out_dir, "results_log.txt")

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    base = os.path.basename(maze_file)
    status = "FOUND" if result.get("found") else "NOT FOUND"
    steps = f"{result.get('path_length', 0)} steps"
    nodes = f"{result.get('nodes_explored', 0)} nodes"
    time_ms = f"{result.get('time_taken', 0.0) * 1000:.2f}ms"

    line = f"[{ts}] | {algo_name.upper()} | {base} | {status} | {steps} | {nodes} | {time_ms}\n"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line)

def print_result(algo_name, maze_file, result):
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

def print_comparison(results, algo_names):
    col_algo = 16
    col_found = 9
    col_nodes = 16
    col_path = 14
    col_time = 14

    top_border = "╔" + "═" * col_algo + "╦" + "═" * col_found + "╦" + "═" * col_nodes + "╦" + "═" * col_path + "╦" + "═" * col_time + "╗"
    header = "║" + "  Algorithm".ljust(col_algo) + "║" + "  Found? ".ljust(col_found) + "║" + " Nodes Explored ".ljust(col_nodes) + "║" + " Path Length  ".ljust(col_path) + "║" + "  Time (ms)   ".ljust(col_time) + "║"
    mid_border = "╠" + "═" * col_algo + "╬" + "═" * col_found + "╬" + "═" * col_nodes + "╬" + "═" * col_path + "╬" + "═" * col_time + "╣"
    bot_border = "╚" + "═" * col_algo + "╩" + "═" * col_found + "╩" + "═" * col_nodes + "╩" + "═" * col_path + "╩" + "═" * col_time + "╝"

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

def resolve_maze_path(maze_arg):
    # helper to allow shortcuts like '20' or 'data/maze_20x20.txt'
    if not maze_arg:
        default_path = os.path.join(PROJECT_ROOT, "data", "maze_20x20.txt")
        return default_path if os.path.exists(default_path) else "data/maze_5x5.txt"

    if os.path.exists(maze_arg):
        return maze_arg

    in_data = os.path.join(PROJECT_ROOT, "data", maze_arg)
    if os.path.exists(in_data):
        return in_data

    clean_num = maze_arg.lower().replace(".txt", "").replace("maze_", "")
    if "x" in clean_num:
        cand = os.path.join(PROJECT_ROOT, "data", f"maze_{clean_num}.txt")
    else:
        cand = os.path.join(PROJECT_ROOT, "data", f"maze_{clean_num}x{clean_num}.txt")

    if os.path.exists(cand):
        return cand

    return maze_arg

def main():
    parser = argparse.ArgumentParser(description="MAZESolver CLI")
    parser.add_argument("-m", "--maze", help="Path or shorthand size (e.g. 20, 100, data/maze_20x20.txt)")
    parser.add_argument(
        "-a",
        "--algo",
        choices=["bfs", "dfs", "dls", "iddfs", "astar"],
        help="Algorithm: bfs, dfs, dls, iddfs, or astar",
    )
    parser.add_argument("-v", "--visual", action="store_true", help="Launch visual animation")
    parser.add_argument("-l", "--limit", type=int, help="Depth limit for DLS")
    parser.add_argument("-c", "--compare", action="store_true", help="Compare all algorithms")
    parser.add_argument("-s", "--splitview", action="store_true", help="Split view BFS vs DFS vs DLS")
    parser.add_argument("-t", "--theme", choices=["dark", "neon", "retro", "light"], default=None)
    parser.add_argument("--export-gif", action="store_true", help="Save animated GIF")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate maze first")
    parser.add_argument("--maze-size", type=int, default=21, help="Size NxN for generated maze")
    parser.add_argument(
        "--gen-algo",
        choices=["recursive_backtrack", "prims"],
        default="recursive_backtrack",
        help="Generation algorithm",
    )
    parser.add_argument("-e", "--edit", action="store_true", help="Open maze editor")

    args = parser.parse_args()

    # editor mode
    if args.edit:
        from src.editor.maze_editor import MazeEditor
        editor = MazeEditor(rows=args.maze_size, cols=args.maze_size, theme_name=args.theme or "dark")
        editor.run()
        return

    # procedural generation
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

    args.maze = resolve_maze_path(args.maze)

    if not os.path.exists(args.maze):
        print(f"Error: Maze file '{args.maze}' not found.")
        sys.exit(1)

    maze = Maze(args.maze)

    # 3-panel split view
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

    # compare mode
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

    # default to visual bfs if nothing specified
    if not args.algo:
        args.algo = "bfs"
        args.visual = True

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
