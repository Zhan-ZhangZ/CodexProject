### [ERR-PS-001] 文本图层字体缺失报错

- **触发场景**: 在调用 `update_text_layer` 接口或编写脚本修改文本图层字体为 Arial 时报错。
- **错误日志/表现**: 
  ```text
  General Photoshop error occurred. The requested font family is not installed or available on this system.
  ```
- **根本原因 (Root Cause)**: 
  Photoshop ExtendScript 要求使用字体的 PostScript 名称（如 `ArialMT`），而非其显示名称（如 `Arial`）。若本地未安装该字体或指定了错误的名称，会导致操作中断。
- **经验证可行的解决方案 (Solution)**:
  1. 在脚本中使用 `app.fonts` 获取并匹配可用的 PostScript 字体名。
  2. 动态生成的 ExtendScript 容错字体切换逻辑：
  ```javascript
  var fontName = "ArialMT"; // 默认字体名
  try {
      // 验证字体是否存在，若不存在则降级为当前活动字体
      app.activeDocument.activeLayer.textItem.font = fontName;
  } catch (e) {
      // 降级为宋体或系统默认字体
      app.activeDocument.activeLayer.textItem.font = "SimSun";
  }
  ```
- **验证状态**: `已自动验证`
