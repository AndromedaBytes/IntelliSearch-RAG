import json
from pathlib import Path

if __name__ == '__main__':
    # Read with BOM handling
    try:
        data = json.loads(Path('graphify-out/.graphify_chunk_00.json').read_text(encoding='utf-8-sig'))
        # Rewrite without BOM
        Path('graphify-out/.graphify_chunk_00.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
        nodes = len(data.get('nodes', []))
        edges = len(data.get('edges', []))
        print(f'Semantic chunk fixed: {nodes} nodes, {edges} edges')
    except FileNotFoundError:
        print('Chunk file not found')
    except json.JSONDecodeError as e:
        print(f'JSON error: {e}')
    except Exception as e:
        print(f'Error: {e}')
