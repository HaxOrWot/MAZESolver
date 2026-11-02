# quick launcher for running commands easily
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.main import main

if __name__ == "__main__":
    # allows typing e.g. 'python run.py 50' or 'python run.py 100 astar'
    args = sys.argv[1:]
    new_args = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.isdigit() and (i == 0 or not args[i - 1].startswith("-")):
            new_args.extend(["-m", arg])
        elif arg.lower() in ("bfs", "dfs", "dls", "iddfs", "astar") and (i == 0 or not args[i - 1].startswith("-")):
            new_args.extend(["-a", arg.lower()])
        else:
            new_args.append(arg)
        i += 1

    sys.argv = [sys.argv[0]] + new_args
    main()
