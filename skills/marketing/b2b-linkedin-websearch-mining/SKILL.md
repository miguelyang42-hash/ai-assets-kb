---
name: "[Harvest-SubAgent] B2B LinkedIn Web搜索挖掘"
description: 针对缺乏专业CRM或SMTP探测工具的受限环境，提供一套基于高级Web搜索语法（LinkedIn精确角色定位、第三方数据平台公开索引交叉验证）批量挖掘、核验并导出B2B负责人有效联系方式的标准化替代工作流，适用于快速拓客与线索冷启动场景。
created_by: sub_agent
main_agent_spawn_note: This skill SKILL.md can be injected into a new sub-agent by passing it in sessions_spawn.required_skills.
sub_agent_type: general
---
## Workflow
1. **构建定向搜索矩阵**：按 `{target_countries}` 和 `{product_keywords}` 组合，使用 `web_search` 执行精确短语查询：`"{Role}" "{Product Keyword}" site:linkedin.com/in {Country}`，批量获取候选人姓名与公司信息。
2. **邮箱模式匹配与第三方交叉验证**：对提取的姓名与公司，构造搜索词 `"{Full Name}" {Company} email "apollo.io"` 或 `"rocketreach.co"`。利用第三方数据平台的公开索引片段确认邮箱地址的真实性与活跃度，替代直接的SMTP探测。
3. **主数据库去重过滤**：使用 `read` 读取现有的 `{master_leads_csv}`，提取已联系的公司或姓名列表。将新挖掘的线索与此列表比对，剔除重复项，确保获取的是全新潜在客户。
4. **线索结构化落盘**：将验证通过的新线索整理为CSV格式，包含姓名、公司、职位、邮箱、国家、类目及LinkedIn证据链接，并调用 `write` 保存至指定路径。

## Suggestions
- 若 `site:linkedin.com` 搜索结果不足，可移除 `site:` 限制，改用 `"Category Manager" "Gardening" {Company} LinkedIn` 针对特定大型零售商进行定向挖掘。
- 邮箱验证时，优先信任 `apollo.io` 或 `rocketreach.co` 在搜索结果中直接展示的完整邮箱字符串，这些通常已做过底层SMTP存活验证。

## Fallback / Edge Cases
- **Web搜索返回“无结果”**：尝试放宽职位关键词（如将 "Purchasing Manager" 替换为 "Buyer" 或 "Category Manager"），或针对目标公司官网使用 `"contact" OR "team" site:{company_domain}`。
- **无法获取具体负责人**：若大型零售商隐私保护严格，转向挖掘其供应链上游的“Brand Manager”或通过 USPTO 商标数据库查找品牌背后的运营实体。

## Pitfalls
- **Step 2: 邮箱猜测风险**：严禁仅凭公司通用格式（如 `first.last@domain.com`）直接认定邮箱有效，必须依赖第三方索引平台的实际抓取记录作为存活证据，否则会被标记为“猜测”。
- **Step 3: 模糊匹配漏网**：去重时不仅要比对邮箱，必须同时比对“公司名称”和“负责人姓名”，防止同一联系人使用不同邮箱或别名导致重复录入。
