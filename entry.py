"""
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
