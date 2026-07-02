# -*- coding: utf-8 -*-
"""
alibaba-hero-image-gen sanity_check.py
Skill 体检脚本 — 必须全部断言通过才允许交付
运行方式: python scripts/sanity_check.py --skill-dir .
"""

import sys
import os
import json
import re
import argparse

SKILL_NAME = "alibaba-hero-image-gen"
REQUIRED_TRIGGER_WORDS = 6
REQUIRED_ASSERTIONS_IN_SANITY = 7
REDLINE_COUNT = 6

def fail(msg: str):
    print(f"❌ FAIL: {msg}")
    sys.exit(1)

def warn(msg: str):
    print(f"🟡 WARN: {msg}")

def ok(msg: str):
    print(f"✅  OK : {msg}")


def assert_file_exists(path: str, label: str):
    if not os.path.isfile(path):
        fail(f"[S1] 文件不存在: {label} ({path})")
    ok(f"[S1] 文件存在: {label}")


def assert_manifest_valid(manifest_path: str):
    try:
        with open(manifest_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        fail(f"[S2] manifest.json 解析失败: {e}")

    required_keys = ["name", "version", "description", "trigger_keywords"]
    for k in required_keys:
        if k not in data:
            fail(f"[S2] manifest.json 缺少必填字段: {k}")

    if not data.get("version"):
        fail("[S2] manifest.json 缺少 version 字段，禁止 fallback 占位")
    version = data["version"]
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        fail(f"[S2] version 不符合 semver: {version!r}")

    ok(f"[S2] manifest.json 合法，version={version}")


def assert_trigger_words(manifest_path: str):
    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)

    keywords = data.get("trigger_keywords", [])
    if len(keywords) < REQUIRED_TRIGGER_WORDS:
        fail(
            f"[S3] trigger_keywords 数量不足: 需要 ≥{REQUIRED_TRIGGER_WORDS}，"
            f"实际 {len(keywords)}"
        )
    ok(f"[S3] 触发词数量合格: {len(keywords)} 个")


def assert_skill_md_frontmatter(skill_md_path: str):
    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        fail("[S4] SKILL.md 缺少 frontmatter（应以 --- 开头）")

    end = content.find("---", 3)
    if end == -1:
        fail("[S4] SKILL.md frontmatter 未正确闭合（缺少结尾 ---）")

    frontmatter = content[3:end]
    for field in ["name:", "version:", "description:"]:
        if field not in frontmatter:
            fail(f"[S4] SKILL.md frontmatter 缺少字段: {field}")

    ok("[S4] SKILL.md frontmatter 合法")


def assert_redline_table(skill_md_path: str):
    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    if "反 AI 偷懒条款" not in content:
        fail("[S5] SKILL.md 缺少「反 AI 偷懒条款」红线表")

    redline_rows = re.findall(r"\|\s*R\d+\s*\|", content)
    if len(redline_rows) < REDLINE_COUNT:
        fail(
            f"[S5] 反偷懒红线数量不足: 需要 ≥{REDLINE_COUNT}，"
            f"实际 {len(redline_rows)}"
        )
    ok(f"[S5] 反 AI 偷懒红线 {len(redline_rows)} 条，合格")


def assert_five_questions_present(skill_md_path: str):
    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    questions_found = len(re.findall(r"Q[1-5]\.", content))
    if questions_found < 5:
        fail(f"[S6] SKILL.md 中 5 问内容不完整，仅发现 {questions_found} 个 Q 标记")
    ok(f"[S6] 5 问内容完整（发现 {questions_found} 处 Q 标记）")


def assert_no_fallback_patterns(scripts_dir: str):
    patterns = [
        re.compile(r'\.get\([^,]+,\s*["\']'),
        re.compile(r'\sor\s+["\']'),
        re.compile(r'default=["\']'),
    ]
    hits = []
    for fname in os.listdir(scripts_dir):
        if not fname.endswith(".py") or fname == "sanity_check.py":
            continue
        fpath = os.path.join(scripts_dir, fname)
        with open(fpath, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                for pat in patterns:
                    if pat.search(line):
                        hits.append(f"{fname}:{lineno}  {line.rstrip()}")

    if hits:
        fail(
            f"[S7] 检测到 fallback 反模式（共 {len(hits)} 处），必须改为 fail-fast:\n"
            + "\n".join(f"  → {h}" for h in hits)
        )
    ok("[S7] 无 fallback 反模式，fail-fast 合规")


def assert_example_positive_negative(skill_md_path: str):
    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    positive = content.count("✅ 正例")
    negative = content.count("❌ 反例")
    if positive < 1 or negative < 1:
        fail(f"[S8] 缺少正例/反例对照（正例 {positive} 个，反例 {negative} 个），需各 ≥1")
    ok(f"[S8] 正例 {positive} 个 / 反例 {negative} 个，范式对照合格")


def assert_three_stage_sop(skill_md_path: str):
    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    stages = ["第 1 段", "第 2 段", "第 3 段"]
    missing = [s for s in stages if s not in content]
    if missing:
        fail(f"[S9] 三段式 SOP 不完整，缺少: {missing}")
    ok("[S9] 三段式 SOP 完整（第1/2/3段均存在）")


def assert_customer_chant_template(skill_md_path: str):
    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    if "客户喊话模板" not in content:
        fail("[S10] SKILL.md 缺少「客户喊话模板」段落")
    ok("[S10] 客户喊话模板存在")


def assert_output_spec_present(skill_md_path: str):
    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    if "输出基准" not in content:
        fail("[S11] SKILL.md 缺少「输出基准」规格表")
    ok("[S11] 输出基准规格表存在")


def run_all(skill_dir: str):
    print("=" * 50)
    print(f"  Skill 体检报告 - {SKILL_NAME}")
    print(f"  Path: {os.path.abspath(skill_dir)}")
    print("=" * 50)

    skill_md = os.path.join(skill_dir, "SKILL.md")
    manifest = os.path.join(skill_dir, "manifest.json")
    scripts_dir = os.path.join(skill_dir, "scripts")
    sanity_py = os.path.join(scripts_dir, "sanity_check.py")

    assert_file_exists(skill_md, "SKILL.md")
    assert_file_exists(manifest, "manifest.json")
    assert_file_exists(sanity_py, "scripts/sanity_check.py")

    assert_manifest_valid(manifest)
    assert_trigger_words(manifest)
    assert_skill_md_frontmatter(skill_md)
    assert_redline_table(skill_md)
    assert_five_questions_present(skill_md)
    assert_no_fallback_patterns(scripts_dir)
    assert_example_positive_negative(skill_md)
    assert_three_stage_sop(skill_md)
    assert_customer_chant_template(skill_md)
    assert_output_spec_present(skill_md)

    print("-" * 50)
    print("🟢 全部 11 项断言通过 — Skill 体检 PASS，可交付")
    print("-" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="alibaba-hero-image-gen sanity check")
    parser.add_argument(
        "--skill-dir",
        default=".",
        help="Skill 根目录路径（默认当前目录）"
    )
    args = parser.parse_args()
    run_all(args.skill_dir)
