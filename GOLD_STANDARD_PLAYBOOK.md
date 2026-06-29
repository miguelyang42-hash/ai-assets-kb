# XPES 外贸开发“金牌标准”模板 (v5 - 2026.06.29)

## 1. 核心格式规范
- **去图片化**: 遵照用户最新指示，**以后所有开发信不再添加图片**，以极简富文本提高送达率。
- **渲染方式**: 使用 Gmail 原生富文本编辑器排版，确保加粗和段落分明。
- **高亮**: 关键卖点使用**加粗 (Bold)** 突出。

## 2. 邮件正文模板 (英语)

### A. 创新引领版 (针对新接触客户)
**Subject**: [Innovation] 4500V Solar Mosquito Technology for {company}

Hi {name},

I am **Miguel Yang**, Business Development Manager at **Guangdong Xingpu Energy Saving Light**.

I am writing to you regarding {company}'s leadership in {business}.

We are a **pioneer factory in Solar Mosquito Killer Lamps since 2020**. I want to share our **2026 4500V Industrial-Grade Solar Model**. It provides the same killing power as traditional AC grid units with **Zero Electricity Cost**.

**Performance Highlights:**
- **4500V High-Voltage Grid**: Consistent industrial-grade kill power.
- **3-Day Battery Backup**: Optimized for cloudy weather performance.
- **IP65 Waterproofing**: Perfect for outdoor durability.

Did you do the market survey for your local market selling? I would like to share our quotation and you local hotsale model with you.

Best regards,

**Miguel Yang**
Business Development Manager
**Guangdong Xingpu Energy Saving Light**

### B. 渠道拓展/进口商专项版 (针对有中国进口经验的成熟买家)
**Subject**: Expand your 2026 catalog with high-margin Solar Insect Control

Hi {name},

Given your expertise in pest control and experience with Chinese manufacturing, I’ll get straight to the point.

You can instantly expand your current channels with a high-margin segment: **Eco-Friendly Solar Insect Control**. Our upgraded Solar Mosquito Zapper is a current category killer, averaging over **2,000 units sold per day in the US**.

**Why it's a hassle-free add-on for your catalog:**
- **Dusk-to-Dawn Automation**: Built-in light sensor automatically charges by day and zaps by night. True "set-and-forget" convenience for consumers.
- **Commercial-Grade Power**: High-voltage grid paired with an outdoor weatherproof design.
- **Turnkey Supply Chain**: Fully compliant with US regulations (**EPA/FCC/RoHS**) and retail-ready packaging.

Since you already know how to import from China, I’d like to share our **2026 Wholesale Catalog** and a detailed **Market Success Report** to see how our solutions fit your procurement cycle.

Would you like me to send over the technical data sheet and pricing?

Best regards,

**Miguel Yang**
Business Development Manager
**Guangdong Xingpu Energy Saving Light**

---

## 4. 协同与持久化 (Collaborative Database)
1. **统一数据库**: 所有新挖掘和联系的客户必须统一汇总至 `XPES_Master_Leads_Database.csv`。
2. **桌面访问**: 已在桌面建立 `XPES_Master_Leads.lnk` 快捷方式，方便用户随时检查。
3. **Agent 协同规范**: 遵循 `XPES_Customer_Assets/README_FOR_AGENTS.md` 中的去重与状态更新规则，确保多个智能体协作时不发生冲突或数据丢失。

## 6. 知识库与数据同步 (Knowledge Base & Sync)
1. **数据上传**: 每日工作完成后，必须将生成的客户表格及主数据库同步至 [ai-assets-kb](https://miguelyang42-hash.github.io/ai-assets-kb/)。
2. **操作规范**: 使用 `git push` 将 `XPES_Customer_Assets/` 下的更新推送到关联的 GitHub 仓库，以供其他智能体和团队成员协同。

## 5. 验证与质量红线
1. **身份真实**: 签名必须完整（Miguel Yang + 经理职位 + 星普公司名）。
2. **邮箱真实**: 严禁“格式猜测”。记录在数据库中的每个邮箱必须有负责人身份证据。
3. **闭环验收**: 每完成一轮投递，必须通过浏览器截图 Gmail “已发送”箱的详情作为交付证据。
