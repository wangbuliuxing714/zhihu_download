@echo off
chcp 65001 >nul
title 知乎盐选工具 - 启动中...
echo.
echo ========================================
echo    知乎盐选工具 - 图形界面
echo ========================================
echo.
echo 正在启动程序...
echo.
python run_gui.py
if errorlevel 1 (
    echo.
    echo ========================================
    echo    启动失败！
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. 未安装Python
    echo 2. 未安装依赖包
    echo.
    echo 解决方法：
    echo 1. 安装Python 3.x
    echo 2. 运行: pip install -r requirements.txt
    echo.
    pause
)

