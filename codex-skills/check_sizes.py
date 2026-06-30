import json
import os

with open('/Users/zz/codexproject/codex-skills/skills_manifest.json') as f:
    skills = json.load(f)

flagged_names = [
    "codebase-migrate", "deploy-pipeline", "gh-fix-ci", "gh-address-comments",
    "pr-review-ci-fix", "mcp-builder", "sentry-triage", "webapp-testing",
    "issue-triage", "datadog-logs", "skill-creator", "skill-installer",
    "slack-gif-creator", "youtube-downloader"
]

for s in skills:
    if s['name'] in flagged_names:
        path = os.path.join('/Users/zz/codexproject/codex-skills', s['relative_path'])
        skill_md = os.path.join(path, 'SKILL.md')
        if os.path.exists(skill_md):
            size = os.path.getsize(skill_md)
            print(f"{s['name']}: SKILL.md size: {size} bytes")
            # print first 5 lines
            with open(skill_md) as f:
                content = f.read().splitlines()
                print("  " + "\n  ".join(content[:5]))
        else:
            print(f"{s['name']}: NO SKILL.md FOUND")
