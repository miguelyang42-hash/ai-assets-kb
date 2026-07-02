---
name: "[Harvest-SubAgent] 多市场B2B线索深度挖掘"
description: 针对美、加、英、法、德等指定市场，深度挖掘特定品类（如户外防虫产品）的B2B客户负责人。涵盖零售商自有品牌、专业批发商及高销量在线品牌的采购/类目经理信息获取、LinkedIn证据链构建、SMTP模拟验证及主数据库排重。
created_by: sub_agent
main_agent_spawn_note: This skill SKILL.md can be injected into a new sub-agent by passing it in sessions_spawn.required_skills.
sub_agent_type: general
---
## Workflow
1. **目标市场与公司定位**：根据 `{target_countries}` 和 `{product_keywords}`，使用 `web_search` 搜索各市场的头部零售商（Retailer Private Labels）、专业害虫防治批发商（Specialized Pest Control Wholesalers）及高流量在线品牌。构造查询词如 `"top pest control wholesalers {country}"` 或 `"{keyword} retailer private label {country}"`，提取 20-30 家目标公司名单。
2. **关键决策人深度挖掘**：针对每家公司，使用 `web_search` 结合 LinkedIn 语法挖掘负责人。构造查询词 `"{Company Name}" "Category Manager" OR "Sourcing Manager" OR "Purchasing" site:linkedin.com/in`。必须获取负责人的真实姓名、具体职位及 LinkedIn 个人主页链接作为证据。
3. **邮箱模式匹配与第三方交叉验证**：基于姓名和公司域名，构造搜索词 `"{Full Name}" "{Company Domain}" email` 或利用 `apollo.io` / `rocketreach.co` 的公开索引片段确认邮箱。严禁使用 `info@` 或 `support@` 等泛型邮箱。对提取的邮箱执行 DNS MX 记录查询或使用 PowerShell 脚本进行 SMTP 模拟验证，确保邮箱可达。
4. **主数据库严格排重**：读取 `{master_leads_csv}`，提取已有的公司名称和联系人姓名列表。将新挖掘的线索与此列表进行比对，剔除任何重复的公司或联系人，确保 100% 为新线索。
5. **结构化落盘与证据归档**：将验证通过的新线索整理为 CSV 格式，字段包含：Name, Company, Role, Email, Country, Category, Evidence_Link。调用 `write` 保存至指定路径 `{output_path}`，并返回摘要统计。

## Suggestions
- **隐私政策页挖掘**：若官网 Contact 页无具体负责人，尝试请求 `/{domain}/policies/privacy-policy`，有时能发现注册邮箱或法律实体名称，进而通过 USPTO 商标数据库反查背后公司实体。
- **批量 MX 验证**：在 Step 3 中，可编写简单的 PowerShell 或 Python 脚本批量检查域名的 MX 记录，比逐个手动验证效率更高。
- **LinkedIn 高级搜索**：若标准搜索无果，尝试移除 `site:linkedin.com` 限制，直接搜索 `"{Role}" "{Product}" "{Company}"`，往往能在新闻稿或行业报道中找到带链接的姓名。

## Fallback / Edge Cases
- **Step 2 无法找到具体负责人**：若大型零售商隐私保护严格，转向挖掘其供应链上游的“Brand Manager”或通过公司官网的 "About Us" / "Team" 页面寻找高层管理人员（如 CEO/Founder）作为备选联系人。
- **Step 3 邮箱验证失败**：若 SMTP 模拟验证返回错误但 MX 记录存在，标记为“低置信度”并尝试构造 `first.last@domain.com` 格式的猜测邮箱，但在输出时需标注为“未验证”。

## Pitfalls
- **Step 2: LinkedIn 反爬限制**：严禁在短时间内高频直接请求 LinkedIn 详情页，这会导致 IP 被锁。必须通过搜索引擎作为中间跳板，仅抓取搜索结果中的快照信息。
- **Step 3: 泛型邮箱陷阱**：严禁录入 `info@`、`contact@` 或 `sales@` 等邮箱，这些通常由客服团队处理，无法触达决策人。若只能找到此类邮箱，需在排重阶段剔除或标记为无效。
- **Step 4: 模糊匹配漏网**：去重时不仅要比对邮箱，必须同时比对“公司名称”和“负责人姓名”，防止同一联系人使用不同邮箱或别名导致重复录入。
