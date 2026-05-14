import sys
import pathlib
import requests

# Ensure project root is on sys.path so backend package imports work
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from backend.app.config import settings

CLIENT_KEY = settings.CLIENT_KEY
URL = "http://127.0.0.1:8000/ingest/"

with open("tmp_test_ingest.pdf", "rb") as f:
    files = {"file": ("tmp_test_ingest.pdf", f, "application/pdf")}
    headers = {"X-IntelliSearch-Client-Key": CLIENT_KEY}
    resp = requests.post(URL, files=files, headers=headers, timeout=120)

print("STATUS", resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)
