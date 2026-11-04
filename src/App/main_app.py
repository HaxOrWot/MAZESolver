# unified entry point: GUI if no args, CLI if args passed
import sys
import os

if getattr(sys, "frozen", False):
    PROJECT_ROOT = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    if len(sys.argv) > 1:
        if sys.platform == "win32":
            try:
                import ctypes
                if ctypes.windll.kernel32.AttachConsole(-1):
                    sys.stdout = open("CONOUT$", "w", encoding="utf-8")
                    sys.stderr = open("CONOUT$", "w", encoding="utf-8")
            except Exception:
                pass
        from src.main import main as cli_main
        cli_main()
    else:
        from src.App.launcher_gui import LauncherGUI
        app = LauncherGUI()
        app.run()

if __name__ == "__main__":
    main()
