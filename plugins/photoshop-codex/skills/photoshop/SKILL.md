---
name: photoshop-integration-skill
description: 当用户需要调用本地 Photoshop 进行新建文档、添加图层、编辑文字、导出图片等自动操作时，使用此技能。该技能引导 Codex 如何调用 @your-company/photoshop-codex-mcp 提供的工具。
---

# Photoshop 智能操作指令技能

## 概述

此技能使 Codex 能够利用绑定的 Photoshop MCP 服务器直接操作用户的本地 Photoshop 客户端。它定义了设计自动化流程的指令规范、图层命名规范以及错误处理机制。

---

## 工作流程

### 1. 确认工具状态

在调用任何 Photoshop 工具前，确认 `photoshop` 命名空间下的工具集是否已成功加载。若未成功加载，请主动提示用户启动 Photoshop 软件或检查 UXP / 权限状态。

### 2. 图像设计与图层规范

在通过 MCP 新建或操作图层时，遵循以下命名和结构规范：
*   **背景图层**：统一命名为 `Background`，确保设定合适底色。
*   **文本图层**：所有新增的文字图层命名以文字内容或作用命名，如 `Text_Title` 或 `Text_CTA`。
*   **组/文件夹**：复杂排版建议使用组进行收纳，例如 `Group_Header`, `Group_Products`。

---

## 常用工具调用指南

根据用户要求选择合适的 MCP 接口工具：

*   **新建文档**：使用 `create_document` 并传入指定的 `width`, `height`, `resolution`。
*   **添加图层**：使用 `add_layer` 或 `add_solid_color_layer`。
*   **修改文本**：使用 `update_text_layer` 改变已有文本图层的内容、字体、字号与颜色。
*   **图层效果与变形**：使用 `apply_layer_transform` 进行缩放或平移。
*   **导出成果**：执行 `save_document` 或 `export_png`。

---

## 错误诊断与故障排除

当 MCP 工具返回错误码或操作超时，按以下逻辑自动诊断并引导用户：
1.  **Photoshop 未打开**：引导用户点击启动本地 Photoshop。
2.  **网络或端口冲突**：如果连接断开，引导用户检查 Photoshop Preferences 中的 Generator 远程连接密码或 UXP Agent 面板的连通状态。
3.  **不支持的格式**：如果文件无法读取，确认文档路径不含特殊字符或权限受阻。
