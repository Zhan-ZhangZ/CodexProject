# [ERR-PS-002] Magic Wand 动作描述符不可用与抠图/排版不协调优化

- **触发场景**: 尝试将带有纯白底的插画素材（如螃蟹、程序员 PNG 插画）导入到 Photoshop 主画布中，并期望去除白色底背景，实现人物/物体悬浮半透明的协调海报效果。
- **错误日志/表现**: 
  - 执行 Magic Wand 动作描述符（`setd` 命令）时抛出错误或静默失败（在 DialogModes.NO 下）：
    ```text
    Magic wand selection error: 功能无法在当前版本的 Photoshop 中使用。/ 命令“设置”当前不可用。
    ```
  - 海报渲染时，底图的白色矩形区块覆盖在底层彩色横幅和网格上，视觉上“一点都不协调”，且局部中英文文本出现重叠（例如“协作已打通”中“作”与“已”字相叠），或者两段文本之间留有大段不自然的空白。

- **根本原因 (Root Cause)**: 
  1. **Magic Wand Descriptor 局限性**: 用 ActionDescriptor 运行魔棒工具（`setd` 选择通道 `fLsn`）依赖特定像素点的取样（如 `Hrzn: 10, Vrtc: 10`），如果图层有缩放、位移或者在该坐标点并非目标纯色背景，魔棒选择便会失效。此外，中文版或不同版本的 Photoshop 的通道名称与内部动作标识存在兼容差异，导致执行报错。
  2. **文本重叠与不协调的 gap**: 
    - 当我们使用多图层 `drawText` 排版拼接长标题（如将“多Agent协作”与“已打通”拆为左右两半分别绘制）时，如果基于字符数粗略预估宽度，会因系统字体 kerning/字体实际长宽比例（如拉丁字母 Agent 与汉字字宽不等）导致最终渲染时两个文本层重叠或间隙过大。
    - 素材位置摆放没有充分预留安全区域，导致主视觉插画（如螃蟹的钳子）遮挡重要的文案说明。

- **经验证可行的解决方案 (Solution)**:
  1. **采用 Color Range 选择代替 Magic Wand 抠图**:
     对于纯色背景（如纯白 #FFFFFF），Color Range（色彩范围）在 ExtendScript 中不仅兼容性极强、不易报错，而且能够根据设定的容差（Tolerance）在整张画布上瞬间精准选择所有背景像素。
     ```javascript
     function placeAndMaskImage(filePath, layerName, scalePercent, moveX, moveY) {
         var imgDoc = app.open(new File(filePath));
         // 将背景图层转为普通图层以支持透明通道
         imgDoc.activeLayer.isBackgroundLayer = false;
         
         try {
             // 运行色彩范围选择：选取白色 RGB(255, 255, 255)
             var desc = new ActionDescriptor();
             desc.putInteger(charIDToTypeID("Tlrn"), 20); // 设定容差为20，可以吃掉JPG/PNG边缘的白边噪点
             
             var colorDesc = new ActionDescriptor();
             colorDesc.putDouble(charIDToTypeID("Rd  "), 255);
             colorDesc.putDouble(charIDToTypeID("Grn "), 255);
             colorDesc.putDouble(charIDToTypeID("Bl  "), 255);
             
             desc.putObject(charIDToTypeID("Mnm "), charIDToTypeID("RGBC"), colorDesc);
             desc.putObject(charIDToTypeID("Mxm "), charIDToTypeID("RGBC"), colorDesc);
             
             executeAction(stringIDToTypeID("colorRange"), desc, DialogModes.NO);
             // 清除（删除）选中的白色背景
             imgDoc.selection.clear();
             imgDoc.selection.deselect();
         } catch(e) {
             imgDoc.selection.deselect();
         }
         
         // 拷贝并贴入主文档
         imgDoc.selection.selectAll();
         imgDoc.selection.copy();
         imgDoc.close(SaveOptions.DONOTSAVECHANGES);
         
         app.activeDocument = doc;
         var activeLayer = doc.paste();
         activeLayer.name = layerName;
         activeLayer.resize(scalePercent, scalePercent, AnchorPosition.MIDDLECENTER);
         activeLayer.translate(moveX, moveY);
     }
     ```
  2. **精确微调拼接文本的起始坐标与图层避让**:
     - **拼接文本对齐**: 在 PingFang SC / Arial 64px 尺寸下，“多Agent协作”（含拉丁字母和汉字混合）渲染出的总宽度约为 400px。若起始 x 为 `200`，结尾约在 `600`。因此，右侧“已打通”的起始 x 应设在 `630`，既不会重叠，又保留了 30px 的紧凑天然间距。
     - **子母句居中**: 胶囊副标题两段文字合并后总宽度约 `470px`，将其在 `800px` 宽度的胶囊框中居中时，左段起始 x 应设为 `260`，右段设为 `480`，拼接浑然一体。
     - **文字避让素材**: 底部红色缎带文本“多Agent交互协作配置”从 `280` 右移至 `420` 起始，完全避开了左下角大螃蟹钳子（螃蟹中心在 `140`，向右延伸至 `320`）的重合区域，视觉观感十分清爽、和谐。

- **验证状态**: `已自动验证`
