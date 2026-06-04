---
name: photoshop-integration-skill
description: 当用户需要调用本地 Photoshop 进行新建文档、添加图层、编辑文字、导出图片等自动操作时，使用此技能。该技能引导 Codex 如何调用 @your-company/photoshop-codex-mcp 提供的工具。
---

# Photoshop 智能操作指令技能

## 概述

此技能使 Codex 能够利用绑定的 Photoshop MCP 服务器直接操作用户的本地 Photoshop 客户端。它定义了设计自动化流程的指令规范、环境自检规范以及错误处理机制。

---

## 工作流程

### 1. 环境诊断与自检 (Environment Diagnosis)

*   **首次载入时**：或者当用户反馈“无法连接 Photoshop”、“找不到工具”时，请主动调用终端运行插件目录下的脚本：
    ```bash
    ./scripts/diagnose.sh
    ```
*   **诊断分析**：
    *   若脚本返回 `Node.js FAILED`：提示用户安装 Node.js。
    *   若脚本返回 `Photoshop is not running FAILED`：友情提示用户打开本地 Photoshop 软件。
    *   若脚本返回 `Automation Permissions FAILED`：以醒目的 Markdown 警告提示用户授予“系统设置 -> 隐私与安全性 -> 自动化”中的 Terminal/Codex 控制 Photoshop 的权限。

---

### 2. 图像设计与图层规范

在通过 MCP 新建或操作图层时，遵循以下命名和结构规范：
*   **背景图层**：统一命名为 `Background`，确保设定合适底色。
*   **文本图层**：所有新增的文字图层命名以文字内容或作用命名，如 `Text_Title` 或 `Text_CTA`。
*   **组/文件夹**：复杂排版建议使用组进行收纳，例如 `Group_Header`, `Group_Products`。

---

### 3. 常用工具调用指南

根据用户要求选择合适的 MCP 接口工具：

*   **新建文档**：使用 `create_document` 并传入指定的 `width`, `height`, `resolution`。
*   **添加图层**：使用 `add_layer` 或 `add_solid_color_layer`。
*   **修改文本**：使用 `update_text_layer` 改变已有文本图层的内容、字号与颜色。
*   **图层效果与变形**：使用 `apply_layer_transform` 进行缩放或平移。
*   **导出成果**：执行 `save_document` 或 `export_png`。
