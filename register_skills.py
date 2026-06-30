import os
import json

manifest_path = 'codex-skills/skills_manifest.json'

new_skills = [
    ("01_代码质量与规范", "git-workflow-skill", "Agent Skill for Git workflow best practices - branching, commits, PR workflows | Claude Code compatible"),
    ("07_GitHub与PR自动化", "mcp-github-pr-issue-analyser", "A Model Context Protocol (MCP) application for automated GitHub PR analysis and issue management."),
    ("04_开发规划与设计", "LLM-based-Multi-Agent-System-Architecture-Design-and-Project-Code-Practice", "LLM-based Multi-Agent 系统架构设计与项目代码实践"),
    ("12_任务与需求管理(Linear-Jira)", "mcp-linear", "MCP server that enables AI assistants to interact with Linear project management system through natural language"),
    ("15_财务发票提取与归档", "hk-finance-mcp-server", "An MCP server that provides access to finance related data in Hong Kong through a FastMCP interface."),
    ("48_Obsidian个人知识库管理", "obsidian-vault-mcp", "MCP tool allowing Open WebUI or Claude Desktop to retrieve files from your vault"),
    ("19_文件整理与清理工具", "File-Organizer-MCP", "This MCP server will organize your files using connections to MCP using clients like Claude, Cursor and Gemini Cli"),
    ("29_去AI味文本润色", "humanize-text", "Free open-source AI text humanizer to convert AI-generated content into undetectable, human-like writing.")
]

with open(manifest_path, 'r', encoding='utf-8') as f:
    skills = json.load(f)

for category, folder, desc in new_skills:
    relative_path = f"./{category}/{folder}"
    abs_dir = os.path.join('codex-skills', category, folder)
    skill_md_path = os.path.join(abs_dir, 'SKILL.md')
    
    # 1. Ensure SKILL.md exists and matches description exactly
    frontmatter = f"---\nname: {folder}\ndescription: {desc}\n---\n\n# {folder}\n\nSee README.md for details."
    
    # Write SKILL.md
    if os.path.exists(abs_dir):
        with open(skill_md_path, 'w', encoding='utf-8') as sf:
            sf.write(frontmatter)
    
    # 2. Append to manifest if not exists
    exists = False
    for s in skills:
        if s.get('relative_path') == relative_path:
            exists = True
            # update description to match
            s['description'] = desc
            s['name'] = folder
            break
            
    if not exists:
        skills.append({
            "name": folder,
            "description": desc,
            "category": category,
            "folder": folder,
            "relative_path": relative_path
        })

# Save manifest
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(skills, f, indent=4, ensure_ascii=False)

print("Registration complete.")
