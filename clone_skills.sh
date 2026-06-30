#!/bin/bash

# A script to clone and integrate new skills
cd codex-skills

clone_and_clean() {
    REPO=$1
    TARGET_DIR=$2
    if [ ! -d "$TARGET_DIR" ]; then
        git clone "https://github.com/$REPO.git" "$TARGET_DIR"
        rm -rf "$TARGET_DIR/.git" "$TARGET_DIR/.github"
    fi
}

clone_and_clean "yuyinws/ai-code-review-gitlab-plugin" "01_代码质量与规范/ai-code-review-gitlab-plugin"
clone_and_clean "saidsef/mcp-github-pr-issue-analyser" "07_GitHub与PR自动化/mcp-github-pr-issue-analyser"
clone_and_clean "AIGeniusInstitute/LLM-based-Multi-Agent-System-Architecture-Design-and-Project-Code-Practice" "04_开发规划与设计/LLM-based-Multi-Agent-System-Architecture-Design-and-Project-Code-Practice"
clone_and_clean "tacticlaunch/mcp-linear" "12_任务与需求管理(Linear-Jira)/mcp-linear"
clone_and_clean "hkopenai/hk-finance-mcp-server" "15_财务发票提取与归档/hk-finance-mcp-server"
clone_and_clean "ebullient/obsidian-vault-mcp" "48_Obsidian个人知识库管理/obsidian-vault-mcp"
clone_and_clean "kridaydave/File-Organizer-MCP" "19_文件整理与清理工具/File-Organizer-MCP"
clone_and_clean "lynote-ai/humanize-text" "29_去AI味文本润色/humanize-text"

echo "Cloning and cleaning complete."
