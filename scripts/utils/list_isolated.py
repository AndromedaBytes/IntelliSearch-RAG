import json
from pathlib import Path

def main():
    data = json.loads(Path('graphify-out/graph.json').read_text(encoding='utf-8'))
    nodes = {n['id']: n for n in data.get('nodes', [])}
    links = data.get('links', []) or data.get('edges', [])
    degree = {nid:0 for nid in nodes}
    for l in links:
        s = l.get('source')
        t = l.get('target')
        if isinstance(s, int):
            try:
                s = data['nodes'][s]['id']
            except:
                s = str(s)
        if isinstance(t, int):
            try:
                t = data['nodes'][t]['id']
            except:
                t = str(t)
        degree.setdefault(s,0); degree.setdefault(t,0)
        degree[s]+=1; degree[t]+=1
    isolated = [(nid, nodes[nid].get('label',''), nodes[nid].get('source_file','')) for nid,c in degree.items() if c<=1]
    isolated_sorted = sorted(isolated, key=lambda x:(x[2]=='' , x[2] or '', x[1]))
    print(len(isolated_sorted))
    for i,(nid,label,src) in enumerate(isolated_sorted[:60],1):
        print(f"{i:3}. {nid} | {label} | {src}")

if __name__ == '__main__':
    main()
