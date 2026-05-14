import sys
import pathlib
import requests

project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from backend.app.config import settings

CLIENT_KEY = settings.CLIENT_KEY
URL = "http://127.0.0.1:8000/ingest/"
FILE_PATH = project_root / "IntelliSearch_V2_Complete_Dev_Guide.pdf"

with open(FILE_PATH, "rb") as f:
    files = {"file": (FILE_PATH.name, f, "application/pdf")}
    headers = {"X-IntelliSearch-Client-Key": CLIENT_KEY}
    resp = requests.post(URL, files=files, headers=headers, timeout=180)

print("STATUS", resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)
