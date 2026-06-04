# OpenClaw 错误与解决方案知识库 (Knowledge Base)

本知识库用于规范记录和整理在 macOS 和 Windows 等系统下运行 OpenClaw 遇到的各类错误及其对应的解决方案。通过结构化、标准化的记录，便于后续遇到相同问题时快速检索与修复，无需重复排查。

---

## 🔍 快速检索索引 (Index)

| 错误 ID | 适用平台 | 错误简述 | 状态 | 快速链接 |
| :--- | :--- | :--- | :--- | :--- |
| `ERR-001` | `Windows` | 代理环境变量异常导致模型连接超时 | `已确认有效` | [ERR-001_windows_proxy_timeout.md](file:///Users/zz/codexproject/openclaw/errors/ERR-001_windows_proxy_timeout.md) |
| `ERR-002` | `通用` | 模型上下文窗口配置过小导致无回复 | `已确认有效` | [ERR-002_context_window_overflow.md](file:///Users/zz/codexproject/openclaw/errors/ERR-002_context_window_overflow.md) |
| `ERR-003` | `通用` | 模型供应商配置缺失导致主模型无法识别 | `已确认有效` | [ERR-003_unknown_provider_model.md](file:///Users/zz/codexproject/openclaw/errors/ERR-003_unknown_provider_model.md) |

---

## 📋 错误记录规范模板 (Standard Template)

新记录的错误需遵循以下结构填入本文件或新文档中：

```markdown
### [ERR-XXX] 错误简短名称

- **适用平台**: `Windows` / `macOS` / `通用`
- **错误现象/日志**: 
  ```text
  [此处贴入核心报错日志或现象描述]
  ```
- **根本原因 (Root Cause)**: 
  [解释为何会出现该错误，如网络超时、依赖缺失、路径权限等]
- **解决方案 (Solution)**:
  1. [步骤一：执行什么操作/修改什么配置]
  2. [步骤二：如何验证修复]
- **验证状态**: `已确认有效` / `待验证`
```

---

## 🔄 协作与维护流程

1. **提出问题**：您向我提供报错信息（日志、截图描述或现象）。
2. **分析诊断**：我识别错误原因，给出分析并提供详细的解决方案。
3. **验证确认**：您在目标设备上尝试该方案，并反馈是否有效。
4. **规范归档**：一旦确认有效，我将按照上述【错误记录规范模板】把该错误及解决方案录入本知识库中。
