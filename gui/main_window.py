# -*- coding: utf-8 -*-
"""
Zhihu Tools - Modern GUI
Main Window Module
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import datetime
import threading
import configparser

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ModernButton(tk.Canvas):
    """Modern Button Component"""
    def __init__(self, parent, text, command=None, bg_color="#4A90E2", hover_color="#357ABD", 
                 text_color="white", width=120, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        
        # Draw rounded rectangle button
        self.rect = self.create_rounded_rect(0, 0, width, height, radius=10, fill=bg_color)
        self.text_id = self.create_text(width/2, height/2, text=text, fill=text_color, 
                                       font=("Microsoft YaHei UI", 11, "bold"))
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Create rounded rectangle"""
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
                  x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
                  x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
                  x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        
    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        
    def on_click(self, event):
        if self.command:
            self.command()


class ZhihuToolsGUI:
    """Zhihu Tools Main Window"""
    def __init__(self, root):
        self.root = root
        self.root.title("知乎盐选工具 - 现代化界面")
        self.root.geometry("950x750")
        self.root.configure(bg="#F5F7FA")

        # Set minimum window size
        self.root.minsize(900, 700)
        
        # Try to set window icon
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Create main container
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI components"""
        # Header
        self.create_header()

        # Initialize log_text as None first
        self.log_text = None

        # Config section
        self.create_config_section()

        # Function selection section
        self.create_function_section()

        # URL input section
        self.create_url_section()

        # Action buttons section
        self.create_action_section()

        # Log section (put at bottom)
        self.create_log_section()

        # Initial welcome message
        self.log("欢迎使用知乎盐选工具！", "SUCCESS")
        self.log("请先配置Cookie，然后选择功能开始使用", "INFO")

        # Check proxy settings
        self.check_proxy_settings()
        
    def create_header(self):
        """Create header bar"""
        header_frame = tk.Frame(self.root, bg="#4A90E2", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="🔧 知乎盐选工具",
                              font=("Microsoft YaHei UI", 24, "bold"),
                              bg="#4A90E2", fg="white")
        title_label.pack(side=tk.LEFT, padx=30, pady=20)

        subtitle_label = tk.Label(header_frame, text="专业的内容提取解决方案",
                                 font=("Microsoft YaHei UI", 11),
                                 bg="#4A90E2", fg="#E8F4FF")
        subtitle_label.pack(side=tk.LEFT, padx=10, pady=20)
        
    def create_log_section(self):
        """Create log display section"""
        log_frame = tk.LabelFrame(self.root, text="📋 运行日志",
                                 font=("Microsoft YaHei UI", 12, "bold"),
                                 bg="#FFFFFF", fg="#333333",
                                 relief=tk.FLAT, bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

        # Log text box
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  font=("Consolas", 9),
                                                  bg="#1E1E1E", fg="#D4D4D4",
                                                  relief=tk.FLAT, bd=0,
                                                  wrap=tk.WORD,
                                                  height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure log color tags
        self.log_text.tag_config("INFO", foreground="#4EC9B0")
        self.log_text.tag_config("ERROR", foreground="#F48771")
        self.log_text.tag_config("SUCCESS", foreground="#B5CEA8")
        self.log_text.tag_config("WARNING", foreground="#DCDCAA")

    def create_config_section(self):
        """Create config section"""
        config_frame = tk.LabelFrame(self.root, text="⚙️ 配置管理",
                                    font=("Microsoft YaHei UI", 12, "bold"),
                                    bg="#FFFFFF", fg="#333333",
                                    relief=tk.FLAT, bd=2)
        config_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        # Cookie input
        cookie_container = tk.Frame(config_frame, bg="#FFFFFF")
        cookie_container.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(cookie_container, text="Cookie:",
                font=("Microsoft YaHei UI", 10),
                bg="#FFFFFF", fg="#666666").pack(side=tk.LEFT, padx=(0, 10))

        self.cookie_entry = tk.Entry(cookie_container,
                                     font=("Consolas", 10),
                                     bg="#F8F9FA", fg="#333333",
                                     relief=tk.FLAT, bd=0)
        self.cookie_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))

        # Save button
        save_btn = ModernButton(cookie_container, "保存配置",
                               command=self.save_config,
                               bg_color="#52C41A", hover_color="#3DA015",
                               width=100, height=36)
        save_btn.pack(side=tk.LEFT)

        # Load existing config
        self.load_config()

    def create_function_section(self):
        """Create function selection section"""
        func_frame = tk.LabelFrame(self.root, text="🎯 功能选择",
                                  font=("Microsoft YaHei UI", 12, "bold"),
                                  bg="#FFFFFF", fg="#333333",
                                  relief=tk.FLAT, bd=2)
        func_frame.pack(fill=tk.X, padx=20, pady=10)

        func_container = tk.Frame(func_frame, bg="#FFFFFF")
        func_container.pack(fill=tk.X, padx=15, pady=15)

        self.function_var = tk.StringVar(value="2")

        # Function options
        functions = [
            ("1", "爬取盐选单个问题", "⏳ 开发中"),
            ("2", "爬取书的单个章节", "✅ 可用"),
            ("3", "爬取整本书", "⏳ 开发中"),
            ("4", "关键词爬取", "⏳ 计划中")
        ]

        for idx, (value, text, status) in enumerate(functions):
            radio_frame = tk.Frame(func_container, bg="#FFFFFF")
            radio_frame.pack(side=tk.LEFT, padx=10)

            # Check if available
            state = tk.NORMAL if value == "2" else tk.DISABLED

            radio = tk.Radiobutton(radio_frame, text=text,
                                  variable=self.function_var, value=value,
                                  font=("Microsoft YaHei UI", 10),
                                  bg="#FFFFFF", fg="#333333",
                                  selectcolor="#E6F7FF",
                                  activebackground="#FFFFFF",
                                  state=state)
            radio.pack(side=tk.LEFT)

            status_label = tk.Label(radio_frame, text=status,
                                   font=("Microsoft YaHei UI", 9),
                                   bg="#FFFFFF",
                                   fg="#52C41A" if status.startswith("✅") else "#FAAD14")
            status_label.pack(side=tk.LEFT, padx=5)

    def create_url_section(self):
        """Create URL input section"""
        url_frame = tk.LabelFrame(self.root, text="🔗 链接输入",
                                 font=("Microsoft YaHei UI", 12, "bold"),
                                 bg="#FFFFFF", fg="#333333",
                                 relief=tk.FLAT, bd=2)
        url_frame.pack(fill=tk.X, padx=20, pady=10)

        url_container = tk.Frame(url_frame, bg="#FFFFFF")
        url_container.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(url_container, text="链接:",
                font=("Microsoft YaHei UI", 10),
                bg="#FFFFFF", fg="#666666").pack(side=tk.LEFT, padx=(0, 10))

        self.url_entry = tk.Entry(url_container,
                                 font=("Consolas", 10),
                                 bg="#F8F9FA", fg="#333333",
                                 relief=tk.FLAT, bd=0)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

        # Hint text
        hint_label = tk.Label(url_frame,
                             text="💡 示例: https://www.zhihu.com/market/paid_column/1702723501155422208/section/1788920608135983104",
                             font=("Microsoft YaHei UI", 9),
                             bg="#FFFFFF", fg="#999999")
        hint_label.pack(padx=15, pady=(0, 10), anchor=tk.W)

    def create_action_section(self):
        """Create action buttons section"""
        action_frame = tk.Frame(self.root, bg="#F5F7FA", height=70)
        action_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        action_frame.pack_propagate(False)

        # Button container
        btn_container = tk.Frame(action_frame, bg="#F5F7FA")
        btn_container.pack(expand=True)

        # Start button
        start_btn = ModernButton(btn_container, "🚀 开始爬取",
                                command=self.start_spider,
                                bg_color="#4A90E2", hover_color="#357ABD",
                                width=140, height=45)
        start_btn.pack(side=tk.LEFT, padx=10)

        # Clear log button
        clear_btn = ModernButton(btn_container, "🗑️ 清空日志",
                                command=self.clear_log,
                                bg_color="#8C8C8C", hover_color="#6B6B6B",
                                width=140, height=45)
        clear_btn.pack(side=tk.LEFT, padx=10)

        # About button
        about_btn = ModernButton(btn_container, "ℹ️ 关于",
                                command=self.show_about,
                                bg_color="#722ED1", hover_color="#531DAB",
                                width=140, height=45)
        about_btn.pack(side=tk.LEFT, padx=10)

    # ==================== Function Methods ====================

    def log(self, message, level="INFO"):
        """Add log"""
        if self.log_text is None:
            return  # Log widget not created yet

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, log_message, level)
        self.log_text.see(tk.END)
        self.root.update()

    def clear_log(self):
        """Clear log"""
        self.log_text.delete(1.0, tk.END)
        self.log("日志已清空", "INFO")

    def load_config(self):
        """Load config"""
        try:
            config_parser = configparser.ConfigParser(interpolation=None)
            config_parser.read("config.ini", encoding="utf-8")
            cookie = config_parser.get("DEFAULT", "Cookie")
            if cookie and cookie != "填入你抓取的Cookie":
                self.cookie_entry.insert(0, cookie)
                self.log("配置加载成功", "SUCCESS")
            else:
                self.log("请配置Cookie后使用", "WARNING")
        except Exception as e:
            self.log(f"配置加载失败: {str(e)}", "ERROR")

    def save_config(self):
        """Save config"""
        cookie = self.cookie_entry.get().strip()
        if not cookie:
            messagebox.showwarning("警告", "请输入Cookie！")
            return

        try:
            # Read config file with interpolation disabled
            config_parser = configparser.ConfigParser(interpolation=None)
            config_parser.read("config.ini", encoding="utf-8")

            # Update Cookie
            config_parser.set("DEFAULT", "Cookie", cookie)

            # Save config
            with open("config.ini", "w", encoding="utf-8") as f:
                config_parser.write(f)

            self.log("配置保存成功！", "SUCCESS")
            messagebox.showinfo("成功", "配置已保存！")
        except Exception as e:
            self.log(f"配置保存失败: {str(e)}", "ERROR")
            messagebox.showerror("错误", f"保存失败: {str(e)}")

    def start_spider(self):
        """Start crawling"""
        # Check Cookie
        cookie = self.cookie_entry.get().strip()
        if not cookie or cookie == "填入你抓取的Cookie":
            messagebox.showwarning("警告", "请先配置Cookie！")
            self.log("请先配置Cookie", "WARNING")
            return

        # Check URL
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入要爬取的URL！")
            self.log("请输入URL", "WARNING")
            return

        # Get selected function
        function = self.function_var.get()

        if function == "2":
            self.spider_market(url)
        else:
            messagebox.showinfo("提示", "该功能正在开发中，敬请期待！")
            self.log("该功能正在开发中", "WARNING")

    def spider_market(self, url):
        """Crawl market content"""

        def run_spider():
            try:
                self.log("=" * 50, "INFO")
                self.log("开始爬取市场内容...", "INFO")
                self.log(f"URL: {url}", "INFO")

                # Import spider modules
                import config
                import marketSpider
                import fakeUserAgent

                # Prepare request headers
                cfg = config.Config().getEnviroments()
                header = {}
                header["Cookie"] = self.cookie_entry.get().strip()
                header["User-Agent"] = cfg["User-Agent"] + " " + str(fakeUserAgent.fakeUserAgent().getRandomUserAgent())

                self.log("请求头配置完成", "SUCCESS")

                # Create spider instance
                market = marketSpider.MarketSpider(header)

                # Start crawling
                self.log("正在请求文章...", "INFO")
                market.getMarketHtml(url)

                self.log("正在下载字体文件...", "INFO")
                market.getFontFile()

                self.log("正在提取内容...", "INFO")
                if market.getContent():
                    self.log("正在解析字体...", "INFO")
                    market.parse()
                    self.log("=" * 50, "SUCCESS")
                    self.log(f"✅ 爬取成功！文件已保存: {market.marketTitle}", "SUCCESS")
                    messagebox.showinfo("成功", f"爬取成功！\n文件已保存: {market.marketTitle}")
                else:
                    self.log("内容提取失败", "ERROR")
                    messagebox.showerror("错误", "内容提取失败，请检查URL和Cookie是否正确")

            except Exception as e:
                self.log(f"爬取失败: {str(e)}", "ERROR")
                messagebox.showerror("错误", f"爬取失败:\n{str(e)}")

        # Run in new thread to avoid UI freeze
        thread = threading.Thread(target=run_spider, daemon=True)
        thread.start()

    def check_proxy_settings(self):
        """Check proxy settings"""
        import os
        http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
        https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')

        if http_proxy or https_proxy:
            self.log(f"检测到系统代理: {http_proxy or https_proxy}", "INFO")
            self.log("程序将使用系统代理访问网络", "INFO")
            self.log("如遇到代理错误，请确保代理软件正在运行", "WARNING")
        else:
            self.log("未检测到系统代理，将直接连接", "INFO")

    def show_about(self):
        """Show about info"""
        about_text = """
知乎盐选工具 v2.0

专业的知乎盐选内容提取解决方案

功能特性:
✅ 动态请求头生成
✅ 字体解码与渲染
✅ 市场内容提取
✅ 自动使用系统代理
⏳ 完整书籍采集（开发中）

项目地址:
https://github.com/onewhitethreee/zhihu_tools

使用说明:
1. 配置知乎Cookie
2. 选择功能类型
3. 输入要爬取的URL
4. 点击开始爬取

注意事项:
• 需要有效的知乎盐选会员账号
• Cookie会过期，请及时更新
• 仅供个人学习使用
• 如使用代理，请确保代理软件正在运行

作者: onewhitethreee
邮箱: twaapot@gmail.com
        """
        messagebox.showinfo("关于", about_text)


def main():
    """Main function"""
    root = tk.Tk()
    app = ZhihuToolsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

