import os
import re

skills = {
    "Auto-Empirical-Research-Skills": {
        "name": "Auto-Empirical-Research-Skills",
        "description": "斯坦福团队自研的 23k+ 实证研究 Agent Skills 全家桶"
    },
    "StatsPAI": {
        "name": "StatsPAI",
        "description": "Agent-native 因果计量 Python 库，统一 API + 结构化输出"
    },
    "Awesome-Journal-Skills": {
        "name": "Awesome-Journal-Skills",
        "description": "期刊专用投稿技能包（AER/QJE/Nature 等）"
    },
    "AER-Skills": {
        "name": "AER-Skills",
        "description": "针对 AER 及 AEJ 系列的顶级期刊投稿技能栈"
    },
    "Auto-Research-Skills": {
        "name": "Auto-Research-Skills",
        "description": "自主科研技能与 Agent 精选库"
    }
}

base_dir = "codex-skills/15_社科研究与实证工具"

for folder, meta in skills.items():
    skill_path = os.path.join(base_dir, folder, "SKILL.md")
    
    frontmatter = f"---\nname: {meta['name']}\ndescription: {meta['description']}\n---\n"
    
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # check if it already has frontmatter
        if content.startswith("---"):
            # replace frontmatter
            content = re.sub(r"^---.*?---\n", frontmatter, content, flags=re.DOTALL)
        else:
            # prepend frontmatter
            content = frontmatter + "\n" + content
            
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        # Create new SKILL.md
        content = f"{frontmatter}\n# {meta['name']}\n\n{meta['description']}\n"
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content)

print("SKILL.md files fixed.")
