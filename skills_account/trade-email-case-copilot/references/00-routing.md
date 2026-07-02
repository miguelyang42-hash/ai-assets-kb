# Routing

Use this file first for issue classification and case-file routing.

Prefer the structured case cards first. Use the raw email library only when you need more examples or more context.

## Categories

- Samples and proofing: sample mistake, sample fee, sample follow-up, sample remake, sample quality complaint, sample shipping, sample customs clearance.
- Price negotiation: price too high, comparison, low online price, discount pressure, price increase, target price unrealistic, mold fee, exchange rate impact, price validity expired.
- Delivery and timing: lead time, shipment delay, delay refund risk, early-order push, partial shipment, logistics tracking, customs delay.
- Payment and credit: deposit, balance, OA, platform order unpaid, fee pushback, installment payment, milestone payment, L/C, bank transfer fee, overdue payment, payment method dispute.
- Follow-up and silence: quote sent but no response, read but no reply, internal discussion, reorder follow-up, seasonal push, annual plan follow-up.
- Complaint and after-sales: quality issue, shipping damage, refund, negative review, trust repair, wrong product sent, size/spec mismatch, production error.
- Win-back and special cases: old customer recovery, buyer changed, family emergency, travel, office move, competitor switch-back, reactivation after long silence.
- Freight and logistics: freight surcharge, weight miscalculation, shipping mode change, freight split negotiation, customs documentation.

## Stages

- Inquiry follow-up
- Quote follow-up
- Sample stage
- Negotiation stage
- Order confirmation
- Production or shipment stage
- After-sales stage
- Existing-customer reorder stage
- Dormant customer reactivation stage

## Customer status

- New customer: no prior transaction history. Build trust before concessions.
- Existing customer: prior orders exist. Can reference history; moderate flexibility on terms.
- Trader / distributor: buys for resale. Focus on margin, reliability, and supply stability.
- Brand: end-brand purchaser. Focus on quality consistency and brand protection.
- End buyer: final consumer. Focus on usability, support, and total cost.
- OEM customer: private label or custom manufacturing. Focus on specs, MOQ, and IP protection.
- Platform buyer: purchases through Alibaba, Made-in-China, etc. Focus on platform rules and trust signals.

## Diagnostic questions

Ask only when needed (max 3):

1. New customer or existing customer? (新客户还是老客户？)
2. What is the main blockage right now? (目前卡在什么环节？)
3. What exactly did the customer say? Ideally the original English line. (客户原话是什么？最好是英文原文。)

Supplementary questions (use only if the above 3 are insufficient):

4. What product or equipment is involved? (涉及什么产品或设备？)
5. What is the approximate order value? (大概订单金额是多少？)
6. Which channel are you communicating on? (你们在哪个渠道沟通？)

## Routing map

- Samples and proofing -> [10-case-cards-samples.md](10-case-cards-samples.md)
- Price negotiation -> [11-case-cards-price.md](11-case-cards-price.md)
- Delivery, payment, and freight -> [12-case-cards-delivery-payment.md](12-case-cards-delivery-payment.md)
- Follow-up, complaint, win-back -> [13-case-cards-followup-after-sales.md](13-case-cards-followup-after-sales.md)
- Need more raw examples or broader wording -> [03-email-case-library.md](03-email-case-library.md)

## Cross-topic routing

When a user's question spans multiple categories (e.g., price + payment, sample + quality complaint):

1. Identify the PRIMARY category — the one the customer is most stuck on.
2. Load the primary case-card file first.
3. Load the secondary case-card file for supplementary cases.
4. If both files together still have fewer than 3 relevant cases, supplement from `03-email-case-library.md`.
5. In the output, clearly label which cases address which aspect of the problem.

Common cross-topic combinations:

| Primary | Secondary | Example scenario |
|---------|-----------|-----------------|
| Price | Payment | Customer wants discount AND longer payment terms |
| Samples | Price | Sample approved but customer now pushes on price |
| Delivery | Payment | Delivery delayed, customer withholds balance |
| Quality complaint | Payment | Quality issue, customer refuses to pay remaining balance |
| Follow-up | Price | Client went silent after receiving quote |
| Win-back | Price | Old customer left for cheaper competitor, wants to return |
| Price | Samples | Customer says sample is good but price is too high |
| Payment | Delivery | Customer delays balance, goods stuck in warehouse |
| Freight | Payment | Freight increased, customer refuses to pay surcharge |

## Minimum case matching rule

**Always match at least 3 cases.** If the primary case-card file has fewer than 3 relevant cases, supplement from the secondary case-card file or `03-email-case-library.md`. Never output fewer than 3 matched cases in the Case Match section.

## Citation format

Always cite matched material as:

`reference file / source block / case theme`

Examples:
- `12-case-cards-delivery-payment.md / CASE-PAYMENT-005 / Installment payment for high-value equipment`
- `03-email-case-library.md / SRC-003 / Case 108 customer asks for O/A`

## Confidence and fallback

When no case closely matches the user's scenario:

1. State: `No exact bundled match; using the closest case-based reasoning.`
2. Still provide 3+ cases that share the most relevant negotiation logic.
3. Clearly note which aspects of the matched cases apply and which do not.
4. Adjust the strategy and drafts to fit the actual scenario, not the matched case verbatim.

## User-uploaded cases

If the user provides their own case or past email exchange:

1. Analyze the user's case using the same diagnostic framework.
2. Still match against the bundled case library for reference.
3. Incorporate the user's specific context (product, customer history, prior communication) into the output.
4. Do not store or reference user-uploaded cases in future sessions.
