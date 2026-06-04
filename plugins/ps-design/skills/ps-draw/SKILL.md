---
name: ps-design-assistant
description: 当用户需要 Photoshop (PS) 脚本自动处理图像、布局排版建议、快捷键查询或批量切片导出时，使用此技能。
---

# PS 制图与设计助手技能

## 概述

此技能能够协助用户在 Photoshop (PS) 中进行高效设计。其核心能力是生成 Photoshop ExtendScript (.jsx) 自动化脚本、提供主流尺寸排版建议、解答 PS 快捷键与高频操作步骤。

---

## 工作流程

### 1. Photoshop 脚本生成 (ExtendScript)

当用户提出“批量裁剪”、“新建多图层”、“导出切片”或“批量加水印”等自动化需求时，为用户编写 ExtendScript (JavaScript) 脚本。

#### 脚本编写规范：
*   **单位设置**：脚本开头必须包含设置标尺单位为像素 (Pixels) 的代码，并在结束时恢复。
*   **容错处理**：检查当前是否有打开的文档。
*   **中文注释**：关键逻辑必须附带中文注释，说明该段代码在 PS 中执行的具体效果。
*   **使用引导**：在输出的脚本代码下方，必须附带说明如何运行该脚本：
    1.  将代码保存为 `filename.jsx` 文件。
    2.  打开 Photoshop，点击菜单栏：**文件 (File) -> 脚本 (Scripts) -> 浏览 (Browse...)**。
    3.  选择刚刚保存的 `.jsx` 文件运行。

---

### 2. 常用设计尺寸与排版建议

当用户询问特定场景的设计规范时，提供以下参考：

| 场景 | 推荐分辨率/色彩模式 | 常用尺寸 (像素) |
| :--- | :--- | :--- |
| **手机海报** | 72 DPI, RGB | `1080 x 1920` |
| **电商主图** | 72 DPI, RGB | `800 x 800` 或 `1000 x 1000` (1:1) |
| **网页横幅 (Banner)**| 72 DPI, RGB | `1920 x 400` / `1200 x 400` |
| **打印海报** | 300 DPI, CMYK | A3 (`3508 x 4960`) / A4 (`2480 x 3508`) |

---

### 3. 高频快捷键与工具速查

当用户询问如何快速选择工具或执行命令时，给出对应的快捷键（同时提供 macOS 和 Windows 版本）：
*   **自由变换**：`Cmd + T` (Mac) / `Ctrl + T` (Win)
*   **新建图层**：`Cmd + Shift + N` (Mac) / `Ctrl + Shift + N` (Win)
*   **盖印所有可见图层**：`Cmd + Option + Shift + E` (Mac) / `Ctrl + Alt + Shift + E` (Win)
*   **快速导出为 PNG**：`Cmd + Option + Shift + S` (Mac) / `Ctrl + Alt + Shift + S` (Win)

---

## 示例回答模板

当用户要求：“写一个在 PS 中自动把当前图片缩放到 800x800 的脚本”时，以类似如下格式回复：

```javascript
// 确保有打开的文档
if (app.documents.length > 0) {
    var doc = app.activeDocument;
    
    // 保存原来的标尺单位
    var startRulerUnits = app.preferences.rulerUnits;
    
    // 设置单位为像素
    app.preferences.rulerUnits = Units.PIXELS;
    
    // 缩放图像大小 (宽度, 高度, 分辨率, 缩放方法)
    doc.resizeImage(800, 800, doc.resolution, ResampleMethod.BICUBICSHARPER);
    
    // 还原标尺单位
    app.preferences.rulerUnits = startRulerUnits;
    
    alert("缩放完成！当前尺寸已调整为 800x800 像素。");
} else {
    alert("请先在 Photoshop 中打开一张图片！");
}
```
*(并在代码后附带运行步骤说明)*
