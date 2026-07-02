---
name: "[Harvest] 外贸开发信标准化与资产固化"
description: 针对跨境 B2B 开发场景，从成功案例中提取并固化视觉规范、HTML 模板及产品素材，建立长期可复用的“金牌标准”手册。通过 PowerShell 素材下载、发件箱渲染核验及脚本逻辑封装，解决 Windows
  环境下路径冲突、HTML 源码泄露等执行痛点。
created_by: main_agent
---
## Preconditions
- 已完成至少一轮外贸开发信试运行，并获得了初步成功的发信反馈或用户确认的模板样式。
- 运行环境为 Windows，需具备 PowerShell 执行权限。

## Workflow
1. **资产本地化与目录构建**：针对用户提供的素材或成功案例中的图片，在目标路径（如 `{project_assets}/product_images`）建立层级目录。在 Windows 环境下，若 `bash` 命令失效，应优先调用 PowerShell 的 `New-Item -ItemType Directory -Force` 及 `Invoke-WebRequest` 完成目录创建与高清图下载。
2. **金牌标准手册（Playbook）编写**：创建 `GOLD_STANDARD_PLAYBOOK.md`。手册必须包含：经过验证的 HTML 邮件骨架、本地素材引用路径清单、核心产品卖点（如 `{product_specs}` 等特定参数）以及发信身份规范，作为后续所有自动化脚本执行的“唯一事实来源”。
3. **发件箱渲染物理验证**：调用 `gmail-assistant` 的 `search_gmail_messages` 结合 `get_gmail_message_content` 获取已发送邮件。重点核验邮件正文（BODY）部分是否包含原始 HTML 标签（如 `<div`, `style=` 等）；若 BODY 字段直接显示这些标签，则判定为“源码泄露”，需优化脚本中的 MIME 封装或字符转义逻辑。
4. **投递脚本版本化封装**：基于手册规范编写专门的 Python 发信脚本（如 `GOLD_STANDARD_EXEC.py`）。脚本必须采用文件读取方式（`with open`）加载 HTML 模板，严禁在 shell 命令行参数中直接传递包含特殊符号的 HTML 字符串，以规避 Windows Shell 的转义解析错误。

## Suggestions
- 在 Windows 环境下，使用 `Get-Command accio-mcp-cli | Select-Object -ExpandProperty Definition` 获取 CLI 的绝对路径，解决脚本调用时的环境变量失踪问题。
- 建议在 Playbook 中对 HTML 模板进行“最小化”压缩后再存入，减少因冗余空格或换行导致的解析歧义。
- 在下载素材前，先执行一次 HTTP HEAD 请求验证图片外链的有效性，避免下载到失效的占位符。

## Fallback / Edge Cases
- **Step 1：素材下载失败**：若 `Invoke-WebRequest` 报错，尝试切换 `curl.exe`（Windows 内置版）并使用单引号包裹 URL，或提示用户检查代理设置。
- **Step 3：渲染验证不确定**：若 API 返回的 BODY 为空，尝试使用 `get_gmail_thread_content` 或直接跳转至 Gmail Web 端直链截图确认视觉效果。

## Pitfalls
- **Step 1**: 严禁在 Windows CMD 环境下使用 `&&` 连接 `mkdir` 与下载命令，这极易因符号解析差异导致路径未创建而下载报错，必须分步执行。
- **Step 3**: 验证渲染时不能仅看 `snippet`（摘要），必须通过内容检索确认是否包含 `<` 或 `>` 字符，防止邮件在收件人端显示为原始代码。
- **Step 4**: 脚本在传递 JSON 参数时，若包含 HTML 内容且未经过临时文件中转，会被 Windows Shell 误将 `< >` 识别为 IO 重定向符号导致执行崩溃。
