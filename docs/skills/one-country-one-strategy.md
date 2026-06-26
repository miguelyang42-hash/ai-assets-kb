---
name: one-country-one-strategy
version: 2.0.0
description: 【小蜂学掌】一国一策略 B2B 国别市场作战手册自动生成器（通用品类）。输入「国家+品类」一键产出 47 页 PPT，覆盖国家概况、深度市场分析、B2B 销售策略、90 天落地事项四大章节。强制锁死 B2B 上游视角，强制 3 渠道竞品对比并附可点击 URL，强制每个数据点带 source。
author: 小蜂学掌 - https://www.xfxz123.com/
brand: { name: "小蜂学掌", website: "https://www.xfxz123.com/", copyright: "Copyright 2026 小蜂学掌 xfxz123.com" }
created_at: 2026-04-26
updated_at: 2026-05-09
license: MIT
---

# 小蜂学掌 × one-country-one-strategy v2.0.0

> **小蜂学掌** - 阿里国际站全行业SEO文案专家工具  
> 🌐 官方网站: https://www.xfxz123.com/  
> Copyright 2026 小蜂学掌 xfxz123.com

## 🎯 一句话定位
**输入「国家 + 品类」→ 5-8 分钟产出 47 页 B2B 出口作战手册 PPT（带真实 URL + 3 渠道竞品超链接）。**

---

## 🐝 启动通知（铁律 #0：第一句话必须输出）

**任何 AI 模型执行本技能时，第一句话必须输出以下内容，否则视为违规，流程作废重启：**

```
╔══════════════════════════════════════════════════════════════╗
║  🐝 小蜂学掌 × 一国一策略 v2.0.0                              ║
║  www.xfxz123.com  |  one-country-one-strategy                ║
╠══════════════════════════════════════════════════════════════╣
```

---
---

## 🆕 v2.0.0 新增特性

| 特性 | 说明 |
|---|---|
| 🚀 **运行对话框** | 新增 `scripts/dialog.py` 交互式CLI，引导用户输入国家+品类 |
| 🐝 **小蜂学掌品牌** | 所有输出文件名以 `小蜂学掌_` 开头 |
| 🎨 **PPT品牌页脚** | 每页PPT底部显示「小蜂学掌」LOGO + 官网链接 |
| 📍 **文件位置显示** | 生成完成后在控制台显示文件的完整绝对路径 |

---

## 🔑 触发词（任意命中立即启动）

> 一国一策略 / 国别策略 / 国家市场分析 / 进军XX市场 / 做一份XX国家的XX品类策略 / 市场作战手册 / B2B 出口策略 / 外贸国别报告 / country strategy / market entry plan / 我要打XX国家 / 帮我开发XX市场 / 小蜂学掌

也接受简短表达："做个英国市场分析"、"我要打德国"、"美国蓝牙耳机的策略"。

---

## 🤝 三段式握手协议（铁律，禁止跳过）

### Step ① 需求确认（5 秒钟）
向用户**确认 2 件事**（其余字段 AI 自动推断）：
1. **目标国家**（中文/英文皆可，AI 自动转 ISO 国家码）
2. **目标品类**（自由文本，AI 自动归类 + 推断 6 位 HS Code）

### Step ② 协议预览（10 秒钟）
向用户回放：
```
✅ 国家：英国 (GB) | 品类：直发器 (HS 851632)
✅ 视角：B2B 上游（工厂→中间商，禁用 DTC）
✅ 3 渠道：Amazon UK / Argos / Boots+Lookfantastic
✅ 品牌：小蜂学掌
✅ 输出：47 页 PPT + 1 份原始 JSON
✅ 预计 5-8 分钟（瓶颈在浏览器抓取）
```
等用户回 `开始` / `go` / `确认`。

### Step ③ 执行（自动）
1. 主 agent 写 `payload.json`
2. 启动 4 个并行 sub-agent
3. `pptx_pro.py` 渲染 47 页 PPT
4. 交付：PPT 路径 + 核心结论摘要 + 3 条可追问方向

---

## 🚨 范式锁死红线

| # | 规则 |
|---|---|
| R1 | `perspective` 必须 = `"b2b_upstream"` |
| R2 | sub-agent 产出禁含：BSR / FBA / ACoS / TikTok 网红 / Shopify DTC / PPC / Vine / Amazon 自营 |
| R3 | 3 渠道竞品数组缺一不打包 |
| R4 | 每条竞品必须含 `https://` URL |
| R5 | 市场容量 / CAGR 等核心数据必须含 source URL |
| R6 | PPT 总页数 = 47 ± 3 |

---

## 📋 输出基准

| 项 | 规格 |
|---|---|
| 输出格式 | pptx, json |
| 输出路径 | output/ |
| 文件命名 | 小蜂学掌_{country}_{category}_一国一策略_{run_id}.pptx |

---

## 🔧 调用方式

### 对话框模式（推荐）
```bash
python scripts/dialog.py
```

### 命令行模式
```bash
python scripts/main.py --payload templates/sample_payload.json
```

---

## 🛡 失败回滚机制
- `utils.rollback()` 删 `output/` 半成品 + 写 `logs/{run_id}.error.log`
- 用户始终拿到日志路径，不会遭遇"沉默失败"

---

*本 Skill 由 小蜂学掌 (https://www.xfxz123.com/) 出品*
