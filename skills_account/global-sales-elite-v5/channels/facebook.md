# Facebook 开发渠道 (channel: facebook)

## 触发提示词
- `#FB开发 [国家] [客群]`：示例 `#FB开发 美国 五金分销商`
- `#FB开发 [兴趣群组关键词]`：示例 `#FB开发 Cabinet Makers Group`
- `#FB深挖 [Page URL]`：示例 `#FB深挖 facebook.com/durasupreme`

## 搜索策略
- Pages：行业关键词搜索（Cabinet, Furniture, Hardware Distributor, Interior Designer）
- Groups：垂直社群（"Cabinet Makers Network", "Interior Design Pros"）
- Marketplace + 商业账号活跃帖
- About 页面：邮箱、电话、官网、负责人

## 决策人挖掘
- Page → About → 邮箱/电话/官网
- Group 高频发帖人 = 业务负责人或采购
- 互动用户 → 反查 LinkedIn 验证身份

## 输出动作
1. 每个 Page 构建 v1~v8 JSON，`channel="facebook"`
2. v2.social 字段填 FB Page 粉丝数 + 互动率
3. 邮件首句 Hook 引用其 FB Page 最新发帖（产品发布、展会、活动）
4. 触点推荐："Page Inbox → 24h 后邮件 → 第 3 天 LinkedIn"
