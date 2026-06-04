---
name: photoshop-integration-skill
description: 当用户需要调用本地 Photoshop 进行设计操作时使用。该技能引导 Codex 在面对环境缺失、连接异常、工具失效等问题时进行动态自我诊断、自动生成 ExtendScript 修复方案或给用户清晰的操作提示，并在解决新问题后自主记录到本地知识库以实现自我进化。
---

# Photoshop 智能操作、故障诊断与自主进化技能

## 概述

此技能使 Codex 能够利用绑定的 Photoshop MCP 服务操作用户的 Photoshop 客户端。**此技能的核心目标是让 Codex 实现“越用越聪明”的自主学习闭环，在日常交互中主动记录并学习新问题的修复方法，而不是单纯依赖写死的 MCP 功能。**

---

## 🔍 1. 自主检索与知识库优先

在遇到任何 Photoshop 报错、功能受限、或接收到复杂制图指令时，Codex 必须：
1.  **优先检索本地知识库**：读取 `plugins/photoshop-codex/knowledge/` 目录下的 `README.md` 和各错误案例文件。
2.  **比对历史解决方案**：如果当前问题与历史记录中的报错（如 `ERR-PS-XXX`）相同或高度相似，**直接套用该记录中经验证有效的 ExtendScript 修复代码或操作规程**，不再重复尝试错误方案。

---

## 📝 2. 自学与自我记录闭环 (Self-Learning Loop)

当 Codex 遇到了此前知识库中**未记录的新错误**（例如某种特殊图层混合模式不支持、或某种新版本 PS 的脚本差异），并在与用户交互中**通过动态生成/修改 ExtendScript 成功解决了该问题**后，必须执行以下“自主进化”流程：

1.  **生成新案例文件**：在 `plugins/photoshop-codex/knowledge/` 下新建一个 Markdown 文件，命名格式为 `ERR-PS-顺序编号_问题简述.md`（如 `ERR-PS-002_blend_mode_fail.md`）。
2.  **套用规范模板**：将该问题的触发场景、报错日志、排查出的根本原因、以及成功执行的 JS/ExtendScript 核心代码写入该文件（参考 `knowledge/README.md` 中的模板）。
3.  **更新索引表格**：编辑 `plugins/photoshop-codex/knowledge/README.md`，在“历史解决案例索引”表格中新增一行，链接到新生成的案例文件。
4.  **自动提交本地 Git**：在终端执行 Git 命令，将新记录自动提交至本地仓库：
    ```bash
    git add plugins/photoshop-codex/knowledge/
    git commit -m "Codex Auto-learn: solved and recorded Photoshop error [ERR-PS-XXX]"
    ```
    *（通过自动提交，当用户下次向 GitHub 推送代码时，所有机器和客户都将自动共享并学习到该解决方案）*

---

## 🛠 3. MCP 工具失效时的“动态自愈”方案 (ExtendScript Fallback)

如果调用的 `photoshop` MCP 工具报错，Codex 应当启动“动态自愈”模式，自动生成 ExtendScript (.jsx) 作为替代执行方案：
1.  **动态生成脚本**：将未能通过 MCP 完成的操作转换成等效的 Photoshop JavaScript 代码。
2.  **生成临时文件并运行**：通过 Codex 的写文件与运行能力，帮助用户一键运行（在用户允许的情况下）：
    *   在工作空间新建一个 `temp_action.jsx` 文件。
    *   在终端使用命令行静默驱动 Photoshop 运行该脚本（macOS 示例）：
        ```bash
        osascript -e 'tell application "Adobe Photoshop" to do javascript file "/Users/zz/codexproject/temp_action.jsx"'
        ```
    *   执行完成后，自动删除临时文件 `temp_action.jsx`。

---

## 📘 4. 常见 Photoshop 运行期错误与修复提示词库

当 Photoshop 接口返回如下错误信息时，Codex 应自我翻译并向用户解释原因及解决方法：

*   **"No document open" (无打开文档)**：自动执行 `create_document` 新建默认画布，或提醒用户打开项目。
*   **"Layer is locked" (图层被锁定)**：先使用工具/脚本解除锁定，或复制图层再操作。
*   **"Target channel is not available" (目标通道不可用)**：提示用户转换色彩模式，或自动生成转换脚本。
