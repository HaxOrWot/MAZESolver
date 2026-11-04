# pyinstaller build script to make standalone MAZESolver.exe
import os
import shutil
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP_DIR = os.path.join(PROJECT_ROOT, "src", "App")
ENTRY_POINT = os.path.join(APP_DIR, "main_app.py")

def build():
    print("=" * 60)
    print("Building Standalone MAZESolver.exe (Windowed / No CMD Window)...")
    print("=" * 60)

    dist_dir = os.path.join(APP_DIR, "dist")
    build_dir = os.path.join(APP_DIR, "build")

    # Clean existing build/dist artifacts
    for d in [dist_dir, build_dir]:
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)
    spec_path = os.path.join(PROJECT_ROOT, "MAZESolver.spec")
    if os.path.exists(spec_path):
        try:
            os.remove(spec_path)
        except Exception:
            pass

    sep = ";" if sys.platform.startswith("win") else ":"
    icon_path = os.path.join(PROJECT_ROOT, "assets", "icons", "app_icon.ico")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=MAZESolver",
        "--onefile",
        "--noconsole",
        "--clean",
        f"--paths={PROJECT_ROOT}",
        f"--icon={icon_path}",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        f"--add-data={os.path.join(PROJECT_ROOT, 'data')}{sep}data",
        f"--add-data={os.path.join(PROJECT_ROOT, 'assets')}{sep}assets",
        f"--add-data={os.path.join(PROJECT_ROOT, 'config.json')}{sep}.",
        "--collect-submodules=src",
        "--hidden-import=src.visualization.split_view",
        "--hidden-import=src.visualization.renderer",
        "--hidden-import=src.visualization.themes",
        "--hidden-import=src.editor.maze_editor",
        "--hidden-import=pygame",
        "--hidden-import=PIL",
        "--hidden-import=numpy",
        ENTRY_POINT,
    ]

    print("Running command:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if res.returncode == 0:
        exe_src = os.path.join(dist_dir, "MAZESolver.exe")
        exe_dest = os.path.join(APP_DIR, "MAZESolver.exe")
        if os.path.exists(exe_src):
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/f", "/im", "MAZESolver.exe"], capture_output=True)
            shutil.copy2(exe_src, exe_dest)
            print("\n" + "=" * 60)
            print(f"SUCCESS! Executable built and copied to:")
            print(f"  -> {exe_dest}")
            print(f"File size: {os.path.getsize(exe_dest) / (1024*1024):.2f} MB")
            print("=" * 60)
    else:
        print("Build failed with return code:", res.returncode)

if __name__ == "__main__":
    build()
