import sys
import pathlib
import requests
import json

# Ensure project root is on sys.path
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from backend.app.config import settings

CLIENT_KEY = settings.CLIENT_KEY
URL = "http://127.0.0.1:8000/query/"

payload = {"query": "What does the ingested document contain?"}
headers = {"X-IntelliSearch-Client-Key": CLIENT_KEY, "Content-Type": "application/json"}

resp = requests.post(URL, headers=headers, data=json.dumps(payload), timeout=60)
print("STATUS", resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)
