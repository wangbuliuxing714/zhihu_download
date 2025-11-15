# ZhiHu Tools

知乎盐选文章获取工具，专业的内容提取解决方案。

## ⚠️ 重要声明

**本项目仅供学习和研究使用，请勿用于商业用途或其他违反知乎服务条款的行为。**

使用本工具时，请遵守以下原则：
- 仅用于个人学习和技术研究
- 尊重知识产权，不得传播或商用获取的内容
- 遵守知乎平台的服务条款和相关法律法规
- 建议支持原创作者，购买正版内容

## 🙏 致谢

本项目 Fork 自原作者 [@onewhitethreee](https://github.com/onewhitethreee) 的开源项目：
- **原始仓库**: [https://github.com/onewhitethreee/zhihu_tools](https://github.com/onewhitethreee/zhihu_tools)

感谢原作者的无私分享和卓越贡献，为技术学习者提供了宝贵的学习资源。本仓库的所有核心功能和代码均来自原作者的辛勤工作。

**本仓库仅用于个人学习和研究，所有权利归原作者所有。**

如果您是原作者并对本仓库有任何疑问或建议，请随时联系我，我会立即处理。

## 项目概述



## 最新更新

### 2025年11月15日 v2.1
- ✅ 全新现代化图形界面上线
- ✅ 支持可视化配置管理
- ✅ 实时日志显示
- ✅ 多线程爬取，界面不卡顿
- ✅ 一键启动，操作更简单
- ✅ 修复HTML标签问题，输出纯文本内容
- ✅ 自动代理回退机制，网络更稳定

### 2025年3月8日
- 感谢 [@Xmug](https://github.com/Xmug) 贡献的PR，修复了多个bug

### 2024年4月20日
- 完成代码重构和架构优化

## 项目结构
```
├─answerSpider      # 问题回答提取模块
├─config            # 配置设置
├─ddddocr           # OCR功能组件
├─fakeUserAgent     # 请求头管理
├─fontPreview       # 字体问题解决工具
├─gui               # 图形界面模块 ⭐新增
├─main              # 核心执行脚本
├─marketSpider      # 市场内容提取模块
├─run_gui.py        # GUI启动脚本 ⭐新增
└─启动GUI.bat       # Windows一键启动 ⭐新增
```

## 开发路线图

| 功能 | 状态 |
|---------|--------|
| 动态请求头生成 | ✅ 已完成 |
| 字体解码与渲染问题 | ✅ 已完成 |
| 单一问题内容提取 | ⏳ 开发中 |
| 市场链接内容提取 | ✅ 已完成 |
| 完整书籍采集 | ⏳ 开发中 |
| 图形界面实现 | ✅ 已完成 |
| 基于关键词的内容搜索 | ⏳ 计划中 |

## 系统要求

- Python 3.x 环境
- 有效的知乎盐选会员账号
- 网络检测工具（用于获取必要的认证信息）

## 安装与使用

### 方式一：图形界面（推荐）⭐

#### Windows用户（最简单）
1. 将此仓库克隆到本地
2. 双击运行 `启动GUI.bat`
3. 在界面中配置Cookie并开始使用

#### 所有平台
1. 将此仓库克隆到本地
2. 进入项目目录
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 启动图形界面：
   ```bash
   python run_gui.py
   ```
5. 在界面中配置Cookie并开始使用

**详细使用说明请查看：[GUI使用指南](GUI_USAGE.md)**

### 方式二：命令行

1. 将此仓库克隆到本地
2. 进入项目目录
3. 在 `config.ini` 中配置您的认证信息
4. 执行主脚本：
   ```bash
   python main/spider.py
   ```

## 功能指南

### 图形界面使用说明

1. **配置Cookie**（⭐[看不懂？点这里查看超详细图文教程](如何获取Cookie.md)）
   - 在浏览器中登录知乎（需要盐选会员）
   - 按F12打开开发者工具 → Network（网络）标签
   - 刷新页面（按F5），找到第一个请求
   - 在右侧找到 Request Headers（请求标头）→ cookie
   - 复制cookie后面的整个值
   - 粘贴到GUI的Cookie输入框并保存

   **快速方法**：打开开发者工具Console标签，输入 `document.cookie` 并回车，复制结果

2. **选择功能**
   - 目前支持"爬取书的单个章节"功能
   - 其他功能正在开发中

3. **输入链接**
   - 输入知乎市场章节链接
   - 示例格式：`https://www.zhihu.com/market/paid_column/1702723501155422208/section/1788920608135983104`

4. **开始爬取**
   - 点击"开始爬取"按钮
   - 在日志窗口查看实时进度
   - 完成后文件会保存在项目目录

### 命令行功能说明

### 选项1：基于问题的内容提取
提取带有"question"标识符的文章内容。由于知乎平台变更，这些链接需要特定格式，可能需要通过网络检测获取。

### 选项2：市场内容提取
使用正确格式的URL从知乎市场提取内容。

示例链接格式：
```
https://www.zhihu.com/market/paid_column/1702723501155422208/section/1788920608135983104
```

### 选项3：完整书籍提取
提取整本盐选书籍的功能正在开发中。

### 选项4：基于关键词的内容获取
此功能旨在解决知乎网页界面重定向到移动应用并提供特定关键词的情况。开发进行中。

## 故障排除

### 常见问题

**模块缺失错误**
- 使用pip安装所需依赖：
  ```
  pip install -r requirements.txt
  ```

**代理错误（ProxyError）**
- 本工具自动使用系统代理
- 如果使用Clash/V2Ray等代理软件，请确保：
  1. 代理软件正在运行
  2. 系统代理已开启
- 详细解决方案请查看：[代理配置说明.md](代理配置说明.md)

**内容获取失败**
- 确保您拥有有效的知乎盐选会员账号
- 验证您的认证cookie是否正确配置
- 检查您的User-Agent字符串是否合适（推荐使用移动设备格式）
- 项目包含多个User-Agent选项；如果初始尝试失败，请重试

**其他技术问题**
- 请创建issue并提供完整的错误详情
- 遵循[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way)中的最佳实践

## 法律与道德考量

本工具设计用于个人存档合法可访问的盐选内容。用户有责任确保其使用符合知乎服务条款和适用法律。

## 贡献指南

如果您想为此项目做出贡献，请访问原作者的仓库：
- **原始仓库**: [https://github.com/onewhitethreee/zhihu_tools](https://github.com/onewhitethreee/zhihu_tools)

请遵循标准GitHub工作流：
1. Fork原作者的仓库
2. 创建功能分支
3. 提交包含清晰文档的Pull Request到原仓库

---

## 📌 版权声明

本仓库是原作者 [@onewhitethreee](https://github.com/onewhitethreee) 项目的学习副本。

- **原始项目**: [https://github.com/onewhitethreee/zhihu_tools](https://github.com/onewhitethreee/zhihu_tools)
- **用途**: 仅供个人学习和技术研究
- **版权**: 所有权利归原作者所有
- **免责声明**: 本仓库维护者不对使用本工具产生的任何后果负责

如需商业用途或其他需求，请联系原作者：twaapot@gmail.com

---

**⭐ 如果这个项目对你有帮助，请给原作者的仓库点个Star！**

**原仓库地址**: [https://github.com/onewhitethreee/zhihu_tools](https://github.com/onewhitethreee/zhihu_tools)


