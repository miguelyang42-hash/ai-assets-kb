## Patch 2026-06-21 17:07

- Step 4: 在 PowerShell 环境下使用 `search_gmail_messages` 验证时，若 `query` 参数包含 `[` 字符或嵌套双引号，极易触发 `MissingArrayIndexExpression` 解析错误。应改用简化关键词（如仅保留数字或字母）或使用单引号包裹整个 query 字符串。
- Step 5: 若按照建议通过 Python 脚本调用 `accio-mcp-cli`，在 Windows 环境下 `subprocess` 可能因环境变量未继承导致找不到命令。应先通过 `Get-Command accio-mcp-cli | Select-Object -ExpandProperty Definition` 发现其绝对路径（通常为 `AppData\Roaming\Accio` 下的 `.cmd` 文件），并在脚本中直接调用该绝对路径。
## Patch 2026-06-21 17:14

- Step 4: 执行发信状态验证时，建议在 `query` 中加入 `in:anywhere` 以扩大搜索范围，或在初步搜索失败后等待 10 秒并使用 `in:sent` 显式查询，避免因 Gmail 索引延迟或 API 暂存导致的可视性问题。
- Step 5: 在编写批量发信脚本时，必须对 CLI 的输出内容进行关键字匹配（如检测 "error" 或 "validation error"）。禁止仅依赖进程退出码 `returncode == 0` 来判断发送成功，以防 MCP 工具返回业务逻辑校验错误但 CLI 进程正常退出的情况。
## Patch 2026-06-22 16:21

- Step 4: 引入浏览器二级核验。当 `search_gmail_messages` 即使在延迟后仍无结果，或需提供“金牌验证”时，必须通过 `sessions_spawn` 导航至 `#sent` 文件夹并截图，防止邮件滞留草稿箱而 API 误报成功。
- Step 5: 严格执行“无图精排”渲染标准。邮件正文严禁使用 `<img>` 标签以根除 HTML 乱码问题，改用富文本格式（加粗、列表）突出核心卖点，并包含完整的经理级商务签名。
- 任务合规性审计：禁止在投递指标（如 50 封/轮）未达标时擅自停用或标记 Cron 任务为已完成。针对进度落后或投递失败项，需编写专用 Python 补救脚本批量补投，并附带截图证据。
