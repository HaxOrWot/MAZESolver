# cli helper for procedural maze generation
import argparse
import datetime
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.generator.recursive_backtrack import RecursiveBacktrackGenerator
from src.generator.prims import PrimsGenerator
from src.maze import Maze
from src.algorithms.bfs import BFSSolver
from src.algorithms.dfs import DFSSolver
from src.algorithms.dls import DLSSolver
from src.algorithms.iddfs import IDDFSSolver
from src.algorithms.astar import AStarSolver

def main():
    parser = argparse.ArgumentParser(description="MAZESolver — Procedural Maze Generator")
    parser.add_argument("--size", type=int, help="NxN square maze dimension")
    parser.add_argument("--rows", type=int, default=21, help="Row count (default: 21)")
    parser.add_argument("--cols", type=int, default=21, help="Column count (default: 21)")
    parser.add_argument(
        "--algo",
        choices=["recursive_backtrack", "prims"],
        default="recursive_backtrack",
        help="Generation algorithm (default: recursive_backtrack)",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--output", type=str, default=None, help="Path to save output .txt file")
    parser.add_argument(
        "--solve",
        choices=["bfs", "dfs", "dls", "iddfs", "astar"],
        default=None,
        help="Immediately solve after generating",
    )
    parser.add_argument("--visual", action="store_true", help="Launch visualizer after generation")

    args = parser.parse_args()

    rows = args.size if args.size else args.rows
    cols = args.size if args.size else args.cols

    if args.algo == "prims":
        gen = PrimsGenerator(rows=rows, cols=cols, seed=args.seed)
    else:
        gen = RecursiveBacktrackGenerator(rows=rows, cols=cols, seed=args.seed)

    gen.generate()

    if not args.output:
        gen_dir = os.path.join(PROJECT_ROOT, "data", "generated")
        os.makedirs(gen_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = os.path.join(gen_dir, f"maze_{gen.rows}x{gen.cols}_{args.algo}_{ts}.txt")

    gen.save(args.output)
    print(f"Generated {gen.rows}x{gen.cols} maze with '{args.algo}' -> {args.output}")

    if args.solve or args.visual:
        maze = Maze(args.output)
        solver_name = args.solve if args.solve else "bfs"
        if solver_name == "bfs":
            sol = BFSSolver(maze)
        elif solver_name == "dfs":
            sol = DFSSolver(maze)
        elif solver_name == "dls":
            sol = DLSSolver(maze)
        elif solver_name == "iddfs":
            sol = IDDFSSolver(maze)
        else:
            sol = AStarSolver(maze)

        res = sol.solve()
        print(f"Solve [{solver_name.upper()}]: Found={res['found']} | Steps={res['path_length']} | Explored={res['nodes_explored']}")

        if args.visual:
            from src.visualization.renderer import Renderer
            renderer = Renderer(maze, res, solver_name.upper())
            renderer.run()

if __name__ == "__main__":
    main()
