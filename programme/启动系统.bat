@echo off
chcp 65001 >nul
title 医院数据自动化系统

echo.
echo ============================================================
echo                    🏥 医院数据自动化系统
echo ============================================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python环境，请先安装Python
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 正在启动系统...
python start_system.py

echo.
echo 系统已退出
pause 