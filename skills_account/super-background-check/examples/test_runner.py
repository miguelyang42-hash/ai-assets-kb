# -*- coding: utf-8 -*-
"""
Super Background Check v2.4 - End-to-End Smoke Test

跑 4 个场景：
1. happy path:    mock_payload → excel_gen → sanity 应 13/13 PASS
2. lazy 简化版:    裸 openpyxl 1 Sheet → sanity 应 S02 FAIL exit(1)
3. 短话术:        篡改 dim9_pitches[0] = "太短" → sanity 应 S12 FAIL
4. 文件名漂移:    重命名为 "背调报告_xxx.xlsx" → sanity 应 S09 FAIL

用法：
    python examples/test_runner.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_GEN = os.path.join(ROOT, "scripts", "excel_gen.py")
SANITY = os.path.join(ROOT, "scripts", "sanity_check.py")
MOCK = os.path.join(ROOT, "examples", "mock_payload.json")


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(p.stdout)
    if p.stderr:
        print("STDERR:", p.stderr)
    return p.returncode


def main():
    tmp = tempfile.mkdtemp(prefix="sbc24_test_")
    print(f"[TEST] workdir = {tmp}")

    payload = json.load(open(MOCK, "r", encoding="utf-8"))
    company_short = payload["company_short"]
    date_str = payload["date_str"]
    fname = f"单客户档案_{company_short}_{date_str}.xlsx"
    out = os.path.join(tmp, fname)

    failures = []

    # ---- Test 1: Happy path ----
    print("\n" + "=" * 60)
    print("TEST 1: Happy path - 应 13/13 PASS")
    print("=" * 60)
    rc = run([sys.executable, EXCEL_GEN, "--payload", MOCK, "--out", out])
    if rc != 0:
        failures.append("T1.gen")
    rc = run([sys.executable, SANITY, "--xlsx", out])
    if rc != 0:
        failures.append("T1.sanity")
    else:
        print("✅ T1 PASS")

    # ---- Test 2: Lazy 简化版 ----
    print("\n" + "=" * 60)
    print("TEST 2: 裸 openpyxl 1 Sheet - 应 sanity FAIL")
    print("=" * 60)
    from openpyxl import Workbook
    wb = Workbook()
    wb.active.title = "简化版"
    wb.active["A1"] = "客户名"
    wb.active["B1"] = "Acme"
    lazy_path = os.path.join(tmp, fname.replace(".xlsx", "_lazy.xlsx"))
    # 强制使用合规文件名以隔离 S09 干扰
    lazy_path2 = os.path.join(tmp, f"单客户档案_{company_short}lazy_{date_str}.xlsx")
    wb.save(lazy_path2)
    rc = run([sys.executable, SANITY, "--xlsx", lazy_path2])
    if rc == 0:
        failures.append("T2.expected_FAIL_but_PASS")
    else:
        print("✅ T2 PASS（确认拦截 lazy 简化版）")

    # ---- Test 3: 短话术 ----
    print("\n" + "=" * 60)
    print("TEST 3: 篡改话术为「太短」- 应 sanity S12 FAIL")
    print("=" * 60)
    bad_payload = json.loads(json.dumps(payload))
    bad_payload["company_short"] = "Bad3"
    bad_payload["dim9_pitches"][0] = "太短"
    bad_p_path = os.path.join(tmp, "bad_short_pitch.json")
    bad_out = os.path.join(tmp, f"单客户档案_Bad3_{date_str}.xlsx")
    json.dump(bad_payload, open(bad_p_path, "w", encoding="utf-8"), ensure_ascii=False)
    rc = run([sys.executable, EXCEL_GEN, "--payload", bad_p_path, "--out", bad_out])
    if rc != 0:
        failures.append("T3.gen_unexpected_fail")
    else:
        rc = run([sys.executable, SANITY, "--xlsx", bad_out])
        if rc == 0:
            failures.append("T3.expected_FAIL_but_PASS")
        else:
            print("✅ T3 PASS（确认拦截短话术）")

    # ---- Test 4: 文件名漂移 ----
    print("\n" + "=" * 60)
    print("TEST 4: 文件名漂移 - excel_gen 应 fail-fast")
    print("=" * 60)
    drift_out = os.path.join(tmp, f"背调报告_{company_short}_{date_str}.xlsx")
    rc = run([sys.executable, EXCEL_GEN, "--payload", MOCK, "--out", drift_out])
    if rc == 0:
        failures.append("T4.expected_FAIL_but_PASS")
    else:
        print("✅ T4 PASS（确认拦截文件名漂移）")

    # ---- 总结 ----
    print("\n" + "=" * 60)
    if failures:
        print(f"❌ {len(failures)} 个测试未达预期: {failures}")
        sys.exit(1)
    else:
        print("✅ ALL 4 TESTS PASSED — v2.4 双向验证通过")
        print(f"📁 测试产物保留于: {tmp}")
    sys.exit(0)


if __name__ == "__main__":
    main()
