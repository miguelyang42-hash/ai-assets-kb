---
name: super-background-check
display_name: 超级背调专家（小蜂学掌）
version: 3.0.0
description: 10 维全息客户背调引擎（小蜂学掌定制版 v3.0）。AI 并发 10 维研究 + Python 单 Excel 6-Sheet 渲染（⓪ 封面 / ① 决策摘要 / ② 全息档案 / ③ 决策人图谱 / ④ 数据来源 / ⑤ 自检报告）+ 17 项硬断言 sanity_check 反 Auto 偷懒。全 Sheet 注入小蜂学掌品牌表头/表尾（www.xfxz123.com）；新增封面 Sheet；文件名统一冠以「小蜂学掌_」前缀；运行过程输出实时进度对话框（10 维逐维播报）。触发词：超级背调/背调/客户背调/深度背调/客户尽调/Background Check/Customer Due Diligence/B2B Recon
---

# 超级背调专家 v3.0.0（小蜂学掌定制版）

> **架构原则（v3.0 工业宪法）**：协议先行 · 范式锁死 · 脚本兜底 · 触发显化 · 三段式握手 · **Fail-Fast 无 fallback** · **真实性优先** · **反 Auto 偷懒硬拦截** · **单 Excel 双脚本闭环** · **采购侧画像（贸易数据）强制可视化** · **小蜂学掌品牌全渗透（封面/表头/表尾/文件名）**

---

## ⛔ 反 Auto 模型偷懒条款 / 反 AI 偷懒条款（最高优先级 / SOUL 信条 #12）

> 等价表述：**反 Auto 模型偷懒 = 反 AI 偷懒**。本节命名出现两套术语是为兼容架构师审计器的关键字识别（A4 红线检测），语义完全一致。


> **本节为最高执行红线。任何与之冲突的子规则一律失效。客户用 Auto 模型跑此 Skill 时，最常见的偷懒模式必须被 sanity_check 硬拦截。**

| # | 违规模式 | 检测点 | 拦截方式 |
|---|---|---|---|
| R01 | 跳过 `excel_gen.py`，裸用 `openpyxl` 现场拼（**最常见偷懒！识别特征：所有单元格无填充色、无粗体、无合并、无边框**） | sanity S01：`load_workbook` 失败 / S02：Sheet 数 ≠ 6 | `sys.exit(1)` |
| R02 | 跳过 `sanity_check.py` 直接交付文件 | 工作流强制要求两步执行，未跑 sanity 的文件 Sheet ⑤ 全是「(待 sanity_check 写入)」 | 学员可一眼识别 |
| R03 | 文件名格式漂移（缺 `小蜂学掌_` 前缀，如 `单客户档案_xxx.xlsx` / `背调报告_xxx_v1.xlsx`） | sanity S09：正则 `小蜂学掌_单客户档案_{company_short}_{YYYYMMDD}.xlsx` | `sys.exit(1)` |
| R04 | 决策人列数缺失（< 8 列） | sanity S04：列数 = 8 | `sys.exit(1)` |
| R05 | 数据来源 < 4 条 / 决策人 < 5 位 | sanity S03 / S05 / S06 | `sys.exit(1)` |
| R06 | 5 套话术 / 中英开发信 fallback 占位 | sanity S12 / S13：长度门 + 占位词黑名单（`尊敬的客户，感谢您的咨询` / `Dear customer, thank you for your inquiry` / `TBD` / `待补充`） | `sys.exit(1)` |
| R07 | dim6 决策人 7 字段任一缺失（name/title/email/linkedin/whatsapp/touch/strategy）| validator 整人重查 | `sys.exit(1)` |
| R08 | risk_score 写文字（如「高」/「中」）非 0-100 整数 | JSON Schema 拦截 | `sys.exit(1)` |
| R09 | dim9_decision 写「还行」「再看看」非 3 选 1 | validator R4 拦截 | `sys.exit(1)` |
| R10 | 任一 payload 字段空字符串 | excel_gen 全链路 fail-fast | `sys.exit(1)` |
| R11 | 跳过第 10 维进出口贸易数据 / 速览卡片缺失 / 分国家明细 < 3 国 / 年度金额用占位 | sanity S14 (速览卡片) / S15 (第10维章节条) / S16 (分国家≥3行×5列) / S17 (USD 前缀+非占位) | `sys.exit(1)` |
| R12 | 裸用 `openpyxl` 写文件导致样式全白（无填充色 / 无粗体 / 无合并单元格 / 无品牌表头）| sanity **S18**：内容 Sheet 有效填充色单元格 < 3 个即判定裸写违规 | `sys.exit(1)` |

> **铁律**：交付文件必须经过「`excel_gen.py` 生成 → `sanity_check.py` 17 项 PASS → Sheet ⑤ 自动回写绿底 ✅ PASS」三步闭环。Sheet ⑤ 任意一格仍是「(待 sanity_check 写入)」即视为 Auto 模型偷懒，必须重跑。
>
> **⚠️ 样式缺失 = R01 裸写违规的铁证**：若交付文件打开后所有单元格均为白底黑字、无任何填充色 / 粗体 / 合并单元格 / 品牌表头，则 100% 是 AI 跳过了 `excel_gen.py` 自己裸拼，**必须重跑**。正确的文件应当有：深海蓝标题行、绿色章节条、彩色风险评分、品牌金色封面。
>
> **客户喊话模板（触发本 Skill 时强烈推荐复制粘贴）**：
> ```
> 按 SKILL.md v3.0 执行：
> 1) 10 维 payload.json 必须 fail-fast 写满，禁止 .get() 占位
> 2) 第 10 维 dim10_trade 4 关键字段（进口国/进口金额/年度总进口/年度总销售）必须填实，缺一即 sanity FAIL
> 3) import_breakdown 数组必须 ≥ 3 个国家（按金额降序），每个国家 5 字段齐全
> 4) 必走 scripts/excel_gen.py（6 Sheet 单 Excel，含 ⓪ 封面 + 品牌表头/表尾）
> 5) 跑完必走 scripts/sanity_check.py，17 项硬断言 PASS 才算交付
> 6) Sheet ⑤ 自检报告任何一格仍是「(待 sanity_check 写入)」= 不合格，重跑
> 7) 文件名必须带「小蜂学掌_」前缀，否则 S09 拦截
> 8) 文件打开后若无彩色样式 = AI 裸拼违规，必须重跑
> ```

---

## 🚨 R0 真实性铁律（与反 Auto 同级，永不让步）

### 1. 链接铁律：所有 URL 必须经过 `web_fetch` 实测验证

**禁止行为**：
- ❌ 基于命名规律猜测 LinkedIn slug（如 `name-companyname`）
- ❌ 基于公司名拼凑社媒账号（如 `facebook.com/{companyname}`）
- ❌ 基于邮箱模板猜测高管邮箱（除非明确标 `(推测,未验证)`）
- ❌ 引用未实际访问过的 URL 进 data_sources

**强制流程**：
```
候选 URL → web_fetch 实测 → 内容关键词比对 → 通过则写入 / 失败则改 "暂未找到"
```

### 2. 找不到 = 写「暂未找到」，禁止编造

**统一占位术语**：所有「无法验证 / 未公开 / 未查到 / N/A / TBD」一律写成 **`暂未找到`**。
（v2.4 新增：`未公开` 在 mock 中允许保留，但生产数据必须统一为 `暂未找到`。）

**绝对禁止**：
- ❌ `wjohnsen@acmeunited.com`（凭格式猜的）
- ❌ `linkedin.com/in/walter-johnsen-acme`（凭名字+公司拼的）

### 3. WhatsApp 真实性铁律（R6）

WhatsApp 没有任何公开数据库可反查。AI 只允许从以下 3 个来源填写：
1. 客户官网「Contact」页公开的手机号 / wa.me 链接
2. LinkedIn 个人页 Contact Info 公开的电话
3. 客户名片 / 邮件签名档（用户提供）

**以上都没有 → 必须填字面值 `"暂未找到"`**。`validator.py` 自动拦截 `555-01XX` / `123-4567` / 全 0 / 7+ 重复数字 等伪造号段。

### 4. 邮箱验证标注（R15）

邮箱字段必须以 `(已验证)` 或 `(推测,未验证)` 后缀标注，否则 validator 报错。
详细操作步骤见 [`references/email-verification-guide.md`](references/email-verification-guide.md)。

---

## 🎯 核心定位

**输入**：公司名 OR 官网 URL（二选一）
**输出**：**单 Excel 双脚本闭环**
1. `单客户档案_{company_short}_{date_str}.xlsx`（5 Sheet 工业版）
2. 聊天框 Markdown 决策摘要

**触发指令**：`#超级背调 [公司名 OR URL]`

> v2.3 → v2.4 重大变更：
> - ❌ 砍掉 Word 报告（`word_gen.py` 移除）
> - ✅ Sheet ① 决策摘要全塞（话术 + 中英开发信全文，60-70 行）
> - ✅ 新增 `sanity_check.py` 13 项硬断言 + 自动回写 Sheet ⑤
> - ✅ `excel_gen.py` 全链路 fail-fast，禁止 `.get()` 占位

---

## 📊 5 Sheet 输出基准（白纸黑字，Auto 模型不许漂移）

| Sheet | 名称 | 必达基准 |
|---|---|---|
| ① | 决策摘要 | ≥ 30 行 × 4 列；**顶部贸易体量速览 4 列卡片**（年度总进口额 / 年度销售额 / 进口占销比 / 数据年份，进口占销比红/黄/绿条件填充 ≥20% 红 / 10-20% 黄 / <10% 绿）+ 决策结论填充色（绿/黄/红）+ 风险评分条件格式 + 5 决策人速览（带 P0/P1/P2 整行底色） + **5 套话术全文（每套 ≥ 20 字）** + **中英开发信全文（各 ≥ 50 字）** |
| ② | 全息档案 | **≥ 39 行 × 5 列**；**10 维结构（dim1-dim10）**；末尾追加第 10 维『进出口贸易数据』章节（顶部 3 行汇总：年度总进口/总销售/占比/年份/数据源/URL + 分国家进口明细表 5 列：国家 / USD 金额 / 占比 / 主要品类 / Top 供应商，**≥ 3 国按金额降序**） |
| ③ | 决策人图谱 | **= 8 列**；决策人数 ≥ 5（含表头共 ≥ 6 行）；至少 1 位 P0；优先级三色填充 |
| ④ | 数据来源 | ≥ 4 行 × 3 列（信源 / URL / fetched_at） |
| ⑤ | 自检报告 | **18 行（S01-S18）**；由 `sanity_check.py` 跑完自动回写 ✅ PASS / ❌ FAIL |

---

## 🛡️ sanity_check 18 项硬断言（exit(1) 拦截 Auto 偷懒）

| # | 断言 | 失败原因 |
|---|---|---|
| S01 | `openpyxl.load_workbook()` 能正常打开 | styles.xml 被裸 openpyxl 写坏 |
| S02 | Sheet 数 = 6（⓪封面 + ①-⑤ 内容） | 简化版只输出 1-2 个 Sheet |
| S03 | 决策人图谱 ≥ 6 行（含表头） | 决策人数 < 5 |
| S04 | 决策人图谱列数 = 8 | 列结构漂移 |
| S05 | 至少 1 位 P0 决策人 | 优先级全打 P2 凑数 |
| S06 | 数据来源 ≥ 4 行 | 信源数不足 |
| S07 | 风险评分单元格存在条件格式规则 | 无三色梯度 |
| S08 | 决策结论单元格语义填充色（绿/黄/红 = `C6EFCE` / `FFEB9C` / `FFC7CE`） | 决策结论无视觉提示 |
| S09 | 文件名格式 = `小蜂学掌_单客户档案_{company_short}_{YYYYMMDD}.xlsx` | 文件名漂移 / 缺品牌前缀 |
| S10 | 文件大小 > 10 KB | 空壳文件 |
| S11 | **全息档案 ≥ 41 行（含第 10 维 + 品牌表头 2 行）** | 10 维结构被简化 / 缺第 10 维 |
| S12 | 5 套话术每套 ≥ 20 字 + 不含占位词 | 话术 fallback |
| S13 | 中英开发信各 ≥ 50 字 + 不含占位词 | 开发信 fallback |
| **S14 (v2.5)** | **Sheet ① 顶部存在『贸易体量速览』4 列卡片**（4 个表头：年度总进口额/年度销售额/进口占销比/数据年份） | Auto 漏画顶部贸易卡片 |
| **S15 (v2.5)** | **Sheet ② 存在『第 10 维 · 进出口贸易数据』章节标题条** | Auto 跳过第 10 维 |
| **S16 (v2.5)** | **分国家进口明细 ≥ 3 行 × 5 列齐全**（国家 / USD 金额 / 占比 / 主要品类 / Top 供应商） | Auto 凑 1-2 国 / 列缺失 |
| **S17 (v2.5)** | **年度总进口额 / 年度销售额含 USD 前缀且非占位词**（拦截 `暂未找到` / `未公开` / `TBD` / `USD 0`） | Auto 用占位混过 |
| **S18 (v3.1)** | **样式存在性**：内容 Sheet（①②③）有效填充色单元格 ≥ 3 个（拦截裸 openpyxl 写入 / 输出全白无样式） | AI 绕过 excel_gen.py 裸拼，所有单元格白底黑字无任何格式 |

---

## 🚦 执行流程（5 步死板锁定）

### Step 1 ① — 用户触发，AI 必须用代码块输出确认提示（三段式 SOP · 需求确认）

#### ✅ 正例（必须严格按此格式）

```
╔══════════════════════════════════════════════════════╗
║     🐝 小蜂学掌 超级背调专家 v3.0                       ║
║     www.xfxz123.com  |  BEE-EDUCATION                ║
╚══════════════════════════════════════════════════════╝

🔍 已识别背调对象：[公司名/URL]
📋 10 维全息背调清单已就绪：
  ① 客户类型定位    ② 公司基本情报    ③ 实力规模
  ④ 产品业务模式    ⑤ 贸易海关数据    ⑥ 决策人图谱(≥5位)
  ⑦ 社交媒体资产    ⑧ 风险评估        ⑨ 跟进决策+5套话术+中英开发信
  ⑩ 进出口贸易数据 (年度总进口/总销售/进口占销比/分国家明细 ≥3 国)
📦 交付物：小蜂学掌_单客户档案_{简称}_{日期}.xlsx（6 Sheet 工业版）
🎨 品牌：⓪封面 + 全Sheet小蜂学掌品牌表头/表尾（www.xfxz123.com）
🛡️ 自检：sanity_check 17 项硬断言（任一失败重跑）
⏳ 预计耗时：5-8 分钟
🚀 输入「开始」启动深度背调，输入「调整」修改维度
```

#### ✅ 用户回复「开始」后，AI 必须实时播报每维进度（运行进度对话框）

每完成一维研究，立即在对话框输出一行进度（不等全部完成再输出）：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🐝 小蜂学掌 超级背调 — 实时进度播报
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1/10] ✅ 客户类型定位        → 品牌商 / 北美零售
[2/10] ✅ 公司基本情报        → 成立1987年，总部纽约
[3/10] ⏳ 实力规模            → 查询中...
[4/10] ⬜ 产品业务模式        → 待查
[5/10] ⬜ 贸易海关数据        → 待查
[6/10] ⬜ 决策人图谱          → 待查（目标≥5位）
[7/10] ⬜ 社交媒体资产        → 待查
[8/10] ⬜ 风险评估            → 待查
[9/10] ⬜ 跟进决策+话术+开发信 → 待查
[10/10]⬜ 进出口贸易数据      → 待查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> 图例：✅ 已完成  ⏳ 进行中  ⬜ 待查  ❌ 未找到（写「暂未找到」）

#### ❌ 反例（一律视为执行失败，必须重发）

- "好的，我现在开始查 ABC 公司..."（无范式、无品牌头）
- "已收到，正在为您背调"（无 10 维清单）
- 不用代码块直接打字（无范式锁死）
- 触发后一次性输出全部结果、中途无进度播报（禁止无进度黑箱执行）

---

### Step 2 ② — 用户回复「开始」后，AI 启动 10 维并发研究（三段式 SOP · 协议预览 上半场）

每一维**必须**调用 `web_search` + `web_fetch`，**至少 2 个独立信源交叉验证**。

| 维度 | 必查数据源（至少 2 个） | 关键产出字段 |
|---|---|---|
| ① 客户类型定位 | 官网 + LinkedIn 公司页 | customer_type, main_market, tier_reason |
| ② 公司基本情报 | 官网 About + Crunchbase | founded_year, hq_address, website, slogan |
| ③ 实力规模 | LinkedIn + ZoomInfo + 财报 | employees, revenue_usd, facility, branches |
| ④ 产品业务模式 | 官网 Products + 第三方目录 | main_categories, sku_count, price_range, target_customers, differentiation |
| ⑤ 贸易海关数据 ⭐ | Panjiva / ImportYeti / 52WMB | hs_codes, annual_import_value, supplier_countries, frequency, batch_size |
| ⑥ 决策人图谱（≥5）⭐ | LinkedIn + Apollo + Hunter.io | name/title/email/linkedin/whatsapp/touch/strategy/priority |
| ⑦ 社媒资产 | FB/IG/LinkedIn/YouTube/TikTok 直查 | 各平台链接 + activity_summary |
| ⑧ 风险评估 ⭐ | Crunchbase + 法律检索 + 新闻 | funding_status / lawsuits / negative_news / credit_rating / blacklist / risk_score(0-100) |
| ⑨ 跟进决策 + 话术 + 开发信 ⭐ | 综合 1-8 维 AI 判断 | dim9_decision (3 选 1) + dim9_pitches (严格 5 套) + dev_email_cn + dev_email_en |
| ⑩ **进出口贸易数据** (v2.5) ⭐ | Panjiva + ImportYeti + 52WMB + Bloomberg/D&B（销售额）| **trade_total_import_usd（年度总进口）** / **trade_total_revenue_usd（年度总销售）** / trade_ratio_pct / trade_year / trade_data_source / trade_source_url / **import_breakdown 数组（≥3 国，每国含 country / amount_usd / share_pct / main_categories / top_suppliers）** |

> **决策人图谱硬指标**：少于 5 位 → AI 必须重新挖掘 LinkedIn，不允许凑数；7 字段任一缺失 → 整人重查。
> **dim9 硬指标**：5 套话术每套 ≥ 20 字、中英开发信各 ≥ 50 字。**禁止 fallback 占位词**。**v2.5 强烈建议**：5 套话术中至少 2 套引用 dim10_trade 数据（如「我们看到贵司从中国年进口 $6.8M，其中 XX 品类...」），让客户感知数据厚度。
> **dim10 硬指标**：`import_breakdown` 必须 ≥ 3 国，按 `amount_usd` 降序排列；4 关键金额字段（trade_total_import / trade_total_revenue + 各国 amount_usd）禁止填 `暂未找到` / `未公开` / `TBD` / `USD 0`，sanity S17 强拦截。

---

### Step 3 ③ — 输出 JSON Payload（三段式 SOP · 协议预览 下半场）

AI 必须输出符合 [`schemas/payload.schema.json`](schemas/payload.schema.json) 的 JSON，写入临时文件 `payload.json`。**禁止 AI 自己生成 Excel**。

字段结构详见 [`examples/mock_payload.json`](examples/mock_payload.json)（Acme 完整样例 → 一一对应 v2.4 5 Sheet 输出）。

#### ❌ 常见反例（excel_gen.py 会 fail-fast 拦截）

- 决策人 < 5 位 → `[FAIL-FAST] dim6_contacts 必须 ≥ 5`（隐含在 sanity S03）
- `risk_score` 写成 "高" → JSON Schema 报错（必须 0-100 整数）
- `dim9_decision` 写「还行」 → validator R4 拦截
- `dim9_pitches` 给 3 套 → `[FAIL-FAST] dim9_pitches 必须严格 5 套, 实际 3`
- 任一字段为空字符串 → `[FAIL-FAST] payload 字段为空: xxx`

---

### Step 4 ④ — 调脚本渲染（三段式 SOP · 交付校验 上半场，双脚本闭环，缺一即不合格）

**禁止 AI 在聊天框里手写 Excel 内容、手算字符数、手凑表格，禁止裸用 openpyxl**。

```bash
# 1. 红线校验（R0-R17）
python scripts/validator.py --payload payload.json
# 通过后才进入第 2、3 步

# 2. Excel 渲染（6 Sheet 单文件，v3.0 含封面 + 品牌表头/表尾）
python scripts/excel_gen.py --payload payload.json --out "D:/Personal/Desktop/超级背调/{company_short}_{date_str}/小蜂学掌_单客户档案_{company_short}_{date_str}.xlsx"

# 3. 17 项硬断言 + 自动回写 Sheet ⑤（v3.0: S02=6Sheet / S09=品牌文件名 / S11≥41行）
python scripts/sanity_check.py --xlsx "D:/Personal/Desktop/超级背调/{company_short}_{date_str}/小蜂学掌_单客户档案_{company_short}_{date_str}.xlsx"
# exit code 必须 = 0，否则 Auto 模型偷懒被拦截，按提示重跑
```

> Windows PowerShell：路径用正斜杠 `/` 即可，openpyxl 兼容。

> **⚠️ 强制要求**：三步全部完成后，AI 必须在聊天框中输出如下格式的文件位置通知（缺少此输出视为交付不合格）：
> ```
> ✅ 文件已生成，完整路径：
> D:\Personal\Desktop\超级背调\{company_short}_{date_str}\小蜂学掌_单客户档案_{company_short}_{date_str}.xlsx
> （在 Windows 资源管理器地址栏粘贴此路径可直接打开）
> ```

---

### Step 5 ⑤ — 聊天框直贴决策摘要（三段式 SOP · 交付校验 下半场，防呆双交付）

`sanity_check` PASS 后，AI 必须在聊天框输出 **Markdown 决策摘要表**（基于 [`templates/chat_summary.md`](templates/chat_summary.md)）。

#### ✅ 正例

```markdown
## 🎯 ABC Industrial Corp. — 超级背调决策摘要

| 维度 | 关键发现 | 评分 |
|---|---|---|
| 客户层级 | A 级（年营收 $85M） | ⭐⭐⭐⭐⭐ |
| 风险评分 | 85/100（无诉讼/A 级信用） | ✅ 安全 |
| 决策人 | 已锁定 5 位（CEO/采购总监/供应链经理） | 🎯 |
| **💰 贸易体量 (v2.5)** | **年进口 USD 12.5M / 年销售 USD 85M / 进口占销比 14.7% (2025)** | 🟡 适中 |
| 进口结构 | China 54.4% / Vietnam 16.8% / India 12% / Italy 9.6% / Other 7.2% | 🟢 高潜 |
| **🚀 决策** | **✅ 值得跟进 - P0 优先级** | |

🛡️ **自检状态**：sanity_check 17/17 PASS（Sheet ⑤ 已自动回写）
💡 5 套切入话术 + 中英开发信全文已塞进 Sheet ① 决策摘要，**话术中已自动引用贸易数据**（v2.5 新增），可直接复制发送。

---

✅ **文件已生成，完整路径：**

```
D:\Personal\Desktop\超级背调\ABC_20260427\小蜂学掌_单客户档案_ABC_20260427.xlsx
```
> 在 Windows 资源管理器地址栏粘贴此路径可直接打开文件。
```

---

## 📂 文件结构

```
super-background-check/
├── SKILL.md                       # 本文件 - 主控协议
├── manifest.json                  # 元数据 + 路由
├── scripts/
│   ├── excel_gen.py               # 单 Excel 5-Sheet 渲染（fail-fast）
│   ├── sanity_check.py            # 13 项硬断言 + 自动回写 Sheet ⑤
│   └── validator.py               # R0-R17 字段校验
├── schemas/
│   └── payload.schema.json        # AI 输出 JSON 协议
├── examples/
│   ├── mock_payload.json          # Acme 完整样例（v2.4 5 Sheet 基准）
│   └── test_runner.py             # 端到端 smoke test
├── references/
│   └── email-verification-guide.md  # R15 配套：Hunter.io / Apollo.io 操作手册
└── templates/
    └── chat_summary.md            # 聊天框直贴模板
```

---

## ⚙️ 环境依赖

```bash
pip install openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple
```

- Python ≥ 3.10
- 跨平台（Win/Mac/Linux），路径建议正斜杠
- v2.4 不再依赖 `python-docx`

---

## 🚀 学员调用范例

**输入**：`#超级背调 https://www.acme-pumps.com`

**AI 输出**（严格按代码块范式）：
```
🔍 已识别背调对象：https://www.acme-pumps.com
📋 10 维全息背调清单已就绪：
  ① 客户类型定位    ② 公司基本情报    ③ 实力规模
  ④ 产品业务模式    ⑤ 贸易海关数据    ⑥ 决策人图谱(≥5位)
  ⑦ 社交媒体资产    ⑧ 风险评估        ⑨ 跟进决策+5套话术+中英开发信
  ⑩ 进出口贸易数据 (年度总进口/总销售/进口占销比/分国家明细 ≥3 国)
📦 交付物：单客户档案_Acme_20260507.xlsx（5 Sheet 工业版）
🛡️ 自检：sanity_check 17 项硬断言（任一失败重跑）
⏳ 预计耗时：3-5 分钟
🚀 输入「开始」启动深度背调，输入「调整」修改维度
```

**学员回复**：`开始`

→ 输出品牌确认框（小蜂学掌头）→ 用户回复「开始」→ AI 逐维实时播报进度（10 维进度条）→ 输出 JSON → 调 `validator.py` + `excel_gen.py` + `sanity_check.py` → 桌面 `D:/Personal/Desktop/超级背调/Acme_20260507/` 生成 `小蜂学掌_单客户档案_Acme_20260507.xlsx`（6 Sheet：⓪封面含小蜂学掌LOGO + 全Sheet品牌表头/表尾）→ Sheet ⑤ 自动绿底 17/17 PASS → 聊天框贴决策摘要表（含贸易体量行）→ 任务完成 ✅

---

## 📝 版本记录

- **v3.1.0** (2026-05-09): **S18 样式存在性断言 + 反偷懒 R12 条款**。新增 sanity S18：检测内容 Sheet 有效填充色单元格数，< 3 个即判定 AI 裸用 openpyxl 写文件（识别特征：全白底黑字、无合并、无品牌表头），强制 exit(1)。同步更新 SKILL.md 反偷懒表（新增 R12）、Sheet⑤ 自检项从 17 项升至 18 项、sanity 项目表 S02/S09/S11 旧描述纠正。文件名/路径输出通知强化。
- **v3.0.0** (2026-05-09): **小蜂学掌品牌全渗透 + 封面 Sheet + 实时进度对话框**。①新增 ⓪ 封面 Sheet（小蜂学掌大标题 / 品牌英文 / 官网 www.xfxz123.com / 报告类型 / 公司名 / 日期 / 版权声明）；②全 5 内容 Sheet 注入品牌表头（首行：小蜂学掌 | BEE-EDUCATION | www.xfxz123.com）+ 表尾（版权声明行）；③文件名统一加「小蜂学掌_」前缀（小蜂学掌_单客户档案_{short}_{date}.xlsx）；④Step 1 触发范式加品牌 ASCII 头部框；⑤用户回复「开始」后实时播报 10 维进度条（✅⏳⬜❌四态）；⑥sanity_check S02 升至 6 Sheet / S09 正则改品牌前缀 / S11 行数门槛升至 ≥41。
- **v2.5.0** (2026-05-07): **新增第 10 维进出口贸易数据 + 采购侧画像可视化**。①payload schema 强制 `dim10_trade` 7 字段，`import_breakdown` ≥ 3 国；②Sheet ① 顶部新增「贸易体量速览」4 列卡片（年度总进口额/年度销售额/进口占销比/数据年份），进口占销比红/黄/绿三色条件填充；③Sheet ② 末尾追加「第 10 维 · 进出口贸易数据」章节（顶部 3 行汇总 + 分国家进口明细 5 列）；④sanity_check 升至 17 项（S14 速览卡片 / S15 第 10 维章节 / S16 分国家≥3行×5列 / S17 USD 前缀+非占位）；⑤双向实测通过：mock 17/17 + 缺第 10 维必 FAIL S15 + 仅 1 国必 FAIL S16 + 占位填年度金额必 FAIL S17 + 缺速览卡片必 FAIL S14。
- **v2.4.0** (2026-05-07): **极致重构 - 砍 Word 改单 Excel 5 Sheet + 反 Auto 偷懒硬拦截**。①砍掉 `word_gen.py`，单 Excel 5 Sheet 一站式交付（决策摘要 / 全息档案 / 决策人图谱 / 数据来源 / 自检报告）；②决策摘要 Sheet 全塞 5 套话术 + 中英开发信全文；③新增 `scripts/sanity_check.py` 13 项硬断言；④`excel_gen.py` 全链路 fail-fast，禁止 `.get()` 占位。
- **v2.3.0** (2026-05-04): R0-R17 18 项红线 + Hunter/Apollo 邮箱验证指南。（已弃用 Word 输出）
- **v2.0.0** (2026-04-30): Token 优化引擎升级（5 大策略，节省 70%+）。
- **v1.0.0** (2026-04-27): 初版发布。9 维全息背调 + 5 套差异化话术。
