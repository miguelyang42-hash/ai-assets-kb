---
name: "[Harvest-SubAgent] 亚太中东B2B线索深度挖掘"
description: 当需要针对澳大利亚、中东、日韩等特定时区市场开发户外或灭蚊灯品类B2B客户时触发。执行LinkedIn负责人姓名挖掘、个人工作邮箱模式构造及SMTP真实性验证，并严格比对主数据库以排除重复记录，确保输出高质量增量线索。
created_by: sub_agent
main_agent_spawn_note: This skill SKILL.md can be injected into a new sub-agent by passing it in sessions_spawn.required_skills.
sub_agent_type: general
---
## Workflow
1. **目标市场定向搜索**：针对 {target_countries}（如 Australia, UAE, Japan）和 {product_keywords}（如 mosquito lamp, outdoor gear），使用 `web_search` 执行组合查询：`"{Role Keywords}" "{Product Keyword}" site:linkedin.com/in {Country}`，提取至少 60 个候选人的姓名与公司信息以应对筛选损耗。
2. **邮箱模式推导与 SMTP 验证**：对每个候选人，通过其公司官网或公开索引推导个人邮箱格式（如 first.last@domain.com）。严禁使用 info@ 等泛型邮箱。必须调用专业验证工具或脚本执行 SMTP 握手验证，确保邮箱真实可达且非 catch-all 陷阱。
3. **主数据库去重过滤**：读取 `{master_leads_csv}` 路径下的现有记录，提取所有已存在的 Company Name 和 Email。将新挖掘的线索与此列表进行精确比对，剔除任何已在库中的客户，确保增量价值。
4. **证据链锚定与落盘**：为每条保留的线索获取其 LinkedIn 个人主页 URL 作为 Evidence_Link。将最终结果整理为 CSV 格式，包含 Name, Company, Role, Email, Country, Category, Evidence_Link 字段，并保存至 {output_path}。

## Suggestions
- 若 LinkedIn 直接搜索受限，可尝试搜索目标公司的 "About Us" 或 "Team" 页面，结合 `web_search` 抓取页面上的负责人姓名。
- 对于日本和韩国市场，注意姓名顺序可能为“姓+名”，在构造邮箱时需参考该公司其他员工的公开邮箱格式进行校准。
- 批量验证邮箱时，建议分批次进行（每批 10-15 个），以避免触发 SMTP 服务器的频率限制导致 IP 被封。

## Fallback / Edge Cases
- Step 1: 若特定国家搜索结果不足，放宽职位关键词，将 "Purchasing Manager" 替换为 "Buyer", "Sourcing Specialist" 或 "Category Manager"。
- Step 2: 若无法通过公开信息推导邮箱格式，转向查询该公司的隐私政策页或 WHOIS 信息，寻找技术或行政联系人的邮箱作为格式参考。

## Pitfalls
- Step 2: 严禁仅凭猜测的邮箱格式直接录入，必须经过 SMTP 验证步骤，否则会导致高退信率并损害发件域名信誉。
- Step 3: 去重时必须同时比对公司名称和负责人姓名，防止同一联系人因使用不同邮箱别名而被误判为新线索。
- Step 4: Evidence_Link 必须是具体的个人 LinkedIn 主页链接，而非公司主页，以确保后续开发能精准触达决策人。
