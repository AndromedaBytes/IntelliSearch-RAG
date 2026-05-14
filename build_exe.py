"""
PyInstaller build script for IntelliSearch V2 Windows .exe
Bundles backend (FastAPI + ChromaDB) with frontend (Next.js static build)
Creates single-file, double-clickable .exe for users
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run shell command and return success status"""
    print(f"\n{'='*60}")
    # Resolve npm through the Windows shim, but keep direct execution for other tools.
    if os.name == 'nt' and cmd and cmd[0] == 'npm':
        cmd = ['npm.cmd', *cmd[1:]]

    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=cwd)

    return result.returncode == 0


def main():
    project_root = Path(__file__).parent
    
    # Step 1: Build frontend
    print("\n[1/4] Building Next.js frontend...")
    if not run_command(
        [sys.executable, "-m", "pip", "list"],  # Verify pip works
        cwd=project_root / "frontend"
    ):
        print("Frontend setup check failed")
    
    # Install frontend deps
    if not run_command(
        ["npm", "install"],
        cwd=project_root / "frontend"
    ):
        print("⚠ Frontend npm install had issues, continuing...")
    
    # Build frontend
    if not run_command(
        ["npm", "run", "build"],
        cwd=project_root / "frontend"
    ):
        print("⚠ Frontend build had issues, continuing...")
    
    # Step 2: Create entry point script
    print("\n[2/4] Creating entry point script...")
    entry_script = project_root / "entry.py"
    entry_script.write_text('''"""
IntelliSearch V2 - Windows .exe Entry Point
Starts FastAPI backend and serves Next.js frontend
"""

import codecs
import os
import sys
import threading
import webbrowser
import time
import socket
from pathlib import Path

if sys.stdout is not None and getattr(sys.stdout, "encoding", None) != "utf-8":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
if sys.stderr is not None and getattr(sys.stderr, "encoding", None) != "utf-8":
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

# Setup paths for frozen executable
if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

# Add app root to path so backend can be imported
sys.path.insert(0, app_path)

# Change to app directory
os.chdir(app_path)

def check_port_available(port=8000, timeout=15):
    """Poll until port is ready"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        time.sleep(0.5)
    return False


def run_backend():
    """Start FastAPI backend"""
    try:
        from uvicorn import run
        from backend.app.main import app
        run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(f"Backend startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    # Setup error logging
    if getattr(sys, 'frozen', False):
        app_path = sys._MEIPASS
    else:
        app_path = os.path.dirname(os.path.abspath(__file__))
    
    log_file = os.path.join(app_path, 'app_startup.log')
    try:
        log_handle = open(log_file, 'w')
        sys.stdout = log_handle
        sys.stderr = log_handle
    except:
        pass  # If logging fails, continue anyway
    
    print("Starting IntelliSearch V2...")
    print(f"App path: {app_path}")
    print(f"sys.path: {sys.path}")
    print(f"sys.frozen: {getattr(sys, 'frozen', False)}")
    
    # Start backend in daemon thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to be ready
    print("Waiting for backend to start...")
    if check_port_available():
        print("Backend ready!")
        
        # Open browser
        print("Opening browser...")
        time.sleep(0.5)
        webbrowser.open("http://127.0.0.1:8000")
        
        # Keep app running
        try:
            backend_thread.join()
        except KeyboardInterrupt:
            print("Shutting down...")
            sys.exit(0)
    else:
        print("Backend failed to start")
        sys.exit(1)


if __name__ == "__main__":
    main()
''', encoding='utf-8')
    
    # Step 3: Build with PyInstaller
    print("\n[3/4] Building .exe with PyInstaller...")
    
    # Remove old build artifacts
    for path in [project_root / "build", project_root / "dist"]:
        if path.exists():
            shutil.rmtree(path)
    
    pyinstaller_args = [
        "pyinstaller",
        "--name", "IntelliSearch-V2",
        "--onedir",
        "--windowed",
    ]

    # Optionally add icon
    icon_path = project_root / "assets" / "icon.ico"
    if icon_path.exists():
        pyinstaller_args += ["--icon", str(icon_path)]

    # Include frontend static export if available
    frontend_out = project_root / 'frontend' / 'out'
    if frontend_out.exists():
        pyinstaller_args += ["--add-data", f"{frontend_out}{os.pathsep}frontend/out"]
    else:
        print("⚠ frontend/out not found — skipping adding frontend static files to PyInstaller")

    # Include backend package
    pyinstaller_args += ["--add-data", f"{project_root / 'backend'}{os.pathsep}backend"]

    # Include .env if present so packaged backend can load configuration
    env_path = project_root / ".env"
    if env_path.exists():
        pyinstaller_args += ["--add-data", f"{env_path}{os.pathsep}."]

    # Hidden imports and collections
    pyinstaller_args += [
        "--hidden-import", "chromadb",
        "--hidden-import", "chromadb.utils.embedding_functions",
        "--hidden-import", "tqdm",
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--collect-all", "chromadb",
        "--collect-all", "tqdm",
        "--collect-all", "tiktoken",
        str(entry_script)
    ]

    pyinstaller_command = [sys.executable, "-m", "PyInstaller", *pyinstaller_args[1:]]

    if not run_command(pyinstaller_command):
        print("✗ PyInstaller build failed")
        sys.exit(1)
    
    # Step 4: Verify build
    print("\n[4/4] Verifying build...")
    dist_dir = project_root / "dist" / "IntelliSearch-V2"
    exe_path = dist_dir / "IntelliSearch-V2.exe"
    
    if exe_path.exists():
        print(f"\n[SUCCESS] Build successful!")
        print(f"[DIST] Directory: {dist_dir}")
        print(f"[EXE] Executable: {exe_path}")
        print(f"\n[READY] Ready to distribute! (folder-based bundle)")
    else:
        print(f"[ERROR] Build failed - .exe not found at {exe_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()

