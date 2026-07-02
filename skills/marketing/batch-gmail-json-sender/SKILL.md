---
name: "[Harvest] 批量 Gmail 开发信发送 (Python 桥接版)"
description: 在 Windows/PowerShell 环境下，通过 Python 脚本批量读取本地 JSON 邮件文件并调用 Gmail MCP 工具发送开发信。该方法有效避开了命令行直接传递复杂 JSON
  字符串时的转义错误、编码冲突及进程超时问题，适用于跨境 B2B 大规模邮件投递场景。
created_by: main_agent
---
## Preconditions
- 已获取用户的 Gmail 邮箱地址 `{user_email}`。
- 待发送的邮件已作为独立的 JSON 文件存储在本地工作区目录。

## Workflow
1. **扫描邮件资产目录**：确认本地资产目录（如 `{asset_dir}`）中已包含格式正确的 JSON 邮件文件（字段需含 `to`, `subject`, `body`）。调用 `list` 工具获取文件列表并记录绝对路径。
2. **编写 Python 自动化脚本**：生成一个 Python 脚本，逻辑为循环读取文件列表。脚本内需使用 `json.loads` 读取内容，并注入 `user_google_email` 字段，随后通过 `json.dumps` 构造 `accio-mcp-cli call send_gmail_message --json '{json_string}'` 调用语句。
3. **执行环境适配（关键）**：通过 `bash` 运行 Python 脚本。脚本内部调用 `subprocess.run` 时必须显式设置 `shell=True`，以确保 Windows 环境下能正确识别 CLI 命令，并建议使用脚本所在目录的绝对路径防止路径漂移。
4. **批量分发与状态记录**：运行脚本执行批量发送。脚本应实时打印每封邮件的发送状态（stdout/stderr），以便识别因单个 JSON 格式错误或网络抖动导致的发送异常。
5. **抽样投递验证**：发送完成后，随机选取 1-2 个目标邮箱地址，调用 `search_gmail_messages` 查询 `from:me to:{target}`，确保邮件已成功进入用户的“已发送”文件夹。

## Pitfalls
- **Step 3: Windows Shell 转义陷阱**：直接在终端通过变量传递复杂 JSON 字符串极易导致 `Invalid JSON` 或编码报错。必须通过 Python 脚本读取文件并配合 `subprocess` 处理，避免 PowerShell 对特殊字符（如引号、反斜杠）的破坏性解释。
- **Step 3: WinError 2 路径缺失**：若报错“系统找不到指定文件”，需显式启用 `shell=True` 或检查 `accio-mcp-cli` 是否在 PATH 中。路径中包含空格时，务必在 Python 脚本及调用命令中使用双引号包裹。
- **Step 4: 速率限制 (Rate Limiting)**：短时间内密集调用 API 可能触发 Gmail 的反垃圾机制或限流。建议在 Python 脚本循环中加入 `time.sleep(1)` 进行节流，提高任务成功率。
