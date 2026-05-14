"""
Process orchestration launcher for IntelliSearch V2.
Manages ghost process cleanup and starts the Uvicorn server.
"""

import psutil
import subprocess
import sys
import time
import logging
import socket

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def kill_ghost_processes(port=8000):
    """Kill any existing processes listening on the specified port."""
    try:
        for proc in psutil.process_iter(["pid", "name", "connections"]):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        logger.info(f"Killing ghost process: PID {proc.pid} ({proc.name()})")
                        proc.terminate()
                        try:
                            proc.wait(timeout=2)
                        except psutil.TimeoutExpired:
                            proc.kill()
                            logger.info(f"Force killed PID {proc.pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except Exception as e:
        logger.warning(f"Could not kill ghost processes: {e}")


def wait_for_server(host="127.0.0.1", port=8000, timeout=15) -> bool:
    """Poll socket until server accepts connections."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def main():
    """Main entry point."""
    logger.info("Starting IntelliSearch V2...")
    
    # Kill any ghost processes
    kill_ghost_processes(port=8000)
    
    # Launch Uvicorn server
    logger.info("Launching Uvicorn server...")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app.main:app",
         "--host", "127.0.0.1", "--port", "8000", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Wait for server to be ready
    if wait_for_server():
        logger.info("✓ IntelliSearch V2 is online at http://127.0.0.1:8000")
    else:
        logger.error("✗ Server failed to start within timeout")
        process.terminate()
        sys.exit(1)
    
    try:
        process.wait()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        process.terminate()
        process.wait(timeout=5)


if __name__ == "__main__":
    main()
