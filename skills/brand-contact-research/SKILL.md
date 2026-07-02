---
name: "[Harvest-SubAgent] 独立站品牌联系人及邮箱深度调研"
description: 针对指定电商品牌或产品类目进行深度联络信息调研，挖掘官网、业务邮箱及负责人背景并验证邮箱可达性；同时批量挖掘同类Shopify或eBay独立站卖家。适用于跨境B2B开发、供应链对接及竞品渠道拓展。
created_by: sub_agent
main_agent_spawn_note: This skill SKILL.md can be injected into a new sub-agent by passing it in sessions_spawn.required_skills.
sub_agent_type: general
---
## Preconditions
- 明确需要调研的 `{brand_list}`（品牌/公司名称列表）或 `{product_keyword}`（目标产品关键词）。
- 具备基础的 DNS 查询工具或网页内容抓取/正则提取能力。

## Workflow
1. **多渠道官方信息检索**：对每个 `{brand_name}` 执行组合搜索，构造查询词如 `"site:{domain} contact email"`、`"site:{domain} privacy policy"`、`"{brand_name} Amazon storefront trademark"`。若品牌无独立官网或网站失效，转向 USPTO 商标数据库查询品牌法律实体（Legal Entity），再以该实体名称搜索其官方联系方式。
2. **隐私政策与隐藏页面挖掘**：针对 `{ecommerce_platform}`（如 Shopify）独立站，直接请求标准化的 `/policies/privacy-policy` 或 `/pages/privacy-policy` 路径，使用正则匹配提取文本中的邮箱地址。此路径比 Contact 页更可能暴露真实邮箱，且能有效绕过仅展示工单系统（Ticket Form）的反爬虫页面。
3. **企业邮箱可达性验证**：对提取的邮箱执行 DNS MX 记录查询。识别主流企业邮局特征（如网易企业邮、阿里企业邮、Google Workspace、Zoho Mail 等）。若 MX 记录指向个人免费邮局且无其他线索，标记为“低置信度”并尝试构造 `support@{domain}` 或 `info@{domain}` 进行二次验证，确保投递通道有效。
4. **负责人与社交账号关联**：访问官网 "About Us"、"Team" 页面，或构造搜索词 `"{brand_name}" site:linkedin.com`，提取关键决策人姓名（如 CEO、Founder、采购经理）。若无具体姓名，记录其通用业务部门名称（如 Brand Operation Center）。
5. **同类独立站卖家批量挖掘**：针对 `{product_keyword}`，使用 Google 高级搜索 `site:myshopify.com "{keyword}"` 或 `site:ebay.com "{keyword}"` 获取 10+ 家同类卖家。快速请求其隐私政策页提取邮箱，记录店名、独立站链接及主营业务，并补充相关性说明。
6. **结构化数据整合输出**：将所有信息汇总为标准表格，字段必须包含：公司名/品牌、网站、已验证邮箱、负责人/部门、主营业务、相关性说明（如“源头工厂直销”、“垂直 Dropshipping 卖家”、“大型商超供应商”）。

## Suggestions
- **中国出海品牌特征识别**：若 MX 记录显示 `mxbiz1.qq.com`（腾讯）、`mxhichina.com`（阿里）或 `163.com`（网易），该品牌高度大概率为中国跨境卖家，沟通时可直接使用中文或明确标注采购需求。
- **商标数据库作为跳板**：对于纯亚马逊品牌（无独立站），USPTO TESS 数据库中的 "Owner Name" 和 "Attorney Name/Address" 是获取背后公司实体和联系方式的最可靠路径，远比盲目搜索品牌名高效。
- **批处理隐私策略**：Shopify 店铺隐私政策页面的 URL 结构高度标准化，可编写简单脚本批量请求该路径并提取邮箱，比手动逐个浏览效率提升数倍。

## Fallback / Edge Cases
- **官网失效/挂起**：若独立站因账单到期挂起（如 ITOPFOX），应立即转查该品牌在第三方大型零售商（如 Home Depot、Lowe's、Walmart）的供应商详情页面，或通过 Amazon 品牌旗舰店的 "Seller Profile" 寻找线索。
- **泛型邮箱泛滥**：若只能找到 `info@` 或 `contact@`，在 Step 3 验证通过后可保留，但需在“相关性说明”中标注“通用客服入口”，建议后续通过 LinkedIn 寻找具体采购负责人进行定向投递。
- **Shopify 卖家邮箱为个人 Gmail**：大量 Dropshipping 独立站使用 Gmail。提取后若验证 MX 为 `googlemail.com`，需结合网站域名 WHOIS 信息交叉验证其真实性，避免无效触达。

## Pitfalls
- **Step 1 盲目依赖 Contact 页**：许多现代独立站为防爬虫，在 Contact 页使用工单系统而非直接展示邮箱。若直接抓取 Contact 页无果，必须切换至 Step 2 的隐私政策页或网站页脚（Footer）抓取。
- **Step 3 忽略子域名邮局**：部分品牌使用 `support.brand.com` 形式的子域名邮局，DNS 查询时需确保查询完整域名，否则可能返回空 MX 记录导致误判邮箱无效。
- **Step 5 混淆制造商与零售商**：在挖掘同类卖家时，易将上游工厂品牌与下游零售独立站混为一谈。需在输出时严格区分“品牌方/制造商”与“Dropshipping 零售商/渠道商”，以免 B2B 开发信投递错位。
