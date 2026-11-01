"""
MAZESolver 2.0 — Unified Desktop & CLI Application Entry Point
==============================================================
If executed with command-line arguments: Runs standard CLI / visual mode.
If executed without arguments (e.g. double-clicked EXE): Launches interactive GUI Control Center.
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main():
    if len(sys.argv) > 1:
        # CLI invocation: pass to main runner
        from src.main import main as cli_main
        cli_main()
    else:
        # Double-clicked or launched with no args: launch interactive control hub
        from src.App.launcher_gui import LauncherGUI
        app = LauncherGUI()
        app.run()


if __name__ == "__main__":
    main()
