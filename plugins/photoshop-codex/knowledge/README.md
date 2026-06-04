# Photoshop for Codex 错误与解决方案自愈知识库

这是一个由 AI 智能体（Codex）在日常运行中**自我记录、自我学习与演进**的知识库。当在使用 Photoshop MCP 服务或编写 ExtendScript 时遇到错误并最终成功解决，Codex 会自动将诊断日志、根本原因和经证实有效的代码记录在此，以便后续自动检索与复用。

---

## 🔍 历史解决案例索引 (Auto-Indexed Solved Cases)

| 案例 ID | 问题现象 | 核心根源 | 验证状态 | 解决方案链接 |
| :--- | :--- | :--- | :--- | :--- |
| `ERR-PS-001` | 样例：文本图层字体缺失报错 | 本机未安装指定字体 | `已自动验证` | [ERR-PS-001_font_not_found.md](./ERR-PS-001_font_not_found.md) |

---

## 📝 自我记录规范与模板 (Self-Recording Template)

当 Codex 成功解决了一个 Photoshop 操作问题时，需使用此模板在 `knowledge/` 下生成一个新的 Markdown 记录（如 `ERR-PS-XXX_symptom.md`），并自动更新本索引表格。

```markdown
### [ERR-PS-XXX] 错误/优化名称

- **触发场景**: [如：在批量导出 PNG 过程、添加特定特效图层]
- **错误日志/表现**: 
  ```text
  [此处粘贴核心报错信息或表现]
  ```
- **根本原因 (Root Cause)**: 
  [解释为何会出现该错误，如色彩空间限制、画布越界、图层锁死、ExtendScript 引擎兼容问题等]
- **经验证可行的解决方案 (Solution)**:
  1. [描述具体操作或修复参数]
  2. [粘贴成功执行的 ExtendScript 核心代码或 MCP 调用参数]
- **验证状态**: `已自动验证`
```
