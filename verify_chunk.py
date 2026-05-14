import json
from pathlib import Path

if __name__ == '__main__':
    try:
        data = json.loads(Path('graphify-out/.graphify_chunk_00.json').read_text(encoding='utf-8'))
        nodes = len(data.get('nodes', []))
        edges = len(data.get('edges', []))
        hyperedges = len(data.get('hyperedges', []))
        print(f'Semantic extraction chunk: {nodes} nodes, {edges} edges, {hyperedges} hyperedges')
    except FileNotFoundError:
        print('Chunk file not found - extracting from subagent output')
    except json.JSONDecodeError as e:
        print(f'JSON error: {e}')
