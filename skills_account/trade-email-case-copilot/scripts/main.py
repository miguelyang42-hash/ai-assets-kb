#!/usr/bin/env python3
"""Trade Email Case Copilot — CLI entry point.

Usage:
    python scripts/main.py diagnose <customer_message>
    python scripts/main.py route <category>
    python scripts/main.py validate <output_file>
    python scripts/main.py channel <user_message>
    python scripts/main.py tone <user_message>
    python scripts/main.py batch <input_file>
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "references"

CATEGORY_MAP = {
    "samples": "10-case-cards-samples.md",
    "price": "11-case-cards-price.md",
    "delivery_payment": "12-case-cards-delivery-payment.md",
    "followup_aftersales": "13-case-cards-followup-after-sales.md",
    "library": "03-email-case-library.md",
}

CROSS_TOPIC_THRESHOLD = 2.0

TRIGGER_PATTERNS = {
    "samples": {
        "en": [
            r"sample", r"proof", r"prototype", r"test.?unit",
            r"proofing", r"sampling", r"specimen", r"resample",
            r"sample.?fee", r"sample.?cost",
        ],
        "zh": [
            r"样品", r"打样", r"样板", r"试样", r"寄样", r"测样",
            r"样机", r"试用", r"试产", r"样品费", r"重新打样",
        ],
        "weight": 1.0,
    },
    "price": {
        "en": [
            r"price", r"quot", r"discount", r"cheaper",
            r"expensive", r"cost", r"budget", r"target.?price",
            r"mold.?fee", r"exchange.?rate", r"surcharge",
            r"markup", r"margin", r"competitiv", r"benchmark",
            r"price.?increase", r"price.?drop", r"negotiat.*price",
            r"tooling.?cost", r"mould",
        ],
        "zh": [
            r"价格", r"报价", r"折扣", r"便宜", r"贵",
            r"成本", r"预算", r"目标价", r"模具费", r"汇率",
            r"涨价", r"降价", r"砍价", r"比价", r"压价",
            r"报错价", r"开模费", r"利润",
        ],
        "weight": 1.0,
    },
    "delivery_payment": {
        "en": [
            r"pay", r"deposit", r"balance", r"installment",
            r"ship", r"deliver", r"lead.?time", r"freight",
            r"OA\b", r"l\.?/\.?c", r"letter.?of.?credit", r"payment.?term", r"milestone",
            r"customs", r"logistics", r"surcharge", r"overdue",
            r"wire.?transfer", r"T/T", r"escrow",
            r"warehouse", r"container", r"shipping.?cost",
            r"clearance", r"duty", r"tariff",
        ],
        "zh": [
            r"付款", r"定金", r"尾款", r"分期", r"发货",
            r"交期", r"运费", r"账期", r"信用证", r"物流",
            r"清关", r"海运", r"空运", r"催款", r"欠款",
            r"汇款", r"手续费", r"到港", r"关税", r"仓储",
            r"集装箱", r"柜", r"提单",
        ],
        "weight": 1.0,
    },
    "followup_aftersales": {
        "en": [
            r"complaint", r"quality", r"defect", r"damaged",
            r"refund", r"silent", r"no.?reply", r"not.?repl",
            r"ignoring", r"follow.?up", r"win.?back", r"recover",
            r"reorder", r"review", r"feedback", r"ghost",
            r"unresponsive", r"re.?engage", r"re.?activate",
            r"warranty", r"after.?sales", r"return",
            r"negative.?review", r"dispute",
        ],
        "zh": [
            r"投诉", r"质量", r"缺陷", r"损坏", r"退款",
            r"沉默", r"不回复", r"跟进", r"挽回", r"返单",
            r"差评", r"售后", r"已读不回", r"不理", r"流失",
            r"激活", r"老客户.*不回", r"催",
            r"保修", r"退货", r"纠纷", r"客诉",
        ],
        "weight": 1.0,
    },
}

CHANNEL_TRIGGERS = {
    "chat": [
        r"\bTM\b", r"TM上", r"旺旺", r"WhatsApp", r"whatsapp",
        r"\bchat\b", r"聊天", r"quick.?reply", r"快捷回复",
        r"short.?message", r"短消息", r"platform.?chat", r"平台聊天",
        r"social.?DM", r"WeChat", r"微信", r"Skype", r"skype",
        r"LinkedIn", r"Telegram", r"telegram",
        r"Facebook.?Messenger", r"Instagram.?DM", r"\bLine\b",
    ],
}

TONE_TRIGGERS = {
    "firm": [r"强硬", r"firmer", r"be\s+firm", r"直接一点", r"tough"],
    "soft": [r"温和", r"softer", r"be\s+gentle", r"委婉", r"mild"],
    "urgent": [r"紧急", r"urgent", r"赶紧", r"马上", r"ASAP"],
    "casual": [r"轻松", r"casual", r"随意", r"informal"],
    "professional": [r"专业", r"professional", r"formal"],
}

MODE_TRIGGERS = {
    "analysis_only": [r"帮我分析", r"just\s+analyze", r"先不用写邮件", r"analysis\s+only", r"只要分析", r"不用写"],
    "english_only": [r"只要英文", r"English\s+only", r"just\s+English", r"英文就好"],
    "chat_primary": [r"WhatsApp回复", r"聊天回复", r"快捷回复", r"chat\s+reply"],
}

SIX_DIMENSIONS = {
    "problem_judgment": {
        "patterns": [r"problem.?judgment", r"问题诊断"],
        "sub_fields": ["issue", "type", "stage", "risk", "opportunity"],
    },
    "case_match": {
        "patterns": [r"case.?match", r"案例匹配"],
        "sub_fields": ["source", "excerpt", "mindset"],
    },
    "response_strategy": {
        "patterns": [r"response.?strategy", r"应对策略"],
        "sub_fields": ["acknowledge", "counter", "not_to_say", "concession"],
    },
    "email_drafts": {
        "patterns": [r"email.?draft", r"邮件草案"],
        "sub_fields": ["chinese", "english", "subject"],
    },
    "whatsapp_quick_replies": {
        "patterns": [r"whatsapp.*quick", r"whatsapp.*reply", r"快捷短句", r"quick.?repl"],
        "sub_fields": ["cn_lines", "en_lines"],
    },
    "next_step_advice": {
        "patterns": [r"next.?step", r"后续行动"],
        "sub_fields": ["advice_items"],
    },
}


def classify(text: str) -> list[dict]:
    """Return matching categories with confidence scores."""
    results = []
    low = text.lower()
    for cat, config in TRIGGER_PATTERNS.items():
        score = 0
        matched_keywords = []
        for lang in ("en", "zh"):
            for pat in config.get(lang, []):
                matches = re.findall(pat, low if lang == "en" else text)
                if matches:
                    score += len(matches) * config.get("weight", 1.0)
                    matched_keywords.append(pat)
        if score > 0:
            results.append({
                "category": cat,
                "score": round(score, 2),
                "matched_keywords": matched_keywords,
            })
    results.sort(key=lambda x: x["score"], reverse=True)
    if not results:
        results.append({
            "category": "library",
            "score": 0,
            "matched_keywords": [],
        })
    return results


def detect_channel(text: str) -> str:
    """Detect the communication channel from user text."""
    for pat in CHANNEL_TRIGGERS.get("chat", []):
        if re.search(pat, text, re.IGNORECASE):
            return "chat"
    return "email"


def detect_tone(text: str) -> str:
    """Detect requested tone from user text."""
    for tone, patterns in TONE_TRIGGERS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return tone
    return "professional"


def detect_mode(text: str) -> str:
    """Detect output mode from user text."""
    for mode, patterns in MODE_TRIGGERS.items():
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                return mode
    return "full"


def route(category: str) -> str:
    """Return the file path for a given category."""
    filename = CATEGORY_MAP.get(category)
    if not filename:
        return f"Unknown category: {category}"
    filepath = REFERENCES / filename
    if not filepath.exists():
        return f"File not found: {filepath}"
    return str(filepath)


def count_cases(text: str) -> int:
    """Count unique case markers in text."""
    markers = re.findall(
        r"(?:CASE-[\w-]+|案例\s*\d+|Case\s+\d+|SRC-\d+|case\s+\d+)",
        text,
    )
    normalized = set()
    for m in markers:
        normalized.add(re.sub(r"\s+", " ", m.strip().upper()))
    return len(normalized)


def count_quick_reply_lines(text: str) -> dict:
    """Count quick reply lines in both languages."""
    cn_lines = len(re.findall(r"(?:中文|CN|中文快捷短句).*?\n(?:\s*\d+[.．、].*\n?)+", text, re.IGNORECASE))
    en_lines = len(re.findall(r"(?:英文|EN|英文快捷短句).*?\n(?:\s*\d+[.．、].*\n?)+", text, re.IGNORECASE))
    cn_numbered = re.findall(r"(?:中文|CN)[\s\S]*?(\d+[.．、])", text)
    en_numbered = re.findall(r"(?:英文|EN)[\s\S]*?(\d+[.．、])", text)
    return {"cn_lines": len(cn_numbered), "en_lines": len(en_numbered)}


def validate_output(text: str) -> dict:
    """Validate that output contains all 6 dimensions, 3+ cases, and required sub-fields."""
    issues = []
    warnings = []
    low = text.lower()

    for dim, config in SIX_DIMENSIONS.items():
        found = any(re.search(p, low) for p in config["patterns"])
        if not found:
            issues.append(f"Missing dimension: {dim}")

    cases = count_cases(text)
    if cases < 3:
        issues.append(f"Only {cases} case(s) matched; minimum is 3")
    elif cases < 4:
        warnings.append(f"Only {cases} cases matched; consider adding more for robustness")

    if not re.search(r"subject|主题|Subject", text):
        warnings.append("Email drafts may be missing subject lines")

    if not re.search(r"切忌|not.*say|avoid|禁止|Do not say", text, re.IGNORECASE):
        warnings.append("Response strategy may be missing 'what not to say' section")

    has_cn_email = bool(re.search(r"中文邮件|Chinese.*email|中文.*草案", text, re.IGNORECASE))
    has_en_email = bool(re.search(r"英文邮件|English.*email|英文.*草案|English.*draft", text, re.IGNORECASE))
    if not has_cn_email:
        warnings.append("May be missing Chinese email draft")
    if not has_en_email:
        warnings.append("May be missing English email draft")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "cases_found": cases,
        "dimensions_found": 6 - len([i for i in issues if "Missing dimension" in i]),
    }


def cmd_diagnose(args):
    text = args.message
    categories = classify(text)
    channel = detect_channel(text)
    tone = detect_tone(text)
    mode = detect_mode(text)
    files = [route(c["category"]) for c in categories]

    significant_cats = [c for c in categories if c["score"] >= CROSS_TOPIC_THRESHOLD]
    is_cross_topic = len(significant_cats) > 1

    result = {
        "categories": categories,
        "primary_category": categories[0]["category"] if categories else "library",
        "files": files,
        "channel": channel,
        "tone": tone,
        "mode": mode,
        "cross_topic": is_cross_topic,
        "diagnostic_hint": "Read the listed files, match 3+ cases, then produce 6-dimension output.",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_route(args):
    print(route(args.category))


def cmd_validate(args):
    content = Path(args.output_file).read_text(encoding="utf-8")
    result = validate_output(content)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["valid"] else 1)


def cmd_channel(args):
    channel = detect_channel(args.message)
    print(json.dumps({"channel": channel}, indent=2))


def cmd_tone(args):
    tone = detect_tone(args.message)
    print(json.dumps({"tone": tone}, indent=2))


def cmd_batch(args):
    input_path = Path(args.input_file)
    lines = input_path.read_text(encoding="utf-8").strip().split("\n")
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        categories = classify(line)
        channel = detect_channel(line)
        tone = detect_tone(line)
        mode = detect_mode(line)
        results.append({
            "input": line,
            "categories": categories,
            "primary_category": categories[0]["category"] if categories else "library",
            "channel": channel,
            "tone": tone,
            "mode": mode,
        })
    print(json.dumps(results, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Trade Email Case Copilot CLI"
    )
    sub = parser.add_subparsers(dest="command")

    p_diag = sub.add_parser("diagnose", help="Classify a customer message")
    p_diag.add_argument("message", help="Customer message text")
    p_diag.set_defaults(func=cmd_diagnose)

    p_route = sub.add_parser("route", help="Resolve category to file path")
    p_route.add_argument(
        "category",
        choices=list(CATEGORY_MAP.keys()),
    )
    p_route.set_defaults(func=cmd_route)

    p_val = sub.add_parser("validate", help="Validate output completeness")
    p_val.add_argument("output_file", help="Path to output file to validate")
    p_val.set_defaults(func=cmd_validate)

    p_chan = sub.add_parser("channel", help="Detect communication channel")
    p_chan.add_argument("message", help="User message text")
    p_chan.set_defaults(func=cmd_channel)

    p_tone = sub.add_parser("tone", help="Detect requested tone")
    p_tone.add_argument("message", help="User message text")
    p_tone.set_defaults(func=cmd_tone)

    p_batch = sub.add_parser("batch", help="Batch diagnose from file")
    p_batch.add_argument("input_file", help="File with one message per line")
    p_batch.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
