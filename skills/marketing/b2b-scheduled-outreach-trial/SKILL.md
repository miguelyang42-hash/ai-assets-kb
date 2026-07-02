---
name: "[Harvest] 定时外贸开发信试运行"
description: 设置并自动执行定时 B2B 获客与开发信任务。适用于外贸场景，通过 cron 调度 Agent 触发多步工作流，涵盖 Amazon/eBay
  卖家挖掘、品牌联系人深度验证、以及个性化开发信撰写。重点解决了在命令行环境中发送包含引号和换行符的复杂 JSON 邮件正文时的转义失败问题，通过本地文件缓存确保投递的可靠性。
created_by: main_agent
---
## Workflow
1. **定时调度初始化 (Cron Setup)**：使用 `cron` 工具设置任务。Payload 必须采用 `{"agent":"general", "kind":"agent", "message":"{prompt}"}` 结构，其中 `{prompt}` 为唤醒 Agent 后执行的具体获客指令。确保 `at` 时间为 ISO 8601 格式。
2. **多平台潜客挖掘**：任务触发后，针对 `{product_keyword}` 在 Amazon/eBay/Shopify 等平台执行 `web_search`，提取至少 5-10 个潜在目标卖家。同时使用 `task_create` 建立结构化的子任务跟踪进度。
3. **联系人深度验证**：参考 `brand-contact-research` 逻辑挖掘目标的官网、邮箱及负责人信息，并对提取的邮箱执行 DNS/MX 记录查询。将验证后的线索保存至本地工作区的 `{leads_file}.csv`。
4. **开发信文件化暂存 (JSON Payload Bypass)**：针对每个线索撰写个性化开发信。为解决 CLI 环境下 JSON 转义解析失败的问题，必须将每封邮件的 JSON 参数（包含 to、subject、body）通过 `write` 工具保存为本地独立的 `{id}.json` 文件。
5. **稳健的 CLI 邮件投递**：在 PowerShell/Bash 中读取本地 JSON 文件内容并存入变量（如：`$json = Get-Content -Raw {path}`），然后执行 `accio-mcp-cli call send_gmail_message --json $json`。严禁在命令行中直接通过字符串拼接传递包含引号或多行文本的正文。
6. **发信状态审计与汇报**：检查邮件投递日志，更新任务列表状态。若投递失败，检查 JSON 文件格式或发信配额，最后向用户汇总展示已联系的客户清单及后续跟进策略。

## Suggestions
- **PowerShell 参数传递**：在 Windows 环境下，使用 `$params = Get-Content -Raw "path.json"; accio-mcp-cli call ... --json $params` 是规避 Shell 转义错误最稳定的方式。
- **资产自动化归档**：发信完成后，可结合 `b2b-local-lead-archiving` 技能将生成的 JSON 邮件草稿和 leads 列表批量迁移至受保护的业务磁盘进行留痕。

## Pitfalls
- **Step 4/5**: 绝对禁止在命令行中直接用单/双引号包裹复杂的邮件 JSON 正文，这会由于正文内部的引号或换行符导致 Shell 语法解析死锁或报错。
- **Step 1**: 确保定时任务的触发时间晚于当前系统时间，并预留 1-2 分钟的系统处理缓冲，避免 Cron 任务因时间过期而失效。
