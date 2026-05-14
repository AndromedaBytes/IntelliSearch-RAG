"""
Doctor script for IntelliSearch V2 system diagnostics
Validates environment, dependencies, and configuration
"""

import sys
import subprocess
from pathlib import Path
import os


class Doctor:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
    
    def check(self, name, condition, details=""):
        """Record a check result"""
        status = "✓ PASS" if condition else "✗ FAIL"
        self.checks.append((name, condition, details))
        
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        
        print(f"  {status}: {name}")
        if details:
            print(f"       {details}")
    
    def section(self, title):
        """Print section header"""
        print(f"\n{title}")
        print("=" * 50)
    
    def run_diagnostics(self):
        """Run all diagnostic checks"""
        print("\n" + "=" * 50)
        print("IntelliSearch V2 — System Doctor")
        print("=" * 50)
        
        # Python Version
        self.section("🐍 Python Environment")
        py_version = sys.version_info
        self.check(
            "Python 3.10+",
            py_version >= (3, 10),
            f"Found: {py_version.major}.{py_version.minor}.{py_version.micro}"
        )
        
        # Dependencies
        self.section("📦 Python Dependencies")
        deps = [
            "fastapi", "uvicorn", "openai", "chromadb",
            "pydantic", "pydantic_settings", "pytest", "httpx"
        ]
        for dep in deps:
            try:
                __import__(dep)
                self.check(f"{dep}", True)
            except ImportError:
                self.check(f"{dep}", False, "Not installed - run: pip install -r requirements.txt")
        
        # .env Configuration
        self.section("⚙️  Configuration")
        env_file = Path(".env")
        self.check(".env file exists", env_file.exists())
        
        if env_file.exists():
            content = env_file.read_text()
            has_single = "GITHUB_TOKEN=" in content
            has_token_a = "GITHUB_TOKEN_A=" in content
            has_token_b = "GITHUB_TOKEN_B=" in content
            self.check(
                "GitHub token configured",
                has_single or (has_token_a and has_token_b),
                "Use GITHUB_TOKEN or both GITHUB_TOKEN_A + GITHUB_TOKEN_B"
            )
            self.check("CLIENT_KEY set", "CLIENT_KEY=" in content)
        
        # Ports
        self.section("🌐 Network")
        import socket
        try:
            sock = socket.socket()
            sock.bind(('127.0.0.1', 8000))
            sock.close()
            self.check("Port 8000 available", True)
        except OSError:
            self.check("Port 8000 available", False, "Port already in use")
        
        # File System
        self.section("📁 File System")
        project_root = Path(__file__).parent.parent
        required_dirs = [
            project_root / "backend" / "app",
            project_root / "frontend",
            project_root / "tests",
        ]
        for d in required_dirs:
            self.check(f"{d.relative_to(project_root)} exists", d.exists())
        
        # External Tools
        self.section("🛠️  External Tools")
        
        # ffmpeg
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            self.check("ffmpeg installed", True)
        except:
            self.check("ffmpeg installed", False, "Required for audio processing")
        
        # Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, check=True, text=True)
            version = result.stdout.strip()
            self.check(f"Node.js installed", True, f"Version: {version}")
        except:
            self.check("Node.js installed", False, "Required for frontend build")
        
        # Docker
        try:
            subprocess.run(["docker", "--version"], capture_output=True, check=True)
            self.check("Docker installed", True)
        except:
            self.check("Docker installed", False, "Optional - for containerization")
        
        # Summary
        self.section("📊 Summary")
        total = self.passed + self.failed
        health_score = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\nHealth Score: {health_score:.0f}% ({self.passed}/{total})")
        
        if self.failed > 0:
            print(f"\n⚠️  {self.failed} issue(s) detected:")
            for name, passed, details in self.checks:
                if not passed:
                    print(f"  • {name}")
                    if details:
                        print(f"    → {details}")
            
            # Suggest most impactful fix
            print(f"\n💡 Next step:")
            if not subprocess.run(["python", "-c", "import fastapi"], capture_output=True).returncode == 0:
                print("  1. Install Python dependencies:")
                print("     pip install -r requirements.txt")
            elif not Path(".env").exists():
                print("  1. Create .env configuration:")
                print("     cp .env.example .env")
                print("     # Edit .env with your GitHub tokens")
            else:
                print("  1. Run the development server:")
                print("     python run.py")
        else:
            print("✅ All systems operational!")
        
        return self.failed == 0


if __name__ == "__main__":
    doctor = Doctor()
    success = doctor.run_diagnostics()
    sys.exit(0 if success else 1)
