import requests
import os

# Create a small test audio file (silent 1-second M4A)
# This is a minimal M4A file header for testing
test_audio = bytes([
    0xFF, 0xFB, 0x10, 0x00,  # MPEG-1 Layer III frame header
    0x00, 0x00, 0x00, 0x00
]) + b'\x00' * 200  # Padding for a minimal valid audio file

print("Testing audio upload with OpenAI Whisper fix...")
try:
    files = {'file': ('test_audio.m4a', test_audio)}
    r = requests.post('http://127.0.0.1:8000/ingest/', files=files, timeout=60)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Response: {data}")
except Exception as e:
    print(f"Error: {e}")
