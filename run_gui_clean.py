"""
知乎盐选工具 - GUI启动脚本（清除缓存版本）
"""
import sys
import os

# 禁用字节码缓存
sys.dont_write_bytecode = True

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行GUI
if __name__ == "__main__":
    print("正在启动知乎盐选工具图形界面...")
    from gui.main_window import main
    main()

