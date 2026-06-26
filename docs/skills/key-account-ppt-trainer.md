---
name: key-account-ppt-trainer
version: 1.0.0
description: 大客户（KA）营销方案 PPT 实战 Skill — 专为外贸/跨境业务受训学员设计，让学员在 1 小时内独立产出 31 页可直接用于打客户的中英文 PPT。覆盖客户深度背调（Top 10 海外供应商 + 链接）、产品全网数据分析（Amazon / Shopify / 独立站 / Walmart / eBay / 速卖通 / Tmall / B2B 8 级 fallback，确保任何客户都不交白卷）、5 家竞争对手 SWOT、5 位关键决策人档案（含真实邮箱 / LinkedIn / WhatsApp，挖不到写「暂无」严禁编造）、基于「我方优势 × 客户痛点」的定制化营销方案、KP 攻坚 21 天 SOP、首封破冰邮件。当学员说「做 [客户名] 的 KA 方案」「打 XX 客户 PPT」「大客户营销方案」「拿单方案」「客户拓展 PPT」「客户背调 PPT」「key account proposal」时必须立即触发。
trigger_keywords: 做KA方案/打客户PPT/大客户营销方案/拿单方案/客户背调PPT/key account proposal/客户拓展PPT
---

# 大客户营销方案 PPT 实战 Skill（学员版）

## 🎯 这个 Skill 是干什么的

**给受训中的外贸/跨境业务员**，帮他们 1 小时内独立产出一份可以**直接拿去打客户**的 31 页大客户营销方案 PPT。

**关键定位**：
- ✅ 学员真实在打客户（不是模拟作业）→ 产出物**直接可用**，PPT 文字里不出现「学员/作业/练习」字样
- ✅ 学员还在受训中 → Skill 内部包含**步骤引导、自检清单、为什么这么做的解释**，让学员边做边学
- ✅ 信息深度对标顶级商务咨询公司，超过小满/海关数据等浅层背调工具

---

## 📥 学员必填输入（4 项）

| # | 项目 | 必填 | 示例 |
|---|------|------|------|
| 1 | **目标客户**：官网 URL 或 公司名 + 国家 | ✅ | `https://www.spiraledge.com` 或 `Spiraledge, Inc. (USA)` |
| 2 | **客户类型** | ✅ | 海外品牌商 / 跨境零售商 / 工业买家 / 渠道商 / 集采公司 |
| 3 | **我方公司核心优势**（二选一） | ✅ | A) 公司官网或阿里国际站 URL（自动抓取并提炼）<br>B) 直接列 3-6 条优势（每条 1 句话） |
| 4 | **目标品类** | 可选 | 默认从客户主营品类自动推断 |

**可选输入**：
- 客户产品数据来源偏好（默认按 8 级 fallback）
- 特殊需求（如"突出 ESG"、"重点攻 KP-2"）

### ⚠️ 缺「我方优势」必先问

如果学员只说"帮我做 [客户名] 的方案"，**第一反应必须是问清"我方核心优势"**，因为整个营销方案章节（第 4 模块 10 页）都基于它生成。

标准话术：
> 好的，开始前先确认 **我方公司的核心优势**（二选一）：
> A) 给我我方官网/阿里国际站链接，我自动提炼
> B) 直接列 3-6 条优势，例如：
>    · 自有工厂，年产能 200 万件
>    · 持 GRS / OEKO-TEX 双认证
>    · 越南分厂，可越南直发
>    · 30 天小批量返单（MOQ 500）
>    · Cork-TPE 复合垫专利
>    · 美东/欧洲海外仓，48h 本地发货

---

## 📤 产出物（学员拿到的东西）

```
[客户名]_KA_方案/
├── research/                                # 6 份 Markdown 研究底稿
│   ├── 00_input.yaml                        # 学员输入快照
│   ├── 01_company.md                        # 客户公司背调
│   ├── 02_product_data.md                   # 产品矩阵 + 全网数据 + VOC
│   ├── 03_competitor.md                     # 5 家竞争对手 + SWOT
│   ├── 04_kp_profile.md                     # 5 位 KP 真实联系方式
│   ├── 05_marketing_plan.md                 # 我方优势 × 客户痛点
│   └── top10_suppliers.md                   # 海关 Top 10 供应商 + 链接
├── [客户名]_大客户营销方案.pptx                # ★ 主交付物（31 页）
├── [客户名]_preview.pdf                       # PDF 预览
├── preview_images/                           # 31 张 JPG 切图（发微信用）
└── self_check_report.md                      # 学员自检报告（5 项质量门控）
```

---

## 🔄 5 步实战流程（学员按步执行）

每步对应 `workflows/0X_xxx.md`，学员可以跟着读。

```
Step 1  输入收集与确认  → workflows/01_input_checklist.md
Step 2  客户背调       → workflows/02_company_research.md
Step 3  产品全网数据   → workflows/03_product_data_multi_platform.md  ⭐
Step 4  竞争对手 + KP  → workflows/04_competitor.md + 05_kp_outreach.md  (可并行)
Step 5  营销方案合成   → workflows/06_advantage_matching.md
Step 6  PPT 渲染输出   → workflows/07_ppt_render.md
```

详细教学注释见每个 workflow 文件。

---

## 🛡️ 5 大质量门控（PPT 输出前必检）

| Gate | 必须满足 | 不满足怎么办 |
|------|---------|-------------|
| **G1 客户产品数据完整性** | 至少抓到 1 个电商平台 ≥ 10 条 SKU 数据 | 走 `03_product_data_multi_platform.md` 8 级 fallback，**绝不交白卷** |
| **G2 痛点必须溯源** | 5 个痛点每个标注「来源 SKU：xxx (BSR + 评分)」 | 不允许凭空写痛点 |
| **G3 KP 联系方式** | 5 位 KP × 4 字段（邮箱 / LinkedIn / WhatsApp / 其他），缺失写「暂无」 | **严禁编造** |
| **G4 我方优势驱动** | P22「我方优势盘点」必须用学员真实输入，不能是 示例数据 | 缺则回到 Step 1 |
| **G5 PPT 31 页 + 配色统一** | 深蓝 `#0F2C4D` + 橙金 `#F2A633`，31 页结构完整 | 检查模板是否被改坏 |

学员可以跑 `scripts/student_self_check.py [研究目录]` 自动验证 G1-G5。

---

## 🚦 重要约束（不要跳过）

1. **环境**：必须在 Windows + 已装 PowerPoint Desktop（PPT 渲染依赖 `comtypes` 调 PowerPoint COM）
2. **文件名规则**：渲染 PDF/JPG 前必须把中文 PPT 复制为 ASCII 名（如 `proposal.pptx`），否则 COM 失败
3. **PowerPoint COM**：必须 `Visible=1`，否则 `RPC_E_CALL_REJECTED`
4. **PPT 文字规范**：
   - ❌ 不能出现「学员/作业/练习/模拟」字样（PPT 直接发给客户）
   - ❌ 不能出现「竞品」（一律改为「竞争对手」）
   - ❌ 不能编造任何 KP 邮箱/电话/LinkedIn URL
5. **页数**：固定 31 页（包含 P22「我方核心优势盘点」新增页）
6. **配色（已固化，不要改）**：深蓝 `#0F2C4D` 主色 + 橙金 `#F2A633` 强调色 + 浅灰底 `#F5F5F5`

---

## 📞 与其他 Skill 的边界

| 相关 Skill | 区别 |
|-----------|------|
| `company-research` | 只做公司背调，无 PPT 输出 → 本 skill 调用其方法但延伸到 PPT 全流程 |
| `org-structure-research` | 全员组织架构，本 skill 只挖 5 位关键采购/品牌决策人 |
| `alibaba-store-analysis` | 分析自家阿里店铺，与本 skill 互补（自家 vs 打外部客户） |
| `competitive-landscape` | 纯竞争分析，本 skill 含简化版（5 家 SWOT） |

---

## 📂 文件清单速查

```
key-account-ppt-trainer/
├── SKILL.md                          # 本文件
├── reference.md                      # 进阶参考（多平台技巧/KP 挖掘/PPT 模板规范）
├── examples.md                       # 3 个完整学员案例（不同行业）
├── workflows/                        # 7 个实战工作流
│   ├── 01_input_checklist.md
│   ├── 02_company_research.md
│   ├── 03_product_data_multi_platform.md  ⭐
│   ├── 04_competitor.md
│   ├── 05_kp_outreach.md
│   ├── 06_advantage_matching.md
│   └── 07_ppt_render.md
├── prompts/                          # 4 个 prompt 模板
│   ├── voc_extraction.md
│   ├── swot.md
│   ├── advantage_matching.md         ⭐⭐
│   └── opening_email.md
├── scripts/
│   ├── build_ppt.py                  # 31 页 PPT 生成器
│   ├── ppt_convert.py                # PDF/JPG 渲染
│   └── student_self_check.py         # 学员自检 G1-G5
├── templates/
│   ├── input_template.yaml           # 学员填写模板
│   └── grading_rubric.md             # 教师评分标准（学员可对照自评）
└── examples/
    ├── demo_spiraledge.pptx          # 标准答案 demo
    ├── demo_spiraledge.pdf
    └── case_studies.md               # 3 个案例对比
```

详细内容请按需读取对应文件，不要一次性全读。

---

## 🐝 铁律 #0 — 启动播报（每次触发必输出）

```
🐝 小蜂学掌  ·  https://www.xfxz123.com/
📋 大客户营销方案 PPT 实战 Skill v1.0 已就绪。

正在为您准备 KA 方案，请先确认：
  ① 目标客户官网 URL 或 公司名 + 国家
  ② 客户类型（品牌商 / 零售商 / 工业买家 / 渠道商 / 集采公司）
  ③ 我方核心优势（A) 官网/阿里链接  B) 直接列 3-6 条）
```

---

## 🚦 反 Auto 偷懒守则

⚠️ **AI 模型（含 Auto/Sonnet/Opus）必须遵守以下规则，违者交付无效：**

| # | 规则 | 违反后果 |
|---|------|---------|
| R1 | **背调数据必须有来源 URL**，禁止凭空生成公司信息 | G1-G5 任一 FAIL → 不得交付 |
| R2 | **KP 联系方式必须真实可溯源**，推断邮箱必须标注「推断」 | 客户拉黑风险 |
| R3 | **财务数据必须注明来源**（财报/新闻/SimilarWeb），不得默认估算 | 误导决策 |
| R4 | **供应商链接必须 web_fetch 验证可达**，禁止填写未验证 URL | 背调不准根因 |
| R5 | **VOC 痛点必须有 source_sku + source_link**，禁止笼统结论 | G2 FAIL |
| R6 | **双模型实测**：极致模型 + Auto 模型各跑一次 sanity，均 PASS 才可交付 | 发布拒绝 |
| R7 | **输出文件名含小蜂学掌标识**：`[客户名]_KA方案_YYYYMMDD（小蜂学掌）.pptx` | R12 红线 |

---

## 🎯 客户喊话模板（防 Auto 偷懒触发咒语）

学员如发现 AI 给出未溯源的背调内容，直接复制以下话术：

```
按 key-account-ppt-trainer SKILL.md 规范：
① 所有背调数据必须附来源 URL（海关/LinkedIn/官网/财报）
② KP 联系方式：真实邮箱标来源，推断邮箱标「推断」，找不到写「暂无」
③ 供应商链接必须 web_fetch 验证可达，不可填写未验证的 URL
④ VOC 痛点每条必须有 source_sku + source_link，拒绝「用户反馈」笼统结论
⑤ 财务数据必须注明来源，不得默认写「估算约 XXX 万美元」
请重新执行并附上所有来源链接。
```

---

## 📋 品牌规范（小蜂学掌全媒体版）

所有输出物必须包含品牌标识：

| 输出物 | 品牌要求 |
|--------|---------|
| PPT 封面 | 🐝 小蜂学掌 \| https://www.xfxz123.com/ |
| PPT 页脚 | 🐝 小蜂学掌 · 专注外贸增长 · https://www.xfxz123.com/ |
| PDF 水印 | 🐝 小蜂学掌（15° 半透明） |
| 文件名 | `[客户名]_KA方案_YYYYMMDD（小蜂学掌）.pptx` |
| 自检报告 | 报告标题含「小蜂学掌 \| KA 方案质量报告」 |
