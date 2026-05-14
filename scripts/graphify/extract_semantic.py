import json
from pathlib import Path

if __name__ == '__main__':
    # Read the raw subagent response
    response_file = Path(r'c:\Users\saran\AppData\Roaming\Code\User\workspaceStorage\9e90926b90d2601cafc837d2a8eb1050\GitHub.copilot-chat\chat-session-resources\b8ca4cd1-ddd6-4a97-9fc8-0f1f88a647b8\toolu_bdrk_01Vf5CCw6uPV3MNPqsHPEM3C__vscode-1777951592518\content.txt')
    
    if response_file.exists():
        content = response_file.read_text(encoding='utf-8')
        
        # Extract JSON from markdown code fences
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            try:
                data = json.loads(json_str)
                # Save to chunk file
                Path('graphify-out/.graphify_chunk_00.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
                print(f'Extracted semantic chunk: {len(data.get("nodes", []))} nodes, {len(data.get("edges", []))} edges')
            except json.JSONDecodeError as e:
                print(f'JSON parse error: {e}')
        else:
            print('Could not find JSON in response')
    else:
        print('Response file not found')
