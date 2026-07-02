# Google 开发渠道 (channel: google)

## 触发提示词
- `#Google开发 [国家] [客群]`：示例 `#Google开发 美国 全屋定制`
- `#Google开发 [产品关键词] [国家]`：示例 `#Google开发 hinges manufacturer USA`
- `#Google深挖 [公司名/网址]`：单家公司穿透式背调

## 搜索策略（高级搜索语法）
```
"keyword 1" "keyword 2" -alibaba -aliexpress site:.com (intitle:"manufacturer" OR intitle:"distributor")
"product" + "country" + "@email pattern"
inurl:"contact" OR inurl:"about-us" "{company}"
"{company}" + ("VP" OR "Director" OR "Buyer") + linkedin
```

## 决策人挖掘
- 网站 `/contact`, `/about`, `/team`, `/leadership`
- Google + LinkedIn 反查："{Company} site:linkedin.com/in"
- Hunter.io / Snov / RocketReach 邮箱模式验证

## 输出动作
1. 每家公司构建 v1~v8 JSON，`channel="google"`
2. `python main.py payload.json` 自动写 Word + Excel
3. 邮件首句 Hook 优先引用：官网案例 / 产品页 / 新闻稿 / Google News 头条
