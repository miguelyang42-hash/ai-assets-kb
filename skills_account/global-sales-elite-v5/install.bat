@echo off
REM ============================================================
REM  精细化开发-小蜂学掌 V5.3 - Windows 一键安装脚本
REM ============================================================
chcp 65001 > nul
echo.
echo ===== 小蜂学掌 V5.3 工程化版 - 安装开始 =====
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [FAIL] 未检测到 Python，请先安装 Python 3.9+：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Python 版本：
python --version

echo.
echo [2/3] 安装依赖（python-docx / openpyxl / jsonschema）...
python -m pip install --upgrade pip
python -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo [FAIL] 依赖安装失败，请检查网络或代理。
    pause
    exit /b 1
)

echo.
echo [3/3] 运行十项工程自检...
python "%~dp0scripts\self_check.py"
if errorlevel 1 (
    echo.
    echo [WARN] 自检未全绿，请截图给开发者。
    pause
    exit /b 1
)

echo.
echo ===== 安装完成！现在可以运行： =====
echo   python main.py payload.json
echo.
pause
