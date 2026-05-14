import json
from pathlib import Path
from graphify.build import build_from_json
from graphify.cluster import score_all
from graphify.analyze import suggest_questions
from graphify.report import generate
from graphify.export import to_html

if __name__ == '__main__':
    extraction = json.loads(Path('graphify-out/.graphify_extract.json').read_text(encoding='utf-8'))
    detection  = json.loads(Path('graphify-out/.graphify_detect.json').read_text(encoding='utf-8'))
    analysis   = json.loads(Path('graphify-out/.graphify_analysis.json').read_text(encoding='utf-8'))

    G = build_from_json(extraction)
    communities = {int(k): v for k, v in analysis['communities'].items()}
    cohesion = {int(k): v for k, v in analysis['cohesion'].items()}
    tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}

    # Generate meaningful labels
    labels = {}
    gods = analysis['gods']
    
    for cid, nodes in communities.items():
        community_gods = [g for g in gods if g in nodes][:2]
        if community_gods:
            node_labels = [G.nodes[n].get('label', n) for n in community_gods]
            labels[cid] = ' & '.join(node_labels[:2]) if len(node_labels) > 1 else node_labels[0]
        else:
            if nodes:
                first_node = list(nodes)[0]
                labels[cid] = G.nodes[first_node].get('label', f'Module {cid}')
            else:
                labels[cid] = f'Community {cid}'

    # Regenerate questions with real labels
    questions = suggest_questions(G, communities, labels)

    # Generate report
    report = generate(G, communities, cohesion, labels, analysis['gods'], analysis['surprises'], detection, tokens, '.', suggested_questions=questions)
    Path('graphify-out/GRAPH_REPORT.md').write_text(report, encoding='utf-8')
    Path('graphify-out/.graphify_labels.json').write_text(json.dumps({str(k): v for k, v in labels.items()}, indent=2), encoding='utf-8')
    
    # Generate HTML visualization
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, 'graphify-out/graph.html', community_labels=labels)
        print('HTML visualization generated')
    else:
        print(f'Graph too large ({G.number_of_nodes()} nodes) for HTML - skipping visualization')
    
    print('Report updated with community labels')
