# Output Contract

Use this format unless the user explicitly asks for something else.

**All 6 dimensions below are MANDATORY.** Every response must contain all 6 sections in this exact order. The only exception is analysis-only mode, which skips dimensions 4 and 5.

**Stability rule:** The dimension names, numbering, and order must be identical across every response. Do not rename, reorder, merge, or split dimensions. This ensures the user always knows where to find each piece of information.

---

## 1. Problem Judgment (问题诊断)

Output as a structured block with these exact sub-fields:

- **Issue category** (问题类别): which negotiation topic (price, payment, sample, delivery, freight, complaint, follow-up, win-back, etc.)
- **Negotiation type** (谈判类型): the type of negotiation (e.g., payment terms negotiation, price defense, sample objection handling, delivery dispute resolution)
- **Current stage** (当前阶段): where the deal stands (inquiry, quote follow-up, sample stage, negotiation, order confirmation, production/shipment, after-sales, reorder, dormant reactivation)
- **Customer status** (客户类型): new customer, existing customer, trader, distributor, brand, end buyer, OEM, platform buyer
- **Core risk** (核心风险): what could go wrong if handled poorly — be specific to this scenario
- **Core opportunity** (核心机会): what lever can be used to advance the deal — be specific and actionable

Example:
```
问题诊断：高货值设备导致的客户现金流压力。
谈判类型：支付条款博弈（Payment Terms Negotiation）。
当前阶段：成交前方案确定阶段。
客户类型：待确认（建议先核实新老客户）。
核心风险：分期付款（尤其是发货后的分期）会给我方带来巨大的坏账风险和资金压力。
核心机会：利用付款方案的优化替代直接降价，锁定订单。
```

---

## 2. Case Match (案例匹配)

List the **closest 3 or more** bundled cases. Never output fewer than 3 matched cases.

For each case include:

- **Source** (来源): `reference file / source block / case theme`
- **Case excerpt** (案例摘要): a clean, rewritten takeaway from the case (no raw OCR text). 2-4 sentences summarizing the situation and the proven approach.
- **Reply mindset** (回复思维): the mental model or approach for responding — one sentence capturing the core logic.

If there is no exact match, state:

> No exact bundled match; using the closest case-based reasoning.
> 无精确匹配案例；使用最接近的案例推理。

Then still provide the 3+ closest cases from the library.

**Cross-topic matching:** When the user's problem spans multiple categories, cases should be drawn from multiple case-card files. Label each case with which aspect of the problem it addresses.

Example format:
```
案例 1: 12-case-cards-delivery-payment.md / CASE-PAYMENT-005 / Installment payment for high-value equipment
案例摘要：当客户要求长账期或分期时，应通过解释生产成本和资金压力来回绝"纯分期"，转而推行基于"进度"的阶梯付款。
回复思维：分期可以，但必须与生产节点挂钩，而非时间。

案例 2: 03-email-case-library.md / SRC-003 / Case 108 customer asks for O/A
案例摘要：明确指出高价值定制设备无法接受发货后的延期支付，但可以增加第三方金融保障或分阶段支付。
回复思维：底线是发货前必须付清。

案例 3: 12-case-cards-delivery-payment.md / CASE-PAYMENT-003 / Client pushes for longer terms
案例摘要：解释供应商端的现金压力，避免把回答变成抱怨。如有灵活空间，将其与订单规模、历史、保险或更快的尾款时间绑定。
回复思维：保护现金风险，只在有条件的情况下交换条款。
```

---

## 3. Response Strategy (应对策略)

Include all of the following sub-sections:

- **Step 1 — Acknowledge** (第一步：共情确认): how to open — acknowledge the customer's position without conceding. Show understanding of their situation.
- **Step 2 — Counter-offer** (第二步：反提案): the concrete counter-proposal or alternative to offer. Include specific options (方案A, 方案B, 方案C if applicable).
- **What not to say** (切忌说): specific phrases or approaches to avoid — at least 2 items, with brief explanation of why each is harmful.
- **Tradeable concessions** (可让步筹码): what can be offered if the customer pushes, listed in order of increasing concession (smallest concession first).

Example:
```
第一步（Acknowledge）：表达对客户投资预算的理解，强调我们致力于帮助其达成项目。
第二步（Counter-offer）：拒绝传统的"月供分期"，转为"生产进度阶梯付款"方案：
  a. 方案A（3-4-3模式）：30%定金，40%生产过半/视频验收后，30%发货前。
  b. 方案B（信用证L/C）：建议客户开具不可撤销信用证。
  c. 方案C（金融租赁）：建议客户通过当地金融机构融资。
切忌说：
  · "我们公司绝对不接受分期。"（太死板，会赶走客户）
  · "你可以等收到货后再付剩下的钱。"（风险极大，绝对禁止）
可让步筹码（由小到大）：
  1. 延长定金支付期限（如签约后15天内）
  2. 调整中期款比例（如35%而非40%）
  3. 增加5%质保尾款（发货后30天内支付）
  4. 接受L/C at sight替代T/T
```

---

## 4. Email Drafts (邮件草案)

Default output: **Chinese email draft** + **English email draft**.

Each email must include:

- **Subject line** (主题行): clear, professional, action-oriented
- **Salutation**: appropriate for the relationship
- **Body**: 3-6 short paragraphs, explaining rationale briefly, proposing alternatives, ending with a clear question or next step
- **Sign-off**: professional closing

Email style rules:
- Formal but not stiff
- Firm but not rigid
- Give face-saving options
- Use facts, not emotions
- Keep paragraphs short (2-3 sentences max)
- Include specific numbers, dates, or options where applicable
- End with a clear call-to-action or question

**Placeholder convention:** Use `[客户名]` / `[Customer Name]` and `[您的名字]` / `[Your Name]` for names. Use `[产品名]` / `[Product Name]` for product references when the user hasn't specified.

---

## 5. WhatsApp Quick Replies (快捷短句) — **MANDATORY**

Always output quick replies in both languages, even when the main channel is email.

- **Chinese quick replies** (中文快捷短句) — 4 numbered short lines, each ready to paste individually
- **English quick replies** (英文快捷短句) — 4 numbered short lines, each ready to paste individually

Quick reply style rules:
- 1-3 short sentences per line
- Natural and human — sounds like a real person typing
- One key point per message
- No email greeting block
- No long background explanation
- No formal salutations or sign-offs
- Each line is independently usable — no references to other lines

Progressive intensity pattern (MUST follow this order):
1. **Line 1 — Empathy** (共情): acknowledge the customer's concern or position
2. **Line 2 — Pivot** (转折): reframe the situation or introduce the alternative angle
3. **Line 3 — Concrete offer** (方案): state the specific proposal or option
4. **Line 4 — Gentle close** (收尾): invite response or confirm next step

If the user explicitly requested chat as the main channel, these quick replies become the primary output. In that case, expand to 6-8 lines covering more nuance, and optionally provide soft/standard/stronger push versions.

---

## 6. Next-Step Advice (后续行动建议)

Give 2-4 concise, actionable pieces of advice. Each item should be:
- Specific to this scenario (not generic)
- Actionable (the salesperson can do it immediately)
- Brief (1-2 sentences max)

Common advice categories:
- Customer background verification (new vs. existing, industry position, purchase history)
- Financial instrument suggestions (L/C, trade insurance, escrow)
- Product leverage (customization, lead time, quality certification, exclusivity)
- Timing leverage (production slot, raw material price trend, holiday schedule)
- Relationship building (visit invitation, video call, reference customer introduction)

Example:
```
1. 查背景：核实客户是新客户还是老客户，老客户可以适当降低首付比例，但发货前必须付清。
2. 推金融工具：如果客户坚持要货后分期，建议询问其是否能开具L/C（信用证）。
3. 强调定制化：在沟通中不经意地提及设备是根据其瓶型/容量"Customized（定制）"的，暗示我方承担的物料风险。
```

---

## Analysis-only mode

If the user asks only for diagnosis (e.g., "帮我分析一下", "just analyze", "先不用写邮件"), omit dimensions 4 (Email Drafts) and 5 (WhatsApp Quick Replies) but keep dimensions 1, 2, 3, and 6.

## English-only mode

If the user only wants English output, still do case matching first, then output only English for dimensions 4 and 5. Dimensions 1, 2, 3, and 6 remain bilingual or follow the user's language preference.

## Chat-primary mode

If the user specifies WhatsApp/chat as the main channel, dimension 5 becomes the primary output with expanded content (6-8 lines, optional intensity versions). Dimension 4 (email) becomes secondary but is still included.

## Multi-turn adjustment rules

When the user follows up to adjust the previous output:

| User says | Action |
|-----------|--------|
| "再强硬一点" / "firmer" | Adjust tone in dimensions 4 and 5 only; keep dimensions 1-3 and 6 unchanged |
| "再温和一点" / "softer" | Adjust tone in dimensions 4 and 5 only; keep dimensions 1-3 and 6 unchanged |
| "换个角度" / "try different approach" | Re-do dimensions 2-5 with different case selection; keep dimension 1 and 6 |
| "加上[X]" / "add [X]" | Append the requested content to the relevant dimension without re-doing others |
| "邮件太长了" / "shorter email" | Shorten dimension 4 only; keep all other dimensions |
| "只要英文" / "English only" | Re-output dimensions 4 and 5 in English only; keep 1-3 and 6 |
| "再匹配几个案例" / "more cases" | Add 1-2 more cases to dimension 2; keep all other dimensions |

Key principle: minimize re-work. Only re-generate the dimensions that the user's adjustment actually affects.

## Language and quoting rules

- Do not paste raw OCR-heavy blocks.
- Rewrite noisy text into clean `Case excerpt`.
- Keep source attribution precise.
- Do not fabricate case numbers or file names.
- All case excerpts must be paraphrased, not copy-pasted from raw source text.
- Maintain consistent terminology across responses (e.g., always use "阶梯付款" not sometimes "分期付款方案" and sometimes "阶梯式支付").
