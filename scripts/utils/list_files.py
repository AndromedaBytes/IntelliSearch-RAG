import json
from pathlib import Path

# Get uncached files and create a chunk
detect = json.loads(Path('graphify-out/.graphify_uncached.txt').read_text(encoding='utf-8') if Path('graphify-out/.graphify_uncached.txt').exists() else '[]')
if isinstance(detect, str):
    uncached = detect.strip().split('\n') if detect.strip() else []
else:
    uncached = detect

# Filter to non-code files only
non_code_exts = {'.md', '.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp'}
non_code_files = [f for f in uncached if Path(f).suffix.lower() in non_code_exts or f.endswith('.md')]

print("Files for semantic extraction:")
for i, f in enumerate(non_code_files[:25], 1):
    print(f"{i:2}. {f}")

if len(non_code_files) > 25:
    print(f"\n... and {len(non_code_files) - 25} more files")
