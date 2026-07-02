# -*- coding: utf-8 -*-
"""
Super Background Check - Payload Validator
对照 payload.schema.json 的红线逐项校验。
- R0  最高真实性铁律：所有 URL 必须出现在 data_sources（实测过）；占位词必须用 "暂未找到"
- R1  决策人 < 5 位                → 重新挖掘
- R2  任一维度字段为空              → 重发 web_search
- R3  risk_score 不在 0-100
- R4  dim9_decision 不是三选一
- R5  dim9_pitches 数量 != 5
- R6  WhatsApp 非 E.164 / 伪造号段
- R14 LinkedIn URL slug 不规范或疑似猜测     → 改为 "暂未找到"
- R15 邮箱未验证必须以 (推测,未验证) 标注    → 否则视为伪造
- R16 社媒/官网 URL 不符合域名白名单         → 改为 "暂未找到"
- R17 任意字段值出现明显占位/编造模式        → 整字段降级为 "暂未找到"
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Fabricated phone patterns - any match → force to "未公开"
FAKE_PHONE_PATTERNS = [
    re.compile(r"555-?01\d{2}"),       # +1-XXX-555-01XX  Hollywood/teaching reserved
    re.compile(r"555-?\d{4}"),          # 555-XXXX  generic North America fictional
    re.compile(r"123-?4567"),           # 123-4567 placeholder
    re.compile(r"^[\+]?0+$"),           # all zeros
    re.compile(r"(\d)\1{6,}"),          # 7+ same digit run
    re.compile(r"1234567"),             # sequential
    re.compile(r"000-?000-?0000"),
]
WHATSAPP_E164 = re.compile(r"^\+[1-9][0-9]{6,14}$")

# R14 - LinkedIn URL 校验
LINKEDIN_PERSONAL_RE = re.compile(r"^https?://([a-z]{2,3}\.)?linkedin\.com/(in|pub)/[\w\-\.%]+/?$", re.IGNORECASE)
LINKEDIN_COMPANY_RE  = re.compile(r"^https?://([a-z]{2,3}\.)?linkedin\.com/(company|school)/[\w\-\.%]+/?$", re.IGNORECASE)
# 疑似手工猜测的 slug：name-companyname 格式（高度相似业务名）
LINKEDIN_SUSPECT_PATTERNS = [
    re.compile(r"/in/[a-z]+\-[a-z]+\-[a-z]{3,15}/?$", re.IGNORECASE),  # firstname-lastname-companyname
]

# R16 - 官网 / 社媒域名白名单
SOCIAL_DOMAIN_WHITELIST = {
    "facebook":  re.compile(r"^https?://(www\.)?(facebook|fb)\.com/[\w\.\-]+/?", re.IGNORECASE),
    "instagram": re.compile(r"^https?://(www\.)?instagram\.com/[\w\.\-]+/?", re.IGNORECASE),
    "youtube":   re.compile(r"^https?://(www\.)?youtube\.com/(c/|channel/|user/|@)?[\w\.\-]+/?", re.IGNORECASE),
    "tiktok":    re.compile(r"^https?://(www\.)?tiktok\.com/@[\w\.\-]+/?", re.IGNORECASE),
    "twitter":   re.compile(r"^https?://(www\.)?(twitter|x)\.com/[\w\.\-]+/?", re.IGNORECASE),
}

# R15 - 邮箱真实性
EMAIL_RE = re.compile(r"^[\w\.\-+]+@[\w\.\-]+\.[a-zA-Z]{2,}$")
EMAIL_VERIFIED_TAG = re.compile(r"\((已验证|verified|hunter)\)", re.IGNORECASE)
EMAIL_GUESS_TAG    = re.compile(r"\((推测|guessed|未验证|unverified|pattern)\)", re.IGNORECASE)

# R17 - 通用占位 / 编造模式（任何字段触发都强降级）
PLACEHOLDER_PATTERNS = [
    re.compile(r"example\.com", re.IGNORECASE),
    re.compile(r"\bN/A\b", re.IGNORECASE),
    re.compile(r"^TBD$", re.IGNORECASE),
    re.compile(r"lorem\s*ipsum", re.IGNORECASE),
    re.compile(r"^xxx+$", re.IGNORECASE),
]

# Force UTF-8 stdout for Windows GBK console (cross-platform safe)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DECISIONS_OK = {"✅ 值得跟进", "⚠️ 持续观察", "❌ 暂时放弃"}

# R0 - 真实性铁律：标准占位词（仅这个被允许；其他变体强制改写）
NA_STANDARD = "暂未找到"
NA_LEGACY_VARIANTS = ["未公开", "未查到", "未找到", "未披露", "无", "N/A", "n/a", "TBD", "tbd"]

# R0 - URL 模式：只要出现 http(s):// 就触发实测要求
URL_RE = re.compile(r"https?://[^\s\)\"\']+", re.IGNORECASE)


def collect_data_source_urls(payload):
    """从 data_sources 数组里提取所有已实测的 URL（视为白名单）。"""
    urls = set()
    for src in payload.get("data_sources", []) or []:
        u = (src.get("url") or "").strip().rstrip("/").lower()
        if u:
            urls.add(u)
    return urls


def all_urls_in_payload(payload):
    """递归提取 payload 里出现的所有 URL（除 data_sources 自身），返回 [(path, url), ...]。"""
    found = []
    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "data_sources":
                    continue
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
        elif isinstance(node, str):
            for m in URL_RE.finditer(node):
                found.append((path, m.group(0).rstrip(".,)\"';").rstrip("/")))
    walk(payload, "")
    return found

REQUIRED_DIMS = {
    "dim1_type":     ["customer_type", "main_market", "tier_reason"],
    "dim2_basic":    ["founded_year", "hq_address", "website", "slogan"],
    "dim3_scale":    ["employees", "revenue_usd", "facility", "branches"],
    "dim4_business": ["main_categories", "sku_count", "price_range", "target_customers", "differentiation"],
    "dim5_trade":    ["hs_codes", "annual_import_value", "supplier_countries", "frequency", "batch_size"],
    "dim8_risk":     ["funding_status", "lawsuits", "negative_news", "credit_rating", "blacklist", "risk_score"],
}


def check(payload):
    errs = []

    # ============================================================
    # R0 - 最高真实性铁律（必须先于其他规则）
    # ============================================================

    # R0a - 所有 URL 必须出现在 data_sources（即被实测过）
    ds_urls = collect_data_source_urls(payload)
    for path, url in all_urls_in_payload(payload):
        norm = url.lower().rstrip("/")
        # 允许：data_sources 已收录的根域名匹配（同站点不同子页路径放行）
        url_root = re.sub(r"^(https?://[^/]+).*$", r"\1", norm)
        verified = (
            norm in ds_urls
            or url_root in ds_urls
            or any(d.startswith(norm) or norm.startswith(d) for d in ds_urls)
        )
        if not verified:
            errs.append(
                f"[R0 RED] 字段 {path} 引用了未在 data_sources 中实测过的 URL: {url}\n"
                f"         → 必须先用 web_fetch 实测该 URL，并把它加入 data_sources；\n"
                f"         → 或将该字段改为 '{NA_STANDARD}'。禁止编造 URL。"
            )

    # R0b - 强制使用统一占位词 "暂未找到"，禁止旧变体
    def walk_strings(node, path=""):
        results = []
        if isinstance(node, dict):
            for k, v in node.items():
                results.extend(walk_strings(v, f"{path}.{k}" if path else k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                results.extend(walk_strings(v, f"{path}[{i}]"))
        elif isinstance(node, str):
            results.append((path, node))
        return results

    for path, val in walk_strings(payload):
        # 只检查作为整体值的占位词（避免误伤"无障碍"等正常文本）
        v = val.strip()
        for legacy in NA_LEGACY_VARIANTS:
            # 必须是开头匹配（允许后缀备注），且不能在合法句子中出现（如"无 5 个分支"）
            if v == legacy or v.startswith(f"{legacy} ") or v.startswith(f"{legacy}("):
                errs.append(
                    f"[R0 RED] 字段 {path}='{val}' 使用了过时的占位词 '{legacy}'，"
                    f"必须统一改为 '{NA_STANDARD}'（可加备注：{NA_STANDARD} (...)）"
                )
                break

    # ============================================================
    # R1 - 决策人数量
    # ============================================================
    contacts = payload.get("dim6_contacts", [])
    if len(contacts) < 5:
        errs.append(f"[R1 RED] 决策人数量={len(contacts)} < 5，必须重新挖掘 LinkedIn")

    # R2
    for dim_key, fields in REQUIRED_DIMS.items():
        block = payload.get(dim_key, {})
        for f in fields:
            v = block.get(f)
            if v in (None, "", []):
                errs.append(f"[R2 RED] {dim_key}.{f} 为空，必须重发 web_search 补齐")

    # R3
    score = payload.get("dim8_risk", {}).get("risk_score")
    if not isinstance(score, int) or not (0 <= score <= 100):
        errs.append(f"[R3 RED] risk_score={score} 不在 0-100，必须强制重算")

    # R4
    decision = payload.get("dim9_decision", "")
    if decision not in DECISIONS_OK:
        errs.append(f"[R4 RED] dim9_decision='{decision}' 不在三选一列表，必须强制三选一")

    # R5
    pitches = payload.get("dim9_pitches", [])
    if not isinstance(pitches, list) or len(pitches) != 5:
        errs.append(f"[R5 RED] dim9_pitches 数量={len(pitches) if isinstance(pitches, list) else 'N/A'} != 5，必须严格 5 套")

    # 联系人字段完整性
    for i, ct in enumerate(contacts, 1):
        for f in ["name", "title", "email", "linkedin", "whatsapp", "touch", "strategy", "priority"]:
            if not ct.get(f):
                errs.append(f"[R1 RED] 第 {i} 位决策人 {f} 缺失")
        if ct.get("priority") not in ("P0", "P1", "P2"):
            errs.append(f"[R1 RED] 第 {i} 位决策人 priority='{ct.get('priority')}' 必须是 P0/P1/P2")

        # R6 - WhatsApp 真实性硬校验
        wa = (ct.get("whatsapp") or "").strip()
        if wa and not wa.startswith(NA_STANDARD):
            if not WHATSAPP_E164.match(wa.replace(" ", "").replace("-", "")):
                errs.append(f"[R6 RED] 第 {i} 位 WhatsApp '{wa}' 不是 E.164 格式 (应为 +国码+号码) 或字面值 '{NA_STANDARD}'")
            else:
                for pat in FAKE_PHONE_PATTERNS:
                    if pat.search(wa):
                        errs.append(f"[R6 RED] 第 {i} 位 WhatsApp '{wa}' 匹配伪造号段模式 ({pat.pattern})，必须改为 '{NA_STANDARD}'")
                        break

        # R14 - LinkedIn URL 真实性
        li = (ct.get("linkedin") or "").strip()
        if li and not li.startswith(NA_STANDARD):
            if not LINKEDIN_PERSONAL_RE.match(li):
                errs.append(f"[R14 RED] 第 {i} 位 LinkedIn '{li}' 不是合法 linkedin.com/in/ 个人主页格式，必须改为 '{NA_STANDARD}'")
            else:
                for pat in LINKEDIN_SUSPECT_PATTERNS:
                    if pat.search(li):
                        errs.append(f"[R14 RED] 第 {i} 位 LinkedIn '{li}' 疑似猜测的 slug (firstname-lastname-companyname 模式)，必须 web_fetch 实测或改为 '{NA_STANDARD}'")
                        break

        # R15 - 邮箱必须标注 (已验证) 或 (推测,未验证)；'暂未找到' 开头视为合规
        em = (ct.get("email") or "").strip()
        if em and not em.startswith(NA_STANDARD):
            base_email = re.sub(r"\s*\(.*\)\s*$", "", em).strip()
            if not EMAIL_RE.match(base_email):
                errs.append(f"[R15 RED] 第 {i} 位 email '{em}' 不是合法邮箱格式")
            elif not (EMAIL_VERIFIED_TAG.search(em) or EMAIL_GUESS_TAG.search(em)):
                errs.append(f"[R15 RED] 第 {i} 位 email '{em}' 未标注验证状态，必须追加 ' (已验证)' 或 ' (推测,未验证)' 后缀")

        # R17 - 通用占位
        for f in ["name", "title", "email", "linkedin"]:
            v = str(ct.get(f, ""))
            for pat in PLACEHOLDER_PATTERNS:
                if pat.search(v):
                    errs.append(f"[R17 RED] 第 {i} 位 {f}='{v}' 触发占位/编造模式 ({pat.pattern})")
                    break

    # R16 - 社媒/官网域名白名单；'暂未找到' 开头视为合规
    social = payload.get("dim7_social", {}) or {}
    for plat, regex in SOCIAL_DOMAIN_WHITELIST.items():
        url = (social.get(plat) or "").strip()
        if url and not url.startswith(NA_STANDARD):
            if not regex.match(url):
                errs.append(f"[R16 RED] dim7_social.{plat}='{url}' 不符合域名白名单，必须改为 '{NA_STANDARD}'")

    # R16 - 官网 URL 简单合法性
    web = (payload.get("dim2_basic", {}).get("website") or "").strip()
    if web and not re.match(r"^https?://[\w\.\-]+\.[a-zA-Z]{2,}", web):
        errs.append(f"[R16 RED] dim2_basic.website='{web}' 不是合法 URL")

    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--payload", required=True)
    args = ap.parse_args()

    payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
    errs = check(payload)

    if errs:
        print("[VALIDATION FAILED] 共 " + str(len(errs)) + " 项红线触发：")
        for e in errs:
            print("  - " + e)
        sys.exit(1)
    else:
        print("[VALIDATION PASSED] 全部红线通过 ✅ (R0 + R1-R6 + R14-R17)")
        sys.exit(0)


if __name__ == "__main__":
    main()
