---
name: photoshop-integration-skill
description: 当用户需要调用本地 Photoshop 进行设计操作时使用。该技能引导 Codex 在面对环境缺失、连接异常、工具失效等问题时进行动态自我诊断、自动生成 ExtendScript 修复方案或给用户清晰的操作提示。
---

# Photoshop 智能操作与故障诊断技能

## 概述

此技能使 Codex 能够利用绑定的 Photoshop MCP 服务操作用户的 Photoshop 客户端。**当环境、连接或工具调用出现异常时，Codex 应使用本指南进行自我诊断，并动态生成补充解决方案或操作引导。**

---

## 🔍 环境自检与动态诊断指南

当用户反馈“无法使用”、“连接断开”或 MCP 服务抛出错误时，Codex 应执行以下诊断链（可通过终端命令临时验证，无须依赖静态脚本）：

### 1. 确认 Node.js 与 npx 环境
*   **诊断行为**：在必要时静默或引导用户确认 Node.js 安装。
*   **修复引导**：如果环境缺乏 Node，告知用户：“本地未检测到 Node.js，Photoshop 插件市场需要 Node.js 环境以启动本地 MCP 通信桥梁，请前往 https://nodejs.org/ 安装。”

### 2. 检查 Photoshop 进程状态
*   **诊断命令 (macOS)**：执行以下命令检测 PS 运行状态：
    ```bash
    osascript -e 'application "Adobe Photoshop" is running'
    ```
*   **自愈提示**：若返回 `false` 或报错，直接对用户说：“请先启动您的本地 Photoshop，然后再执行此设计指令。”

### 3. 检查 macOS 自动化授权 (Automation Permissions)
*   **诊断命令**：尝试获取 PS 版本：
    ```bash
    osascript -e 'tell application "Adobe Photoshop" to get name'
    ```
*   **权限修复提示**：如果上述命令返回错误（如 `Not authorized to send Apple events`），说明系统权限受限。引导用户执行以下操作：
    > ⚠️ **权限不足**：请前往 **系统设置 -> 隐私与安全性 -> 自动化**，勾选允许 **Terminal**（或 **Codex**）控制 **Adobe Photoshop**。

---

## 🛠 MCP 工具失效时的“动态自愈”方案 (ExtendScript Fallback)

如果调用的 `photoshop` MCP 工具报错（例如“不支持该滤镜”、“图层锁定”、“当前动作不可用”），**不要直接向用户报错。** Codex 应当启动“动态自愈”模式，自动生成 ExtendScript (.jsx) 作为替代执行方案：

1.  **动态生成脚本**：将未能通过 MCP 完成的操作转换成等效的 Photoshop JavaScript 代码。
2.  **生成临时文件并运行**：通过 Codex 的写文件与运行命令能力，帮助用户一键运行（如果在用户允许的情况下）：
    *   在工作空间新建一个 `temp_action.jsx` 文件。
    *   在终端使用命令行静默驱动 Photoshop 运行该脚本（macOS 示例）：
        ```bash
        osascript -e 'tell application "Adobe Photoshop" to do javascript file "/Users/zz/codexproject/temp_action.jsx"'
        ```
    *   执行完成后，自动删除临时文件 `temp_action.jsx`。

---

## 📘 常见 Photoshop 运行期错误与修复提示词库

当 Photoshop 接口返回如下错误信息时，Codex 应自我翻译并向用户解释原因及解决方法：

*   **"No document open" (无打开文档)**：
    *   *理解*：当前没有任何图片或画布在 PS 中处于活动状态。
    *   *自愈*：自动执行 `create_document` 工具新建一个默认画布，或友好提醒用户打开一个项目。
*   **"Layer is locked" (图层被锁定)**：
    *   *理解*：试图修改背景图层或已加锁的图层。
    *   *自愈*：使用 MCP 工具解除锁定，或者先复制该图层为新图层再操作。
*   **"Target channel is not available" (目标通道不可用)**：
    *   *理解*：色彩模式与操作不符（例如在 CMYK 模式下执行只支持 RGB 的滤镜）。
    *   *自愈*：提示用户转换色彩模式，或自动生成转换脚本。
