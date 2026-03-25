# RemUp VSCode 扩展 - 快速开始

## 🚀 30 秒上手

### 第 1 步：安装扩展（10 秒）

1. 打开 VSCode
2. 按 `Ctrl+Shift+X` 打开扩展面板
3. 搜索 "**RemUp**"
4. 点击 **安装**

### 第 2 步：创建文件（10 秒）

1. 新建文件，命名为 `test.remup`
2. 输入以下内容：

```remup
# 我的学习笔记

## RemUp 基础 (!: 重点)

### 什么是 RemUp？
RemUp 是一个轻量级标记语言，用于构建知识体系。

### 核心特性
- 主卡系统
- 注卡批注
- 智能归档

/+>
```

### 第 3 步：体验功能（10 秒）

观察以下自动启用的功能：

✅ **语法高亮** - 不同元素颜色区分  
✅ **自动换行** - 长文本自动折行  
✅ **列参考线** - 80/120 列竖线提示  
✅ **代码折叠** - 左侧可折叠卡片/区域  
✅ **智能提示** - 输入时自动建议  

**完成！无需任何配置！** ✨

---

## ⚙️ 自定义配置（可选）

如需调整默认设置：

### 方式一：设置界面

1. 按 `Ctrl+,` 打开设置
2. 搜索 "RemUp"
3. 调整选项

### 方式二：settings.json

```json
{
    "remup.enableAutoWrap": true,      // 启用自动换行
    "remup.wordWrapColumn": 120,       // 换行列宽
    "remup.enableRulers": true,        // 显示列参考线
    "remup.rulersColumns": [80, 120]   // 参考线位置
}
```

---

## 📝 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Alt+Z` | 切换自动换行 |
| `Ctrl+Space` | 触发代码片段建议 |
| `Ctrl+K Ctrl+F` | 折叠当前卡片 |
| `Ctrl+K Ctrl+J` | 展开所有折叠 |

---

## 🎯 代码片段速查

输入以下前缀后按 `Tab` 键：

| 前缀 | 生成内容 |
|------|----------|
| `#archive` | `# 归档名称` |
| `##card` | `## 卡片主题` + 结构 |
| `###region` | `### 区域名` |
| `!label` | `(!: 内容)` |
| `>label` | `(>: #目标)` |
| `vibe` | `` `内容`[批注] `` |

---

## 📚 下一步

- 📖 查看 [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md) 了解详细配置
- 🎮 查看 [QUICK_REFERENCE_CARD.md](./QUICK_REFERENCE_CARD.md) 获取语法速查
- 📝 打开 [test-extension.remup](./test-extension.remup) 测试所有功能

---

<div align="center">

**开始你的 RemUp 之旅吧！** 🎉

</div>