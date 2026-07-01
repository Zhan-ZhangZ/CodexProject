import json

with open("codex-skills/skills_manifest.json", "r") as f:
    manifest = json.load(f)

new_skills = [
    {
        "name": "Auto-Empirical-Research-Skills",
        "description": "斯坦福团队自研的 23k+ 实证研究 Agent Skills 全家桶",
        "category": "15_社科研究与实证工具",
        "folder": "Auto-Empirical-Research-Skills",
        "relative_path": "./15_社科研究与实证工具/Auto-Empirical-Research-Skills"
    },
    {
        "name": "StatsPAI",
        "description": "Agent-native 因果计量 Python 库，统一 API + 结构化输出",
        "category": "15_社科研究与实证工具",
        "folder": "StatsPAI",
        "relative_path": "./15_社科研究与实证工具/StatsPAI"
    },
    {
        "name": "Awesome-Journal-Skills",
        "description": "期刊专用投稿技能包（AER/QJE/Nature 等）",
        "category": "15_社科研究与实证工具",
        "folder": "Awesome-Journal-Skills",
        "relative_path": "./15_社科研究与实证工具/Awesome-Journal-Skills"
    },
    {
        "name": "AER-Skills",
        "description": "针对 AER 及 AEJ 系列的顶级期刊投稿技能栈",
        "category": "15_社科研究与实证工具",
        "folder": "AER-Skills",
        "relative_path": "./15_社科研究与实证工具/AER-Skills"
    },
    {
        "name": "Auto-Research-Skills",
        "description": "自主科研技能与 Agent 精选库",
        "category": "15_社科研究与实证工具",
        "folder": "Auto-Research-Skills",
        "relative_path": "./15_社科研究与实证工具/Auto-Research-Skills"
    }
]

# Avoid duplicates
existing_names = set(skill["name"] for skill in manifest)
for skill in new_skills:
    if skill["name"] not in existing_names:
        manifest.append(skill)

with open("codex-skills/skills_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write("\n")
