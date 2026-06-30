import json
import os

with open('/Users/zz/codexproject/codex-skills/skills_manifest.json') as f:
    skills = json.load(f)

flagged_names = [
    "mattpocock-skills", "xiaohongshu-hot-copywriter",
    "codebase-migrate", "deploy-pipeline", "gh-fix-ci", "gh-address-comments",
    "pr-review-ci-fix", "mcp-builder", "sentry-triage", "webapp-testing",
    "issue-triage", "datadog-logs", "skill-creator", "skill-installer",
    "slack-gif-creator", "youtube-downloader", "markitdown",
    "scientific-schematics", "scientific-visualization", "paper-search",
    "arxiv-latex-reader", "zotero-connector", "sympy-solver",
    "canghe-douyin-downloader", "canghe-manga-style-video", "paddleocr-doc-parsing"
]

for s in skills:
    if s['name'] in flagged_names:
        path = os.path.join('/Users/zz/codexproject/codex-skills', s['relative_path'])
        skill_md = os.path.join(path, 'SKILL.md')
        print(f"\n--- {s['name']} ---")
        if os.path.exists(skill_md):
            size = os.path.getsize(skill_md)
            print(f"SKILL.md size: {size} bytes")
            with open(skill_md) as f:
                content = f.read()
                print("--- START SKILL.md ---")
                print('\n'.join(content.splitlines()[:15]))
                print("--- END SKILL.md ---")
        else:
            print("NO SKILL.md FOUND")
            # List contents
            print(f"Directory contents: {os.listdir(path)}")
