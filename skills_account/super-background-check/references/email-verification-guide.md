# 邮箱验证可选增强指南 (R15 配套)

> 本文档是 super-background-check SKILL 的可选增强模块，配合 validator R15 红线使用。
> 当 LinkedIn / 官网无公开邮箱时，AI 应主动尝试本指南的两条路径，将 `(推测,未验证)` 升级为 `(已验证)`。

---

## 1. 触发条件

满足以下任一条件，AI 必须执行本指南：

1. 决策人 7 字段中 `email` 字段为空或为 `暂暂未找到`，且对方是 P0/P1 优先级
2. 用户显式要求"验证邮箱"或"找出真实邮箱"
3. 决策人姓名 + 公司域名都已确认（缺一不可，否则跳过）

---

## 2. 路径 A — Hunter.io（推荐首选）

### 2.1 适用场景
- 公司有独立域名（非 Gmail/QQ 邮箱客户）
- 域名 ≥ 5 个员工记录在 Hunter 数据库中
- 免费额度：25 次/月（按 IP 计）

### 2.2 操作步骤

**Step 1 — 域名探查（Domain Search）**
```
URL: https://hunter.io/search/{domain}
示例: https://hunter.io/search/acmeunited.com
```
预期产出：
- 该域名的常见邮箱模式（如 `{first}.{last}@domain` 或 `{f}{last}@domain`）
- Top 10 高管的真实邮箱（公开可见部分）
- 每个邮箱的置信度分数（0-100）

**Step 2 — 单人验证（Email Finder）**
```
URL: https://hunter.io/email-finder?full_name={姓+名}&domain={域名}
示例: https://hunter.io/email-finder?full_name=Walter+Johnsen&domain=acmeunited.com
```
预期产出：
- 1 个最可能的邮箱地址
- 置信度分数 + 来源页面 URL

### 2.3 置信度阈值与 R15 标记映射

| Hunter 置信度 | R15 标注 | 是否写入 payload |
|---|---|---|
| **≥ 90** | `(已验证, Hunter:高置信)` | ✅ 写入 |
| **70-89** | `(推测, Hunter:中置信)` | ✅ 写入但提醒人工复核 |
| **< 70** | `(推测,未验证)` | ⚠️ 标注但建议改 `暂暂未找到` |
| **未命中** | `暂暂未找到` | 必须降级 |

---

## 3. 路径 B — Apollo.io（备选 / 同时拿到 LinkedIn）

### 3.1 适用场景
- Hunter 未命中或域名记录不足
- 同时需要 LinkedIn URL + 直拨电话
- 免费额度：60 邮箱解锁/月，10000 条搜索结果/月

### 3.2 操作步骤

**Step 1 — People Search**
```
URL: https://app.apollo.io/#/people?qOrganizationName={公司名}&personTitles[]={职位关键词}
示例: https://app.apollo.io/#/people?qOrganizationName=Acme%20United&personTitles[]=Procurement
```
预期产出：
- 公司全员列表（带职位过滤）
- 每条记录附带 LinkedIn URL + 邮箱解锁按钮 + 直拨电话

**Step 2 — 邮箱解锁（消耗配额）**
对 P0/P1 决策人点击 "Access Email" 按钮，Apollo 返回：
- 已验证邮箱（带 ✅ Verified 标记）
- 或 Likely 邮箱（带 ⚠️ Catch-all 标记）

### 3.3 置信度阈值与 R15 标记映射

| Apollo 状态 | R15 标注 | 是否写入 payload |
|---|---|---|
| **Verified** | `(已验证, Apollo:Verified)` | ✅ 写入 |
| **Likely** | `(推测, Apollo:Likely)` | ✅ 写入但提醒人工复核 |
| **Catch-all** | `(推测,未验证, Apollo:Catch-all)` | ⚠️ 写入并建议二次校验 |
| **No Email** | `暂暂未找到` | 必须降级 |

---

## 4. 双源交叉验证策略（最高置信度）

当 P0 决策人极重要时，建议同时跑两条路径：

| Hunter 结果 | Apollo 结果 | 最终结论 |
|---|---|---|
| ≥ 90 | Verified | **金标准**：`(已验证,双源交叉确认)` |
| ≥ 70 | Verified | `(已验证, Apollo:Verified)` |
| < 70 | Likely | `(推测, 双源中等置信)` |
| 未命中 | 未命中 | `暂暂未找到` |
| 邮箱不一致 | 邮箱不一致 | `暂暂未找到` 并记入 dim8_risk.notes |

---

## 5. AI 执行清单（Checklist）

执行邮箱验证前，AI 必须按以下顺序检查：

- [ ] 是否已确认决策人姓名（First + Last，不是 "Manager" 这种职位）
- [ ] 是否已确认公司根域名（不是子域 / 个人域）
- [ ] 是否在公司官网 `/contact` `/team` 页直接搜过（最高置信度，免费）
- [ ] 是否在 LinkedIn 个人页 Contact Info 看过（部分公开邮箱）
- [ ] 以上全部无 → 才启动 Hunter.io / Apollo.io

执行后必须：

- [ ] 在 payload 的 contact.email 字段附带置信度标注（如 `walter.j@acmeunited.com (已验证, Hunter:95)`）
- [ ] 在 data_sources 数组中追加 Hunter / Apollo 的 URL + fetched_at
- [ ] 在 dim6 后面附 `email_verification_log` 字段记录尝试历史（可选）

---

## 6. 反例：禁止行为

❌ **禁止**未跑工具就标注 `(已验证)` —— 触发 R15 红线
❌ **禁止**把 Hunter 置信度 < 70 的邮箱标 `(已验证)` —— 误导用户
❌ **禁止**编造 Hunter / Apollo 的 URL 写入 data_sources —— 触发 R17 占位检测
❌ **禁止**对 Catch-all 邮箱不加警示就直接发开发信 —— 高退信率风险

---

## 7. 与 SKILL.md 的关系

- **R15 红线**（validator.py 强制执行）：邮箱必须以 `(已验证)` / `(推测,未验证)` 标注，否则报错
- **本指南**（AI 主动执行）：提供两条提升 `已验证` 比例的具体路径
- **触发顺序**：官网/LinkedIn 直查（免费） → Hunter.io（免费 25 次） → Apollo.io（免费 60 次）→ 全部失败 → `暂暂未找到`

> 维护人：super-background-check SKILL
> 版本：v1.0（与 SKILL v2.1 同步）
