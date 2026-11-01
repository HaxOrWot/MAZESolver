"""
MAZESolver — Fast Launcher
==========================
Convenient root launcher allowing ultra-short CLI commands.

Examples:
  python run.py                # Visual solve on default 20x20 maze
  python run.py -c             # Compare all 5 algorithms
  python run.py -s             # Split-screen comparison view
  python run.py -e             # Open interactive maze editor
  python run.py 50             # Visual solve on 50x50 maze
  python run.py 100 astar      # Visual A* solve on 100x100 maze
  python run.py 40 dfs -t neon # Visual DFS on 40x40 maze with neon theme
"""
import sys
import os

# Insert project directory to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.main import main

if __name__ == "__main__":
    # Friendly positional parsing if user provides raw numbers/names:
    # e.g. 'python run.py 50' or 'python run.py 100 astar'
    args = sys.argv[1:]
    new_args = []
    i = 0
    while i < len(args):
        arg = args[i]
        # Check if arg is a standalone size number like '50' or '100' without flag
        if arg.isdigit() and (i == 0 or not args[i - 1].startswith("-")):
            new_args.extend(["-m", arg])
        # Check if arg is an algorithm name like 'astar' or 'bfs' without flag
        elif arg.lower() in ("bfs", "dfs", "dls", "iddfs", "astar") and (i == 0 or not args[i - 1].startswith("-")):
            new_args.extend(["-a", arg.lower()])
        else:
            new_args.append(arg)
        i += 1

    sys.argv = [sys.argv[0]] + new_args
    main()
