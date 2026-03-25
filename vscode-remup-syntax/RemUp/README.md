<div align="center">

# RemUp - VSCode 完整支持扩展

**为 RemUp 标记语言提供一站式解决方案**  
语法高亮 ✦ 自动换行 ✦ 智能编辑 ✦ 可视化配置

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

## 📖 简介

RemUp VSCode 扩展是一个功能完整的语言支持插件，不仅提供语法高亮，还内置了优化的编辑设置，让你无需手动配置即可获得最佳编辑体验。

### ✨ 核心理念

**安装一个扩展 = 获得完整功能**

- ✅ 语法高亮
- ✅ 自动换行
- ✅ 智能提示
- ✅ 代码片段
- ✅ 可视化配置

---

## 🎯 快速开始

### 3 步上手（30 秒）

1. **安装扩展** - VSCode 扩展面板搜索 "RemUp"
2. **创建文件** - 新建 `.remup` 或 `.ru` 文件
3. **开始写作** - 享受自动换行和语法高亮！

**无需任何配置！** ✨

---

## 🔥 核心功能

### 1. 双语法高亮支持

#### Markdown 风格（推荐新手）
```remup
# 归档名称

## 卡片主题 (!: 重点)

### 区域名
内容 ^解释

/+>
```

#### 传统风格
```remup
--<归档名称>--

<+卡片主题
(!: 重点) (>: #参考)

---区域名
`术语`[批注] >>解释

/+>
```

### 2. 自动换行（类似 Markdown）

长文本自动在编辑器边界处折行，无需横向滚动。

**效果对比：**

| 关闭 ❌ | 开启 ✅ |
|--------|--------|
| 横向滚动阅读困难 | 自动折行舒适阅读 |

### 3. 标签系统

不同语义的标签使用不同颜色和图标：

- `(!: 内容)` - 🔴 重要/警告（红色）
- `(>: #目标)` - 🔗 引用/跳转（蓝色）
- `(*: ⭐⭐⭐)` - ⭐ 等级/评分（星级）
- `(备注：说明)` - ℹ️ 说明提示（灰色）

### 5. 交互式元素

#### 注卡批注
```remup
`变量`[存储数据的容器] ^编程概念
```

#### 内联解释
```remup
def greet(name): ^定义函数
    return f"Hello, {name}"
```

### 5. 智能编辑功能

- 🔄 **自动闭合** - 输入 `<+` 自动添加 `/+>`
- 📦 **代码块闭合** - 输入 ``` 自动添加结束标记
- 🗂️ **语法折叠** - 按层级折叠卡片/区域
- ⚡ **代码片段** - 50+ 个快捷模板

### 6. 可视化配置

通过 VSCode 设置界面即可调整所有选项：

1. 按 `Ctrl+,` 打开设置
2. 搜索 "RemUp"
3. 勾选/取消选项

**无需手动编辑配置文件！**

---

## ⚙️ 配置选项

### 默认配置（开箱即用）

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `remup.enableAutoWrap` | `true` | 启用自动换行 |
| `remup.wordWrapColumn` | `120` | 换行列宽 |

### 自定义配置

如需调整，可在 `settings.json` 中添加：

```json
{
    "remup.enableAutoWrap": true,
    "remup.wordWrapColumn": 120
}
```

### 禁用自动换行

只想保留语法高亮：

```json
{
    "remup.enableAutoWrap": false
}
```

---

## 🎮 代码片段速查

输入前缀后按 `Tab` 键：

| 前缀 | 生成内容 |
|------|----------|
| `#archive` | `# 归档名称` |
| `##card` | `## 卡片主题` + 完整结构 |
| `###region` | `### 区域名` |
| `####subcard` | `#### 次级卡片` |
| `!label` | `(!: 内容)` |
| `>label` | `(>: #目标)` |
| `*label` | `(*: ⭐⭐⭐)` |
| `vibe` | `` `内容`[批注] `` |
| `[vibe` | `[内容 \| 批注]` |
| `fullcard` | 完整卡片模板 |
| `note` | 学习笔记模板 |

---

## 📝 使用示例

### 简单笔记

```remup
# Python 学习笔记

## 基础语法 (!: 重点)

### 变量
`变量`[存储数据的容器] ^编程概念

用于存储数据的基本单元。

### 函数
def greet(name): ^定义函数
    return f"Hello, {name}"

函数的基本语法结构。

/+>
```

### 知识卡片

```remup
# 设计模式

## 单例模式 (*: ⭐⭐⭐⭐⭐)

### 概念
确保一个类只有一个实例 (>: #工厂模式)

### 实现
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 应用场景
- 数据库连接池
- 配置文件管理
- 日志记录器

(!: 注意线程安全问题)

/+>
```

---

## 🔧 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Alt+Z` | 切换自动换行 |
| `Ctrl+Space` | 触发代码片段建议 |
| `Ctrl+K Ctrl+F` | 折叠当前卡片/区域 |
| `Ctrl+K Ctrl+J` | 展开所有折叠 |

---

## 📚 文档导航

- 🚀 **[docs/QUICK_START.md](./docs/QUICK_START.md)** - 30 秒快速上手
- 📋 **[QUICK_REFERENCE_CARD.md](./QUICK_REFERENCE_CARD.md)** - 语法速查表
- 📖 **[DEVELOPMENT.md](./DEVELOPMENT.md)** - 开发指南
- 🔄 **[CHANGELOG.md](./CHANGELOG.md)** - 更新日志
- 🧪 **[test-extension.remup](./test-extension.remup)** - 功能测试文件

**历史文档**: 详见 [`docs/`](./docs/) 文件夹

---

## 🆚 版本对比

| 特性 | v1.0.0 | v1.1.0（当前） |
|------|--------|----------------|
| 语法高亮 | ✅ | ✅ |
| 代码片段 | ✅ | ✅ |
| 自动闭合 | ✅ | ✅ |
| **自动换行** | ❌ | ✅ **默认启用** |
| **设置界面** | ❌ | ✅ **可视化配置** |

---

## 💡 推荐配置

### 标准配置（推荐）
```json
{
    "remup.enableAutoWrap": true,
    "remup.wordWrapColumn": 120
}
```

### 仅语法高亮
```json
{
    "remup.enableAutoWrap": false
}
```

---

## 🤔 常见问题

### Q: 安装后为什么没有自动换行？

A: 
1. 检查文件扩展名是否为 `.remup` 或 `.ru`
2. 确认右下角语言模式为 "RemUp"
3. 重启 VSCode 试试

### Q: 如何禁用自动换行？

A: 
1. 按 `Ctrl+,` 打开设置
2. 搜索 "RemUp"
3. 取消勾选 "Enable Auto Wrap"

### Q: 会影响其他语言吗？

A: 不会！RemUp 的配置只对 `.remup` 和 `.ru` 文件生效。

### Q: 如何临时切换换行？

A: 按 `Alt+Z` 可以快速切换当前文件的自动换行。

---

## 🔗 相关资源

- **GitHub**: https://github.com/MingShuo-S/PPL_Project-RemUp
- **RemUp 编译器**: https://github.com/MingShuo-S/PPL_Project-RemUp/tree/main/RemUp_compiler
- **官方文档**: https://github.com/MingShuo-S/PPL_Project-RemUp/blob/main/README.md
- **问题反馈**: https://github.com/MingShuo-S/PPL_Project-RemUp/issues

---

## 🙏 致谢

感谢所有为 RemUp 项目做出贡献的开发者！

特别感谢提出宝贵建议的用户们！

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

<div align="center">

**享受一站式 RemUp 编辑体验！** 🚀

**安装一个扩展，获得完整功能支持**

如果这个扩展对你有帮助，请给个 ⭐️ 支持一下！

</div>