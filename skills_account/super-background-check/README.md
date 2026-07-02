# 🔍 super-background-check v2.5.0

> **10 维全息客户背调引擎** —— 一条指令触发，AI 并发抓取 10 维数据 + Python 脚本渲染单 Excel 5-Sheet 工业版报告，17 项硬断言全程拦截 Auto 模型偷懒。

---

## 🎯 一句话定位

输入「公司名 OR 官网 URL」，30 秒内得到 1 份 5-Sheet 决策级 Excel + 1 张聊天框 Markdown 摘要，含 5 决策人、5 套话术、中英开发信、年度进出口贸易体量与分国家明细。

---

## 🚀 核心能力

- **10 维全息扫描**：客户类型 / 基本情报 / 实力规模 / 产品业务 / 贸易海关 / 决策人(≥5位) / 社媒资产 / 风险评估 / 跟进决策 / **进出口贸易数据 (v2.5 新增)**
- **单 Excel 5 Sheet 渲染**：决策摘要 / 全息档案(≥39行) / 决策人图谱(8列≥6行) / 数据来源 / 自检报告
- **17 项 sanity_check 硬断言**：跑完自动回写 Sheet ⑤，任一 FAIL → exit(1) 拦截
- **三段式 SOP 锁死**：需求确认 → 协议预览 → 交付校验，AI 全流程范式输出
- **零编造铁律**：fail-fast 全链路，禁止 `.get(field, "默认值")` fallback；占位词黑名单（暂未找到 / TBD / N/A 等）由 sanity S12/S13/S17 强拦截
- **贸易体量速览 (v2.5)**：Sheet ① 顶部 4 列卡片（年度总进口 / 年度销售 / 进口占销比 / 数据年份），进口占销比红/黄/绿条件填充

---

## ⚡ 快速开始（3 步）

```text
Step 1 ➜ 触发指令： #超级背调 [公司名 OR 官网 URL]
Step 2 ➜ AI 输出 10 维确认清单 → 用户回复「开始」
Step 3 ➜ 三脚本闭环自动跑：
         python scripts/validator.py --payload payload.json
         python scripts/excel_gen.py --payload payload.json --out <path>
         python scripts/sanity_check.py --xlsx <path>
         任一 exit ≠ 0 → 立即重跑
```

---

## 📁 目录结构

```
super-background-check/
├── SKILL.md                      # Skill 协议主文件（5 Step 死板锁定）
├── manifest.json                 # 元数据 + 触发词
├── README.md                     # 本文件
├── scripts/
│   ├── validator.py              # R0-R17 红线校验
│   ├── excel_gen.py              # 5 Sheet Excel 单文件渲染
│   └── sanity_check.py           # 17 项硬断言 + 自动回写 Sheet ⑤
├── schemas/
│   └── payload.schema.json       # 10 维 payload JSON Schema
├── templates/
│   └── chat_summary.md           # 聊天框 Markdown 摘要模板
├── examples/
│   └── mock_payload.json         # Acme 完整样例 payload
└── output/                       # 双模型实测产物归档
```

---

## 🛡️ Sanity Check 17 项断言简表

| # | 断言 | 失败拦截原因 |
|---|---|---|
| S01 | openpyxl 能正常打开 | styles.xml 被裸 openpyxl 写坏 |
| S02 | Sheet 数 = 5 | 简化版只输出 1-2 个 Sheet |
| S03 | 决策人图谱 ≥ 6 行（含表头） | 决策人 < 5 |
| S04 | 决策人图谱列数 = 8 | 列结构漂移 |
| S05 | 至少 1 位 P0 决策人 | 优先级全打 P2 凑数 |
| S06 | 数据来源 ≥ 4 行 | 信源不足 |
| S07 | 风险评分含条件格式 | 无三色梯度 |
| S08 | 决策结论语义填充色（绿/黄/红）| 无视觉提示 |
| S09 | 文件名格式 = `单客户档案_{short}_{YYYYMMDD}.xlsx` | 文件名漂移 |
| S10 | 文件大小 > 10 KB | 空壳文件 |
| S11 | 全息档案 ≥ 39 行（含第 10 维）| 10 维结构被简化 |
| S12 | 5 套话术每套 ≥ 20 字 + 不含占位词 | 话术 fallback |
| S13 | 中英开发信各 ≥ 50 字 + 不含占位词 | 开发信 fallback |
| **S14** | Sheet ① 顶部贸易速览 4 列卡片 | Auto 漏画顶部贸易卡片 |
| **S15** | Sheet ② 含「第 10 维 · 进出口贸易数据」章节标题条 | Auto 跳过第 10 维 |
| **S16** | 分国家进口明细 ≥ 3 行 × 5 列 | Auto 凑 1-2 国 / 列缺失 |
| **S17** | 年度总进口 / 销售含 USD 前缀且非占位 | Auto 用占位混过 |

> **S14-S17 为 v2.5 新增贸易数据维度专属拦截**。

---

## 🧪 双模型双向验证

```
[极致模型 Sonnet 4.5 / Opus 4]  ──→ 跑出 Demo Excel ──→ sanity_check 必须 17/17 PASS
                                                              │
                                                              ▼
[Auto 模型]                     ──→ 同 SOP 跑一次   ──→ sanity_check 必须 17/17 PASS
```

- 极致模型 PASS → 证明 SOP 可达
- Auto 模型 PASS → 证明强制脚本 + sanity 拦截足够稳
- **两份都过，Demo 才算合格**。只用极致模型验证就发布 = 重大事故。

---

## 📜 版本历史

| 版本 | 关键变更 |
|---|---|
| v2.3 | 9 维全息背调 + Word + Excel 双交付 |
| v2.4 | ❌ 砍 Word；✅ Sheet ① 全塞决策摘要；✅ 新增 sanity_check 13 项；✅ excel_gen 全链路 fail-fast |
| **v2.5** | ✅ 新增第 10 维「进出口贸易数据」；✅ Sheet ① 顶部贸易体量速览 4 列卡片；✅ Sheet ② 末尾追加分国家明细（≥3 国）；✅ sanity_check 13 → **17 项**（新增 S14-S17 贸易数据拦截）；✅ 全息档案 ≥39 行 |
