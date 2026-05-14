#!/usr/bin/env python3
"""
One-click health check script for IntelliSearch V2.
Verifies:
1. Backend API /health endpoint
2. GitHub Models authentication (Foundry SDK)
3. Optional quick test query
"""

import subprocess
import sys
import json
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_backend_health(endpoint: str = "http://127.0.0.1:8000") -> dict:
    """Check /health endpoint"""
    import requests
    try:
        response = requests.get(f"{endpoint}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "OK",
                "endpoint": endpoint,
                "data": data
            }
        else:
            return {
                "status": "FAILED",
                "endpoint": endpoint,
                "error": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "endpoint": endpoint,
            "error": str(e)
        }

def check_github_models_auth() -> dict:
    """Check GitHub Models authentication using Foundry SDK"""
    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential
        from backend.app.config import settings
        
        token = settings.GITHUB_TOKEN_A or settings.GITHUB_TOKEN
        if not token:
            return {
                "status": "FAILED",
                "error": "No GitHub token configured (GITHUB_TOKEN not set)"
            }
        
        client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(token)
        )
        
        # Quick test completion
        response = client.complete(
            model="gpt-4.1",
            messages=[{"role": "user", "content": "Say 'OK'"}],
            temperature=0,
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            return {
                "status": "OK",
                "model": "gpt-4.1",
                "message": response.choices[0].message.content.strip()
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e)
        }

def check_query_endpoint(endpoint: str = "http://127.0.0.1:8000") -> dict:
    """Run a quick test query"""
    import requests
    from backend.app.config import settings
    
    try:
        client_key = settings.CLIENT_KEY
        if not client_key:
            return {
                "status": "SKIPPED",
                "reason": "CLIENT_KEY not configured"
            }
        
        response = requests.post(
            f"{endpoint}/query/",
            headers={
                "Content-Type": "application/json",
                "X-IntelliSearch-Client-Key": client_key
            },
            json={"query": "test"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "OK",
                "gate_passed": data.get("gate_passed"),
                "top_similarity": data.get("top_similarity"),
                "corpus_size": "available"
            }
        else:
            return {
                "status": "FAILED",
                "http_status": response.status_code,
                "error": response.text[:100]
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e)
        }

def print_result(title: str, result: dict, indent: int = 0) -> None:
    """Pretty print result"""
    prefix = "  " * indent
    status = result.get("status", "UNKNOWN")
    
    # Color codes
    if status == "OK":
        color = "\033[92m"  # Green
    elif status == "FAILED":
        color = "\033[91m"  # Red
    elif status == "SKIPPED":
        color = "\033[93m"  # Yellow
    else:
        color = "\033[94m"  # Blue
    
    reset = "\033[0m"
    
    print(f"{prefix}{title}")
    print(f"{prefix}  Status: {color}[{status}]{reset}")
    
    for key, value in result.items():
        if key != "status":
            if isinstance(value, (dict, list)):
                print(f"{prefix}  {key}: {json.dumps(value, indent=2).replace(chr(10), chr(10) + prefix + '    ')}")
            else:
                print(f"{prefix}  {key}: {value}")

def main():
    """Run all health checks"""
    print("\n" + "=" * 60)
    print("IntelliSearch V2 - Health Check")
    print("=" * 60 + "\n")
    
    results = {}
    
    # Check 1: Backend API
    print("1. Backend API Health...")
    results["backend"] = check_backend_health()
    print_result("Result", results["backend"], indent=1)
    print()
    
    if results["backend"]["status"] != "OK":
        print("\n⚠️  Backend is not responding. Cannot proceed with other checks.")
        print("   Make sure the backend is running: python -m uvicorn backend.app.main:app --port 8000\n")
        return 1
    
    # Check 2: GitHub Models Auth
    print("2. GitHub Models Authentication...")
    time.sleep(0.5)
    results["github_models"] = check_github_models_auth()
    print_result("Result", results["github_models"], indent=1)
    print()
    
    if results["github_models"]["status"] != "OK":
        print("\n⚠️  GitHub Models authentication failed.")
        print("   Ensure GITHUB_TOKEN is set with models:read permission.\n")
    
    # Check 3: Query Endpoint
    print("3. Query Endpoint (Test Query)...")
    time.sleep(0.5)
    results["query"] = check_query_endpoint()
    print_result("Result", results["query"], indent=1)
    print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_ok = all(r.get("status") == "OK" for r in results.values() if r.get("status") != "SKIPPED")
    
    if all_ok:
        print("\n✅ All checks passed! IntelliSearch V2 is healthy.\n")
        return 0
    else:
        print("\n❌ Some checks failed. Review the output above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
