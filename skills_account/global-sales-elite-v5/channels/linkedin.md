# LinkedIn 开发渠道 (channel: linkedin)

## 触发提示词
- `#领英开发 [国家] [客群]`：示例 `#领英开发 美国 全屋定制`
- `#领英开发 [职位] [行业]`：示例 `#领英开发 Buyer Cabinet Manufacturer`
- `#领英深挖 [Company URL]`：示例 `#领英深挖 linkedin.com/company/wood-mode`

## 搜索策略
- Sales Navigator 高级筛选：Industry + Headcount + Title + Geography
- Boolean 检索：`("Director of Procurement" OR "Buyer" OR "Sourcing") AND ("Cabinet" OR "Furniture") AND "United States"`
- 公司主页 → People 标签 → 关键岗位反查
- Posts 互动：评论 + 点赞 + Repost 制造曝光

## 决策人挖掘
- 公司 People 页：CEO/COO/VP/Director/Procurement/Buyer 全角色覆盖
- 反向 Hunter.io / Apollo 邮箱
- 个人主页 → Activity → 最近发文/评论 = 互动 Hook

## 输出动作
1. 每位决策人构建 v4_contacts 项，`channel="linkedin"`
2. v4.linkedin 字段必填完整 URL
3. 邮件首句 Hook 引用其个人 LinkedIn 最近 1 篇帖子或公司动态
4. 触点推荐："先互动 3 天 → InMail → 同步邮件"组合拳
