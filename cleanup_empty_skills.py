import json
import os
import shutil

manifest_path = 'codex-skills/skills_manifest.json'

with open(manifest_path, 'r', encoding='utf-8') as f:
    skills = json.load(f)

valid_extensions = {'.py', '.js', '.ts', '.sh', '.rs', '.go', '.c', '.cpp', '.h', '.java', '.php', '.rb', '.tsx', '.jsx'}
skills_to_keep = []
removed_count = 0

for s in skills:
    rel = s.get('relative_path', '')
    rel_clean = rel.lstrip('./')
    abs_path = os.path.join('codex-skills', rel_clean)
    
    has_code = False
    if os.path.exists(abs_path) and os.path.isdir(abs_path):
        for root, dirs, files in os.walk(abs_path):
            for fn in files:
                if not fn.startswith('.'):
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in valid_extensions:
                        has_code = True
                        break
            if has_code:
                break
        
        if not has_code:
            print(f"Removing empty skill: {s['name']} at {abs_path}")
            shutil.rmtree(abs_path)
            removed_count += 1
        else:
            skills_to_keep.append(s)
    else:
        print(f"Directory not found, removing entry: {s['name']}")
        removed_count += 1

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(skills_to_keep, f, indent=4, ensure_ascii=False)

print(f"\nCleanup complete. Removed {removed_count} skills. Kept {len(skills_to_keep)} skills.")
