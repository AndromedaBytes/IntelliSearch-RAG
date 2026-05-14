import json
from pathlib import Path
import glob

if __name__ == '__main__':
    # Merge semantic chunks
    chunks = sorted(glob.glob('graphify-out/.graphify_chunk_*.json'))
    all_nodes, all_edges, all_hyperedges = [], [], []
    total_in, total_out = 0, 0
    
    for c in chunks:
        d = json.loads(Path(c).read_text(encoding='utf-8'))
        all_nodes += d.get('nodes', [])
        all_edges += d.get('edges', [])
        all_hyperedges += d.get('hyperedges', [])
        total_in += d.get('input_tokens', 0)
        total_out += d.get('output_tokens', 0)
    
    Path('graphify-out/.graphify_semantic_new.json').write_text(json.dumps({
        'nodes': all_nodes, 'edges': all_edges, 'hyperedges': all_hyperedges,
        'input_tokens': total_in, 'output_tokens': total_out,
    }, indent=2), encoding='utf-8')
    print(f'Merged {len(chunks)} chunks: {total_in:,} in / {total_out:,} out tokens')
    
    # Merge AST + semantic
    ast = json.loads(Path('graphify-out/.graphify_ast.json').read_text(encoding='utf-8'))
    sem = json.loads(Path('graphify-out/.graphify_semantic_new.json').read_text(encoding='utf-8'))
    
    seen = {n['id'] for n in ast['nodes']}
    merged_nodes = list(ast['nodes'])
    for n in sem['nodes']:
        if n['id'] not in seen:
            merged_nodes.append(n)
            seen.add(n['id'])
    
    merged_edges = ast['edges'] + sem['edges']
    merged_hyperedges = sem.get('hyperedges', [])
    merged = {
        'nodes': merged_nodes,
        'edges': merged_edges,
        'hyperedges': merged_hyperedges,
        'input_tokens': sem.get('input_tokens', 0),
        'output_tokens': sem.get('output_tokens', 0),
    }
    Path('graphify-out/.graphify_extract.json').write_text(json.dumps(merged, indent=2), encoding='utf-8')
    total = len(merged_nodes)
    edges = len(merged_edges)
    print(f'Merged: {total} nodes, {edges} edges ({len(ast["nodes"])} AST + {len(sem["nodes"])} semantic)')
