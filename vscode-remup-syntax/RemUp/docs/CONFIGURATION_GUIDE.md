# RemUp VSCode 扩展配置指南

## 🎉 新功能：一体化配置

从 v1.1.0 开始，RemUp VSCode 扩展不仅提供语法高亮，还内置了优化的编辑设置，让你无需手动配置即可获得最佳体验！

## ✨ 核心特性

### 1. 语法高亮 ✅
- 支持传统语法和 Markdown 风格语法
- 标签、注卡、代码块等元素智能着色
- 完整的折叠和自动闭合功能

### 2. 自动换行 ✅（新增）
- 默认启用，类似 Markdown 的舒适体验
- 可自定义换行列宽
- 保持缩进对齐

### 3. 列参考线 ✅（新增）
- 80 列和 120 列参考线
- 帮助控制行长，提升可读性
- 可选开启/关闭

### 4. 智能编辑 ✅
- 丰富的代码片段
- 自动括号闭合
- 快速建议触发

## 🚀 快速开始

### 安装扩展

1. 打开 VSCode
2. 按 `Ctrl+Shift+X` 打开扩展面板
3. 搜索 "RemUp"
4. 点击安装

### 立即使用

安装完成后，打开任意 `.remup` 或 `.ru` 文件即可享受：
- ✅ 自动语法高亮
- ✅ 自动换行
- ✅ 列参考线
- ✅ 智能提示

**无需任何额外配置！**

## ⚙️ 自定义配置

如需调整默认行为，可通过以下方式：

### 方式一：设置界面

1. 按 `Ctrl+,` 打开设置
2. 搜索 "RemUp"
3. 调整以下选项：

   - ✓ `Remup: Enable Auto Wrap` - 启用自动换行
   - ✓ `Remup: Word Wrap Column` - 换行列宽
   - ✓ `Remup: Enable Rulers` - 显示列参考线
   - ✓ `Remup: Rulers Columns` - 参考线位置

### 方式二：settings.json

```json
{
    // RemUp 扩展配置
    "remup.enableAutoWrap": true,        // 启用自动换行
    "remup.wordWrapColumn": 120,         // 换行列宽
    "remup.enableRulers": true,          // 显示列参考线
    "remup.rulersColumns": [80, 120]     // 参考线位置
}
```

### 禁用某项功能

如果只想保留语法高亮，不想要自动换行：

```json
{
    "remup.enableAutoWrap": false,
    "remup.enableRulers": false
}
```

## 📊 配置效果对比

### 自动换行

#### 关闭 ❌
```
这是一行非常长的文本内容，会一直向右延伸超出屏幕范围，需要拖动横向滚动条才能看到完整内容...
```

#### 开启 ✅
```
这是一行非常长的文本内容，会在
编辑器边界处自动换行，无需横向
滚动即可看到完整内容。
```

### 列参考线

#### 关闭 ❌
无法直观判断行长是否合适

#### 开启 ✅
```
这是一行内容，长度适中 |
这是另一行，超过了 80 列参考线 |
```

## 💡 推荐配置组合

### 方案一：标准配置（推荐新手）
```json
{
    "remup.enableAutoWrap": true,
    "remup.wordWrapColumn": 120,
    "remup.enableRulers": true,
    "remup.rulersColumns": [80, 120]
}
```

### 方案二：极简配置（专注写作）
```json
{
    "remup.enableAutoWrap": true,
    "remup.wordWrapColumn": 100,
    "remup.enableRulers": false
}
```

### 方案三：专业配置（精确控制）
```json
{
    "remup.enableAutoWrap": true,
    "remup.wordWrapColumn": 80,
    "remup.enableRulers": true,
    "remup.rulersColumns": [60, 80, 100],
    "editor.renderWhitespace": "selection",
    "editor.minimap.enabled": true
}
```

### 方案四：禁用所有优化（仅语法高亮）
```json
{
    "remup.enableAutoWrap": false,
    "remup.enableRulers": false
}
```

## 🔧 高级技巧

### 1. 临时切换自动换行
按 `Alt+Z` 可以快速开启/关闭当前文件的换行功能（不保存设置）。

### 2. 为不同项目设置不同配置
在项目根目录创建 `.vscode/settings.json`：

```json
{
    "remup.enableAutoWrap": true,
    "remup.wordWrapColumn": 90
}
```

这样每个项目可以有独立的配置。

### 3. 配合其他语言设置
RemUp 的设置不会影响其他语言，你可以为不同语言分别配置：

```json
{
    "[remup]": {
        "editor.wordWrap": "on",
        "editor.rulers": [80, 120]
    },
    "[markdown]": {
        "editor.wordWrap": "on"
    },
    "[javascript]": {
        "editor.rulers": [100]
    }
}
```

## 🎨 视觉优化建议

除了 RemUp 扩展自带功能，还可以考虑：

### 1. 使用连字字体
```json
{
    "editor.fontFamily": "'Fira Code', 'Cascadia Code', Consolas, monospace",
    "editor.fontLigatures": true
}
```

### 2. 调整行高和字号
```json
{
    "editor.fontSize": 14,
    "editor.lineHeight": 1.6
}
```

### 3. 启用小地图
```json
{
    "editor.minimap.enabled": true,
    "editor.minimap.maxColumn": 80
}
```

### 4. 面包屑导航
```json
{
    "editor.breadcrumbs.enabled": true
}
```

## 📝 常见问题

### Q: 安装扩展后为什么没有自动换行？
A: 
1. 检查文件扩展名是否为 `.remup` 或 `.ru`
2. 确认右下角语言模式为 "RemUp"
3. 检查设置中 `remup.enableAutoWrap` 是否为 `true`
4. 重启 VSCode 试试

### Q: 能否只启用语法高亮，不要自动换行？
A: 可以！在设置中将 `remup.enableAutoWrap` 设为 `false` 即可。

### Q: 列参考线太明显了怎么办？
A: 可以通过颜色设置调整参考线透明度：

```json
{
    "workbench.colorCustomizations": {
        "editorRuler.foreground": "#33333333"
    }
}
```

### Q: 如何在不同项目使用不同配置？
A: 在每个项目的 `.vscode/settings.json` 中分别设置即可。

### Q: 扩展设置会影响其他语言吗？
A: 不会！RemUp 的配置只对 `.remup` 和 `.ru` 文件生效。

## 🆚 版本对比

### v1.0.0 vs v1.1.0

| 特性 | v1.0.0 | v1.1.0 |
|------|--------|--------|
| 语法高亮 | ✅ | ✅ |
| 代码片段 | ✅ | ✅ |
| 自动闭合 | ✅ | ✅ |
| 自动换行 | ❌ | ✅ 默认启用 |
| 列参考线 | ❌ | ✅ 可配置 |
| 设置界面 | ❌ | ✅ 可视化配置 |
| 智能激活 | ❌ | ✅ 按需加载 |

## 📚 相关资源

- [RemUp 官方文档](https://github.com/MingShuo-S/PPL_Project-RemUp)
- [语法速查表](./QUICK_REFERENCE_CARD.md)
- [开发指南](./DEVELOPMENT.md)
- [更新日志](./CHANGELOG.md)

## 🤝 反馈与建议

如有任何问题或建议，欢迎通过以下方式联系我们：

- **GitHub Issues**: https://github.com/MingShuo-S/PPL_Project-RemUp/issues
- **邮箱**: 2954809209@qq.com

---

<div align="center">

**享受一站式 RemUp 编辑体验！** 🚀

安装一个扩展，获得完整功能支持

</div>