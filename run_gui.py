"""
知乎盐选工具 - GUI启动脚本
直接运行此文件启动图形界面
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行GUI
from gui.main_window import main

if __name__ == "__main__":
    print("正在启动知乎盐选工具图形界面...")
    main()

