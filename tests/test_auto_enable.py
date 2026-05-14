import requests

# Check corpus files
r = requests.get('http://127.0.0.1:8000/query/corpus/info')
data = r.json()
print(f'Total files: {len(data["files"])}')
for f in data['files']:
    print(f'  {f["filename"]} ({f["file_type"]}) - {f["chunk_count"]} chunks')

# Test query with full_document_mode=false
print('\n--- Testing auto-enable (sending full_document_mode=false) ---')
payload = {
    'query': 'what is the project about',
    'full_document_mode': False
}
r = requests.post('http://127.0.0.1:8000/query/', json=payload, timeout=180)
print(f'Status: {r.status_code}')
data = r.json()
print(f'Analysis mode detected: {"full_document" if data.get("auto_full_document_enabled") else "retrieval"}')
print(f'Auto-enabled: {data.get("auto_full_document_enabled")}')
print(f'Answer preview: {data["answer"][:150]}...')
