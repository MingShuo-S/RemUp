
---
<div align="center">
<a href="https://github.com/MingShuo-S/PPL_Project-RemUp">
    <img src="static/Logo.svg" alt="RemUp Logo" width="500" height="120" style="border-radius: 8px;  object-fit: cover;object-position: center; 
border: 0px solid #ddd;">
  </a>


# RemUp - 记忆辅助标记语言

**将结构化的知识转换为交互式学习卡片**

![GitHub Actions](https://img.shields.io/badge/Python-3.8+-blue)
![GitHub Actions](https://img.shields.io/badge/License-MIT-green)

</div>

***建议先看完[项目报告](Project_Report.md)再看本文件***
## 📖 项目介绍

RemUp 是一个创新的轻量级标记语言和编译器，专为构建"学习-理解-再学习"的记忆闭环而设计。它可以将结构化的知识转换为具有丰富交互功能的HTML学习卡片，支持主卡系统、注卡批注和智能归档，帮助用户高效构建个人知识体系。

### ✨ 核心特性

- **🎴 主卡系统** - 结构化知识承载，使用简洁的标记语法
- **💡 注卡系统** - 交互式批注，悬停显示，双向跳转
- **📚 归档系统** - 智能知识组织，自动生成导航
- **🎨 多主题支持** - 内置多种CSS主题，支持一键切换
- **🔗 智能链接** - 标签间快速跳转，构建知识网络
- **🌙 主题切换** - 支持默认、紧凑和夜间模式
- **🔥 实时预览** - 开发中的实时编译和预览功能
- **📦 静态资源管理** - 自动复制CSS文件，支持离线使用

## 🚀 快速开始

### 系统要求

- Python 3.8 或更高版本
- 现代浏览器（Chrome、Firefox、Safari等）

### 体验流程

1. **下载项目**
   从GitHub仓库下载压缩包并解压，或使用git克隆（或直接下载安装包）：
   ```bash
   git clone https://github.com/MingShuo-S/PPL_Project-RemUp.git
   cd PPL_Project-RemUp
   ```

2. **设置虚拟环境（推荐）**
   ```bash
   python -m venv venv
   # 激活环境
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. **安装依赖与模块**
   ```bash
   pip install -r requirements.txt
   pip install -e . # 开发者模式
   ```

4. **查看可用主题**
   ```bash
   remup --list-themes
   ```

5. **编译第一个文件**
   ```bash
   # 编译单个文件
   remup test.remup
   
   # 或者启动实时预览
   remup live test.remup
   ```
   **最便捷**：你也可以直接拖入remup_compile.py文件进行编译：
   ![演示gif](static/gifs/toss_compile.gif)

6. **查看结果**
   - 将生成的HTML文件拖入浏览器中欣赏成果
   - 在浏览器页面右上角测试主题切换功能

## 💡 使用方式

### 1. 命令行编译（推荐）

RemUp v3.1 引入了子命令系统，提供更清晰的命令行接口。

#### 基础编译命令
```bash
# 编译单个文件
remup build input.remup

# 编译整个目录
remup build ./notes -d

# 递归编译子目录
remup build ./notes -d -r

# 指定输出路径和主题
remup build input.remup -o output.html -t DarkTheme

# 自定义页面标题
remup build input.remup --title "我的学习笔记"
```

#### 实时预览命令
```bash
# 启动实时预览服务器
remup live input.remup

# 指定端口和主机
remup live input.remup -p 8080 --host 0.0.0.0

# 不自动打开浏览器
remup live input.remup --no-browser

# 使用特定主题
remup live input.remup -t CompactStyle
```

#### 信息查询命令
```bash
# 列出所有可用主题
remup --list-themes

# 显示版本信息
remup --version
```

### 2. 主题系统

RemUp 支持多主题系统，编译时会自动将CSS文件复制到输出目录的 `static/css/` 子目录。

#### 可用主题
- **RemStyle** - 默认主题，平衡的可读性和美观性
- **CompactStyle** - 紧凑主题，适合内容密集的笔记
- **DarkTheme** - 暗色主题，减少眼部疲劳

#### 主题切换
在生成的HTML页面中，可以通过页面顶部的主题选择器实时切换主题，选择会自动保存到本地存储。

### 3. 静态资源管理

编译器会自动处理静态CSS文件：
- ✅ 自动检测项目根目录的 `static/css/` 文件夹
- ✅ 编译时复制所有CSS主题文件到输出目录
- ✅ 保持主题文件的完整性和版本一致性
- ✅ 支持离线使用，所有资源本地化

### 4. 高级选项

```bash
# 禁用静态资源复制（高级用户）
remup build input.remup --no-static

# 批量编译目录
remup build ./my_notes -d -r -t DarkTheme

# 生产环境编译
remup build input.remup -o dist/production.html --title "正式文档"
```

## 📝 语法指南

### 基础语法速查表

| 语法元素 | 格式 | 示例 | 说明 |
|---------|------|------|------|
| **主卡开始** | `<+主题` | `<+RemUp` | 定义新卡片 |
| **主卡结束** | `/+>` | `/+>` | 结束当前卡片 |
| **标签** | `(符号: 内容)` | `(!: 重要)` | 右上角标签 |
| **链接标签** | `(符号: #目标)` | `(!: #必看)` | 可跳转标签 |
| **区域划分** | `---区域名` | `---语法` | 内容分区 |
| **行内解释** | `>>解释` | `>>编程基础` | 灰色解释文字 |
| **注卡批注** | `` `内容`[批注] `` | `` `变量`[存储数据] `` | 交互式批注 |
| **文本加粗** | `**文本**` | `**重要内容**` | 加粗显示 |
| **文本斜体** | `*文本*` | `*强调内容*` | 斜体显示 |
| **文本高亮** | `==文本==` | `==关键点==` | 高亮显示 |
| **文本放大** | `+文本+` | `+重点+` | 放大1.2倍 |
| **文本更大** | `++文本++` | `++标题++` | 放大1.5倍 |

### 完整示例

```remup
--<欢迎入门>--
<+RemUp
(i: 基础介绍)
(!: #必看)

---RemUp是什么
**RemUp**是一个用于**辅助学习记忆**的**专注于电脑笔记**领域的**轻量级标记语言**。你可以简单地认为这是一个专业化的MarkDown，这与MarkDown的原理是差不多的，就是专业化更高，并且相应的支持还在构建中。

---如何入门
1. 首先，你需要按照本教程把RemUp的环境搭建好，然后将这个文件编译成html文件。
2. 使用以下命令编译：`remup build example.remup -t DarkTheme`

---新特性
RemUp v3.1 引入了以下新功能：
- **多主题支持**：使用 `-t` 参数切换主题
- **实时预览**：使用 `remup live` 命令启动实时预览
- **静态资源管理**：自动处理CSS文件
- **改进的命令行接口**：子命令系统更加直观

>>更多功能正在开发中...
/+>
```

## 📁 项目结构

```
PPL_Project-RemUp/                 # 项目根目录
├── remup/                         # 编译器核心包
│   ├── __init__.py                # 初始化文件
│   ├── ast_nodes.py               # 抽象语法树定义
│   ├── lexer.py                   # 词法解析器
│   ├── parser.py                  # 语法解析器
│   ├── html_generator.py          # HTML生成器
│   ├── compiler.py                # 编译器核心
│   ├── live_preview.py            # 实时预览功能
│   └── main.py                    # 命令行主入口
├── static/                        # 静态资源
│   ├── Logo.svg                   # RemUp的Logo
│   └── css/                       # 主题文件目录
│       ├── RemStyle.css           # 默认样式文件
│       ├── CompactStyle.css       # 紧凑样式文件
│       └── DarkTheme.css          # 暗色主题文件
├── examples/                      # 示例文件目录
│   ├── test.remup                 # 测试文件
│   └── vocabulary.remup           # 词汇表示例
├── requirements.txt               # Python依赖配置
├── setup.py                       # 包安装配置
├── README.md                      # 项目说明文档
└── LICENSE                    # 许可证文件（作业中不可见）
```

## 🛠️ 开发指南

### 架构概述

RemUp编译器采用标准的编译器架构：

1. **词法分析** (`lexer.py`) - 将源代码转换为token流
2. **语法分析** (`parser.py`) - 构建抽象语法树(AST)
3. **代码生成** (`html_generator.py`) - 将AST转换为HTML
4. **编译器协调** (`compiler.py`) - 协调整个编译流程

### 扩展开发

欢迎扩展RemUp的功能：

- **新的语法元素** - 在lexer和parser中添加支持
- **输出格式** - 实现新的生成器（如PDF、Anki等）
- **主题系统** - 创建可切换的CSS主题
- **实时预览** - 完善live_preview功能

## 🤝 贡献指南

我们欢迎各种形式的贡献！在贡献时，请遵循技术文档写作的黄金法则：清晰、准确、简洁。

### 贡献方式

1. **Fork** 本仓库
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **开启 Pull Request**

### 文档标准

在提交文档更改时，请确保：
- 使用清晰的标题层级结构
- 保持段落简洁（最佳长度小于等于四行）
- 使用主动语态和肯定句
- 为代码示例提供适当的注释和说明

## ❓ 常见问题

### Q: 如何查看可用的主题列表？
A: 使用 `remup --list-themes` 命令查看所有可用主题。

### Q: 编译时出现主题不存在的错误怎么办？
A: 确保项目根目录下的 `static/css/` 目录中存在对应的CSS文件。可以使用默认主题 `RemStyle` 进行测试。

### Q: 实时预览功能如何工作？
A: 使用 `remup live input.remup` 启动实时预览服务器，该命令会监控文件变化并自动重新编译，但是目前预览需要手动刷新浏览器。

### Q: 如何自定义主题？
A: 在 `static/css/` 目录下创建新的CSS文件，然后在编译时使用 `-t` 参数指定主题名。

### Q: 静态资源复制失败怎么办？
A: 检查项目根目录结构，确保存在 `static/css/` 目录。可以使用 `--no-static` 参数暂时禁用静态资源复制。

### Q: 如何为现有项目添加RemUp支持？
A: 在项目根目录创建 `static/css/` 目录并添加主题文件，然后使用RemUp编译器处理你的文档文件。

## 📄 许可证

本项目基于 MIT 许可证 - 查看 LICENSE 文件了解详情。

## 📞 联系方式

- **作者**: MingShuo-S
- **项目链接**: https://github.com/MingShuo-S/PPL_Project-RemUp
- **问题反馈**: 欢迎通过GitHub Issues提交问题和建议

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！特别感谢：
- 开源社区提供的宝贵工具和库
- 所有测试人员和bug报告者
- 提供宝贵反馈的用户

---

<div align="center">

如果这个项目对你有帮助，请考虑给它一个 ⭐️！

**开始你的记忆升级之旅吧！** 🚀

</div>

## 🔄 更新日志

### v3.1 (2026-01-25)
- **新增**: 多主题系统支持
- **新增**: 静态资源自动管理
- **新增**: 子命令命令行接口
- **优化**: 改进的错误处理和用户反馈
- **增强**: 实时预览功能稳定性


*持续更新中...*