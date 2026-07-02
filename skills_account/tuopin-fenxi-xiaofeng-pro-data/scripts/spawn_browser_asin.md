# 🤖 Browser 子代理 ASIN 实抓 Prompt 模板

> 这是 Step ② 用于消除 LLM 幻觉的核心资产。**直接 copy 给 `sessions_spawn(agent_id="browser")` 调用**，把 `{{KEYWORDS}}` 替换为该象限的 20 个英文关键词。

---

## 调用方式（主代理代码）

```javascript
// 4 个象限并行启动，每个 spawn 处理 20 个关键词
for (const quadrant of ['A', 'B', 'C', 'D']) {
  await sessions_spawn({
    agent_id: 'browser',
    label: `抓${quadrant}象限ASIN`,
    task: PROMPT_TEMPLATE
      .replace('{{QUADRANT}}', quadrant)
      .replace('{{KEYWORDS}}', keywords[quadrant].join('\n'))
  });
}

// 收齐结果后，对空缺项启动补抓 spawn（关键！timeout 600s 通常只能抓 16-18 个）
const missing = collectMissing(results);
if (missing.length > 0) {
  await sessions_spawn({
    agent_id: 'browser',
    label: `补抓${missing.length}个空缺ASIN`,
    task: PROMPT_TEMPLATE.replace('{{KEYWORDS}}', missing.join('\n'))
  });
}
```

---

## PROMPT_TEMPLATE（直接复制给 browser 子代理）

```
**任务：在真实 Amazon US 网站上为以下关键词各抓取一个真实 ASIN 并验证 PDP 页面非 404。**

## 操作步骤
对每个关键词：
1. 访问 `https://www.amazon.com/s?k=<关键词用+号连接>`
2. 用 browser snapshot 拿 DOM
3. 读取第一个非 Sponsored 商品的 `data-asin` 属性
4. 访问 `https://www.amazon.com/dp/<ASIN>` 确认页面真实存在、能看到商品标题
5. 记录关键词、ASIN、URL、商品标题

## 关键词列表（{{QUADRANT}} 象限，共 20 个）
{{KEYWORDS}}

## 严格规则（违反任意一条即重做）
- ❌ **禁止编造 ASIN**：必须 DOM 实读 `data-asin` 属性
- ❌ **禁止用搜索 URL 兜底**：找不到就换近似 SKU 重搜，绝不能返回 `amazon.com/s?k=`
- ❌ **禁止跳过 PDP 验证**：每个 ASIN 必须实际访问 `/dp/<ASIN>` 页面
- ✅ **找不到时换近似 SKU**：例如 "smart yoga mat" 找不到，可改 "intelligent yoga mat" 重搜
- ✅ **必须提取真实标题**作为验证证据

## 输出格式（严格 JSON，不要其他文字，不要 markdown 代码块包裹）
[
  {"id": 1, "keyword": "<原始关键词>", "asin": "B0XXXXXXXX", "url": "https://www.amazon.com/dp/B0XXXXXXXX", "title": "<实际页面标题>"},
  ...
]

20 个全部抓完且验证通过后返回。如果在 timeout 前确实无法抓完，把已抓的部分输出，未抓到的标 `"asin": null`。
```

---

## 经验数据（来自实战）

| 指标 | 值 | 说明 |
|---|---|---|
| 单 spawn timeout | 600 秒 | sessions_spawn 默认上限 |
| 单 spawn 平均产能 | 16-18 个 ASIN | 600 秒内 |
| 推荐策略 | 4 并行 spawn + 1 补抓 spawn | 总耗时 ~12 分钟，覆盖率 100% |
| 串行 spawn 风险 | "navigation interrupted" | 禁止串行，必须并行 |

---

## ⚠️ 校验红线

> 如果子代理返回结果中存在以下情况，**必须**重新启动补抓 spawn：
> - URL 包含 `amazon.com/s?k=`（搜索页兜底）
> - URL 包含 `alibaba.com/showroom/`（列表页兜底）
> - `asin: null` 或 `asin: ""` 数量 > 0
> - `title` 字段为空或包含 "Page Not Found"
