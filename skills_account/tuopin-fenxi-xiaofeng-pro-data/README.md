# 🐝 拓品分析报告（小蜂学掌）Pro v2.0

> 工业级 B2B 拓品方案 Skill，10 分钟产出一份能给老板/客户讲的高颜值 ABCD 四象限拓品报告。

---

## 这个 Skill 解决什么问题？

外贸业务员/选品经理/KA 经理经常被问：
- 老客户问"还能给我推荐什么"，你给不出系统答案
- 老板要拓品方案，你只会拍脑袋想 3 个新品
- 工厂产能利用率不饱和，不知道往哪些行业延伸

**ABCD 四象限方法论**强制让你穷尽所有方向：
- 🅰 现有客户的升级款（A）
- 🅱 现有客户的周边件（B）
- 🅲 同样工艺卖给新行业（C）
- 🅳 第二增长曲线的蓝海（D）

每象限 20 个 SKU，前 5 个标 ⭐ 推荐，配真实 Amazon PDP 链接。

---

## 30 秒上手

1. 在 Accio Work 对话框输入：
   ```
   做一份 [瑜伽垫] 的拓品分析，我们工厂在丹阳，TPE/PVC/天然橡胶三种产线
   ```
2. AI 会按三段式握手：
   - Step ① 三要素调研（公司+产品+优势）
   - Step ② 启动 4 个 browser 子代理实抓 80 个真实 ASIN
   - Step ③ 生成 `{产品}拓品报告{日期}（小蜂学掌）.docx`
3. 拿到 docx，直接给老板。

---

## 文件结构

```
tuopin-fenxi-xiaofeng-pro/
├── SKILL.md                              # 入口协议
├── manifest.json                         # 元数据
├── README.md                             # 本文件
├── 学员使用手册.md                          # 给学员的傻瓜版指南
├── scripts/
│   ├── spawn_browser_asin.md             # Browser 子代理模板
│   └── generate_visual_report.js         # Node.js 报告生成器
├── templates/
│   └── keywords_ABCD.md                  # 4 象限关键词框架
├── references/
│   └── ABCD_methodology.md               # 方法论文字版
├── schemas/
│   └── payload.schema.json               # 数据契约
└── examples/
    └── 瑜伽垫拓品报告20260426（小蜂学掌）.docx   # demo 报告
```

---

## 依赖

- **Node.js** ≥ 18.0.0
- **docx** ^8.5.0（`npm install docx`）
- **Browser 子代理**（Accio Work 内置，需用户登录 Amazon）

---

## 触发关键词

拓品分析 / 小蜂学掌 / ABCD 选品 / 四象限选品 / 拓品报告 / 产品拓展 / product expansion / ABCD quadrant

---

## 版本

- **v2.0.0**（2026-04-26）：基于 skill-writer-pro v2.1 协议重构
  - 新增三段式握手 + 范式锁死 + 校验红线 + 触发词显化
  - 浏览器实抓 ASIN 流程，杜绝 LLM 编造
  - 废弃搜索 URL 兜底方案
  - 报告生成器参数化（接受 payload.json）

---

## 作者

Accio Work × 小蜂学掌  
方法论来源：《外贸产品裂变系统》
