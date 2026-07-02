# -*- coding: utf-8 -*-
"""
精细化开发-小蜂学掌 V5.4（小蜂学掌定制版）- main.py
统一入口：路径计算 + payload 校验 + Word/Excel 同步生成。

新增（v5.4）:
  - 启动品牌通知框（╔══╗格式）
  - 生成完成后输出文件绝对路径通知框
  - 文件名前缀：小蜂学掌_
  - Word 封面 + 页眉页脚品牌注入
  - Excel 品牌表头/金色条/版权表尾

跨平台运行：自动按 Win/Mac/Linux 选择默认输出目录。
仅依赖：python-docx, openpyxl, jsonschema。

用法：
  python main.py <payload_json>
  python main.py <payload_json> --out-dir "D:/some/path"
退出码：
  0 = 成功；1 = 校验失败；2 = 平台/环境失败；3 = IO 失败。
"""
from __future__ import annotations
import sys, os, json, time, argparse, platform, traceback
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "scripts"))

from scripts.word_gen import create_pro_report    # noqa: E402
from scripts.excel_sync import sync_excel         # noqa: E402

# ── 品牌常量 ──
BRAND_NAME = "小蜂学掌"
BRAND_URL  = "www.xfxz123.com"


def print_brand_startup():
    """启动时输出小蜂学掌品牌通知框（铁律 #0）。"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🐝 小蜂学掌 × 精细化开发系统  V5.4                        ║")
    print("║  www.xfxz123.com  |  global-sales-elite-v5                  ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  正在启动 5 大渠道开发引擎 + Word/Excel 品牌输出…            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def print_delivery_box(word_path: str | None, excel_path: str | None, run_id: str):
    """生成完成后输出文件绝对路径通知框。"""
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  ✅ 小蜂学掌 精细化开发报告 — 生成成功！                    ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    if word_path:
        short_w = word_path if len(word_path) <= 52 else "..." + word_path[-49:]
        print("║  📄 Word 完整路径：                                          ║")
        print(f"║    {short_w:<58}║")
    if excel_path:
        short_e = excel_path if len(excel_path) <= 52 else "..." + excel_path[-49:]
        print("║  📊 Excel 完整路径：                                         ║")
        print(f"║    {short_e:<58}║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  💡 在 Windows 资源管理器地址栏粘贴路径可直接打开文件        ║")
    print(f"║  🔑 run_id: {run_id:<50}║")
    print("╚══════════════════════════════════════════════════════════════╝")


def load_manifest() -> dict:
    with open(HERE / "manifest.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_default_out_root(manifest: dict) -> Path:
    sysname = platform.system().lower()
    key = "macos" if sysname == "darwin" else ("windows" if sysname.startswith("win") else "linux")
    raw = manifest.get("default_out_dir", {}).get(key, "~/Desktop")
    return Path(os.path.expanduser(raw)).resolve()


def validate_payload(payload: dict) -> tuple[bool, str]:
    try:
        from jsonschema import Draft7Validator
    except ImportError:
        return False, "jsonschema 未安装；请 pip install jsonschema"
    with open(HERE / "payload.schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if not errors:
        return True, "ok"
    msgs = []
    for e in errors[:10]:
        path = ".".join(str(p) for p in e.path) or "(root)"
        msgs.append(f"  - {path}: {e.message}")
    return False, "ValidationError:\n" + "\n".join(msgs)


def compute_project_dir(out_root: Path, payload: dict) -> Path:
    country = payload.get("country", "Unknown")
    segment = payload.get("segment", "Unknown")
    yyyymmdd = datetime.now().strftime("%Y%m%d")
    folder = f"{country}_{segment}_{yyyymmdd}"
    return out_root / folder


def compute_excel_path(project_dir: Path, payload: dict) -> Path:
    country = payload.get("country", "Unknown")
    segment = payload.get("segment", "Unknown")
    yyyymmdd = datetime.now().strftime("%Y%m%d")
    # 文件名带品牌前缀
    return project_dir / f"{BRAND_NAME}_{country}{segment}{yyyymmdd}.xlsx"


def setup_logger(project_dir: Path) -> tuple[Path, str]:
    logs_dir = project_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_") + str(int(time.time() * 1000))[-4:]
    log_path = logs_dir / f"{run_id}.log"
    return log_path, run_id


def write_log(log_path: Path, msg: str) -> None:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")


def main():
    # ── 铁律 #0：启动品牌通知框 ──
    print_brand_startup()

    parser = argparse.ArgumentParser(description="小蜂学掌 V5.4 精细化开发主入口")
    parser.add_argument("payload", help="payload JSON 文件路径")
    parser.add_argument("--out-dir", default=None, help="覆盖默认输出根目录")
    parser.add_argument("--no-excel", action="store_true", help="只生成 Word，不写 Excel")
    parser.add_argument("--no-word", action="store_true", help="只追加 Excel，不生成 Word")
    args = parser.parse_args()

    payload_path = Path(args.payload).resolve()
    if not payload_path.exists():
        print(f"[FATAL] payload 文件不存在: {payload_path}")
        sys.exit(3)

    try:
        with open(payload_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception as e:
        print(f"[FATAL] payload 解析失败: {e}")
        sys.exit(3)

    ok, msg = validate_payload(payload)
    if not ok:
        print(f"[VALIDATION_FAILED]\n{msg}")
        sys.exit(1)

    try:
        manifest = load_manifest()
        out_root = Path(os.path.expanduser(args.out_dir)).resolve() if args.out_dir else get_default_out_root(manifest)
        out_root.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[PLATFORM_FAILED] 平台路径初始化失败: {e}")
        sys.exit(2)

    project_dir = compute_project_dir(out_root, payload)
    project_dir.mkdir(parents=True, exist_ok=True)
    excel_path = compute_excel_path(project_dir, payload)
    log_path, run_id = setup_logger(project_dir)

    write_log(log_path, f"run_id={run_id} channel={payload.get('channel')} country={payload.get('country')} segment={payload.get('segment')}")
    write_log(log_path, f"project_dir={project_dir}")
    write_log(log_path, f"excel_path={excel_path}")

    word_path_final = None
    excel_path_final = None

    try:
        if not args.no_word:
            word_path_final = create_pro_report(str(payload_path), str(project_dir))
            write_log(log_path, f"WORD_OK: {word_path_final}")

        if not args.no_excel:
            excel_path_final = sync_excel(str(payload_path), str(excel_path))
            write_log(log_path, f"EXCEL_OK: {excel_path_final}")

    except Exception as e:
        write_log(log_path, f"ERROR: {e}\n{traceback.format_exc()}")
        print(f"[IO_FAILED] {e}")
        sys.exit(3)

    write_log(log_path, "DONE")

    # ── 生成完成：输出绝对路径通知框 ──
    print_delivery_box(word_path_final, excel_path_final, run_id)

    print(f"[DONE] run_id={run_id}")
    sys.exit(0)


if __name__ == "__main__":
    main()
