import requests

# Check corpus
r = requests.get('http://127.0.0.1:8000/query/corpus/info')
data = r.json()
print(f'Files in corpus: {len(data["files"])}')
for f in data['files']:
    print(f'  - {f["filename"]} ({f["file_type"]}) | {f["chunk_count"]} chunks')

# Test query
print()
print('Testing query...')
r = requests.post('http://127.0.0.1:8000/query/', json={'query': 'what format is this'}, timeout=60)
data = r.json()
print(f'Answer: {data["answer"][:300]}...')
print(f'Auto-enabled: {data.get("auto_full_document_enabled")}')
