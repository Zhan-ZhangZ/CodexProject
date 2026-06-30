import json
import os

with open('/Users/zz/codexproject/codex-skills/skills_manifest.json') as f:
    skills = json.load(f)

problematic = []

for s in skills:
    path = os.path.join('/Users/zz/codexproject/codex-skills', s['relative_path'])
    if not os.path.exists(path):
        problematic.append(f"{s['name']}: Directory does not exist")
        continue
    
    files = os.listdir(path)
    # Ignore hidden files
    visible_files = [f for f in files if not f.startswith('.')]
    
    # Check if README exists
    has_readme = any(f.lower().startswith('readme') for f in visible_files)
    has_claude = any(f.lower().startswith('claude') for f in visible_files)
    
    # If the directory only has SKILL.md, or very few files and no README/src
    if len(visible_files) <= 1:
        problematic.append(f"{s['name']}: Only contains {visible_files}")
    elif not has_readme and not has_claude:
        # Check if there are any directories
        has_dir = any(os.path.isdir(os.path.join(path, f)) for f in visible_files)
        if not has_dir:
             problematic.append(f"{s['name']}: No README/CLAUDE and no subdirectories. Files: {visible_files}")
        else:
             # Still suspicious if no README
             problematic.append(f"{s['name']}: No README/CLAUDE. Files: {visible_files}")

print("Problematic Skills found:")
for p in problematic:
    print(p)

if not problematic:
    print("None found!")
