#!/usr/bin/env bash
# ============================================================
#  精细化开发-小蜂学掌 V5.3 - macOS / Linux 一键安装脚本
# ============================================================
set -e
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo
echo "===== 小蜂学掌 V5.3 工程化版 - 安装开始 ====="
echo

PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
  echo "[FAIL] 未检测到 Python，请先安装 Python 3.9+：https://www.python.org/downloads/"
  exit 1
fi

echo "[1/3] Python 版本："
$PY --version

echo
echo "[2/3] 安装依赖（python-docx / openpyxl / jsonschema）..."
$PY -m pip install --upgrade pip
$PY -m pip install -r "$HERE/requirements.txt"

echo
echo "[3/3] 运行十项工程自检..."
$PY "$HERE/scripts/self_check.py"

echo
echo "===== 安装完成！现在可以运行： ====="
echo "  python3 main.py payload.json"
echo
