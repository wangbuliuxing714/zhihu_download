# 此类用于爬取链接中带有market的数据
import os, sys

import requests
from lxml import etree
import re
import base64
import sys
import os
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import fontPreview


class MarketSpider:
    def __init__(self, header) -> None:
        self.header = header
        self.marketTitle = None
        self.glyfDict = {}
        self.url = None  # 保存初始URL

        # 配置代理设置
        self.session = requests.Session()
        self.session.trust_env = True  # 使用系统环境变量中的代理设置

        # 禁用SSL验证警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def getMarketHtml(self, url):
        """请求知乎市场页面 HTML，优先使用系统代理，失败时自动回退为直连"""
        self.url = url  # 保存URL
        response = None

        # 先尝试使用系统代理
        try:
            logging.info("正在通过系统代理请求文章...")
            logging.info(f"当前代理配置: {self.session.proxies}")
            response = self.session.get(url, verify=False, headers=self.header, timeout=30)
        except requests.exceptions.ProxyError as e:
            # 系统代理不可用的典型情况：本地代理软件未启动 / 配置错误
            logging.error(f"通过系统代理请求失败: {e}")
            logging.info("将尝试在不使用代理的情况下直连知乎...")

            try:
                direct_session = requests.Session()
                direct_session.trust_env = False  # 显式禁用环境代理
                response = direct_session.get(url, verify=False, headers=self.header, timeout=30)
                logging.info("直连知乎成功，已绕过系统代理访问")
            except Exception as e2:
                logging.error(f"直连知乎同样失败: {e2}")
                # 抛出给上层，由 GUI 统一提示
                raise
        except requests.exceptions.RequestException as e:
            # 其他网络相关错误
            logging.error(f"请求知乎失败：{e}")
            raise

        # 如果仍然没有拿到 response，直接返回失败
        if response is None:
            logging.error("未能获取到知乎响应，终止后续处理")
            return

        # 将 HTML 写入本地文件
        try:
            with open("market.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            logging.info("文章请求成功！")
        except Exception as e:
            logging.error("文章写入失败：%s", str(e))

    def re_fetch_article(self):
        """
        重新请求文章，更新HTML和字体文件
        """
        logging.info("重新请求文章...")
        self.getMarketHtml(self.url)  # 重新下载HTML
        self.getFontFile()  # 重新获取字体文件
        self.getContent()

        # 获取字体文件并且下载

    def getFontFile(self, htmlFile="market.html"):
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()
        fontFile = self.get_third_font_face(html)
        if fontFile == "":
            logging.error("未匹配到字体文件！")
            return
        parts = fontFile.split(",")
        if len(parts) != 2:
            logging.error("无效的字体数据URL！")
            return
        # 获取数据部分
        data = parts[1]
        try:
            # 将数据进行解码
            data_bytes = base64.b64decode(data)
            # 将解码后的数据保存到文件
            with open("font.woff", "wb") as file:
                file.write(data_bytes)
            logging.info("字体文件下载成功！")
        except Exception as e:
            logging.error("字体文件下载失败:", str(e))

    # 获取第三个字体文件。应该为被动调用
    def get_third_font_face(self, font_re):
        font_face_blocks = re.findall(r"@font-face\s*{[^}]*}", font_re)
        # 获取第三个 @font-face 规则块
        if len(font_face_blocks) >= 3:
            font_face_blocks = re.findall(r"@font-face\s*{[^}]*}", font_re)
            font_url = re.search(r"src:\s*url\(([^)]+)\)", font_face_blocks[2]).group(1)
            return font_url
        else:
            return ''

    # 获取正文
    def getContent(self, htmlFile="market.html") -> bool:
        with open(htmlFile, "r", encoding="utf-8") as f:
            html = f.read()

        if not html:
            logging.error("在获取文件的时候出错了！")
            return False

        content = etree.HTML(html)
        content = content.xpath('string(//*[@id="resolved"])')
        content = json.loads(content)
        contents = content["appContext"]["__connectedAutoFetch"]["manuscript"]["data"][
            "manuscriptData"
        ]["pTagList"]  # 获取内容

        self.marketTitle = content["appContext"]["__connectedAutoFetch"]["manuscript"]["data"][
                               "manuscriptData"
                           ]["title"] + ".txt"  # 获取标题

        # 清理HTML标签
        with open(self.marketTitle + ".temp", "w", encoding="utf-8") as f:
            for item in contents:
                # 移除所有HTML标签
                clean_text = re.sub(r'<[^>]+>', '', item)
                # 移除多余的空白字符
                clean_text = clean_text.strip()
                if clean_text:  # 只写入非空内容
                    f.write(clean_text + "\n")
        logging.info("内容获取成功！")
        return True

    # 替换正文中的文字
    def replace_text(self, text, replacement_dict):
        result = []
        for char in text:
            if char in replacement_dict:
                result.append(replacement_dict[char])
            else:
                result.append(char)
        return "".join(result)

    # 解析字体文件
    def parse(self):
        font_preview = fontPreview.FontPreview()
        font_preview.set_market_spider(self)  # 关联MarketSpider实例
        self.glyfDict = font_preview.preview("font.woff", "images")
        logging.info(f"字体映射表: {self.glyfDict}")  # 打印映射表以验证
        with open(self.marketTitle + ".temp", "r", encoding="utf-8") as f:
            content = f.read()
        content = self.replace_text(content, self.glyfDict)
        with open(self.marketTitle, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info("文章解析成功！")

    def spider(self, url):
        self.getMarketHtml(url)
        self.getFontFile()
        if self.getContent():
            self.parse()

