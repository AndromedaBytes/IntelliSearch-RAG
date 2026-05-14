import json
from pathlib import Path
from graphify.build import build_from_json

if __name__ == '__main__':
    extraction = json.loads(Path('graphify-out/.graphify_extract.json').read_text(encoding='utf-8'))
    analysis   = json.loads(Path('graphify-out/.graphify_analysis.json').read_text(encoding='utf-8'))
    
    G = build_from_json(extraction)
    communities = {int(k): v for k, v in analysis['communities'].items()}
    
    # Generate labels based on top god nodes in each community
    labels = {}
    gods = analysis['gods']
    
    for cid, nodes in communities.items():
        # Get top god nodes in this community
        community_gods = [g for g in gods if g in nodes][:2]
        
        if community_gods:
            # Use god node labels to name the community
            node_labels = [G.nodes[n].get('label', n) for n in community_gods]
            labels[cid] = ' & '.join(node_labels[:2]) if len(node_labels) > 1 else node_labels[0]
        else:
            # Fallback: use any node in the community
            if nodes:
                first_node = list(nodes)[0]
                labels[cid] = G.nodes[first_node].get('label', f'Module {cid}')
            else:
                labels[cid] = f'Community {cid}'
    
    print(f'Generated labels for {len(labels)} communities:')
    for cid in sorted(labels.keys())[:10]:
        print(f'  Community {cid}: {labels[cid]}')
    if len(labels) > 10:
        print(f'  ... and {len(labels)-10} more')
