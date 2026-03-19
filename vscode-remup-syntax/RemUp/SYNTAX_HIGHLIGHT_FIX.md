# 语法高亮修复说明

## 🔧 修复内容

本次更新修复了 Markdown 语法符号和行内解释符号的高亮问题。

### 修复的问题

#### 1. Markdown 标题符号高亮 ✅
**之前**: `#`, `##`, `###`, `####` 显示为白色  
**现在**: 使用 `punctuation.definition.heading.remup` 作用域，会有颜色区分

**修复的作用域名称**:
- `#` → `markup.heading.1.remup` + `punctuation.definition.heading.remup`
- `##` → `markup.heading.2.remup` + `punctuation.definition.heading.remup`
- `###` → `markup.heading.3.remup` + `punctuation.definition.heading.remup`
- `####` → `markup.heading.4.remup` + `punctuation.definition.heading.remup`

#### 2. 行内解释符号高亮 ✅
**之前**: `^` 和 `>>` 显示为白色  
**现在**: 使用 `punctuation.definition.explanation.remup` 作用域

**修复的作用域名称**:
- `^` → `punctuation.definition.explanation.remup`
- `>>` → `punctuation.definition.explanation.remup`

#### 3. 标签符号高亮优化 ✅
**优化**: 括号和分隔符也单独标记

**修复的作用域名称**:
- `(` → `punctuation.definition.label.begin.remup`
- `:` 或 `：` → `punctuation.definition.label.separator.remup`
- `)` → 自动闭合（由 VSCode 处理）

#### 4. 注卡符号高亮优化 ✅
**优化**: Markdown 注卡的方括号和分隔符也单独标记

**修复的作用域名称**:
- `[` → `punctuation.definition.vibe.begin.md.remup`
- `|` → `punctuation.definition.vibe.separator.md.remup`
- `]` → `punctuation.definition.vibe.end.md.remup`

---

## 🧪 测试步骤

### 步骤 1: 重新加载 VSCode 扩展

1. 按 `Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (macOS)
2. 输入 "Reload Window" 并回车

或者：

1. 按 `Ctrl+Shift+P`
2. 输入 "Developer: Reload Extensions" 并回车

### 步骤 2: 打开测试文件

打开 `test-syntax.remup` 文件或创建新的 `.remup` 文件

### 步骤 3: 验证高亮效果

#### 测试 Markdown 标题

```remup
# 一级标题 - 应该有不同的颜色
## 二级标题 - 应该有不同的颜色
### 三级标题 - 应该有不同的颜色
#### 四级标题 - 应该有不同的颜色
```

**检查项**:
- [ ] `#` 符号本身有颜色（不是白色）
- [ ] `##` 符号本身有颜色
- [ ] `###` 符号本身有颜色
- [ ] `####` 符号本身有颜色
- [ ] 标题文字也有不同的颜色

#### 测试行内解释

```remup
这是概念 ^简短解释
这是另一个 >>详细解释
```

**检查项**:
- [ ] `^` 符号本身有颜色
- [ ] `>>` 符号本身有颜色
- [ ] 解释文字是灰色或其他颜色

#### 测试标签

```remup
(!: 重要内容)
(>: #参考链接)
(*: ⭐⭐⭐)
```

**检查项**:
- [ ] `(` 括号有颜色
- [ ] `!`, `>`, `*` 等符号有明显的颜色
- [ ] `:` 或 `：` 分隔符有颜色
- [ ] 标签内容有不同的颜色

#### 测试注卡

```remup
传统注卡：`术语`[批注说明]
Markdown 注卡：[内容 | 批注]
```

**检查项**:
- [ ] `` ` `` 反引号有颜色
- [ ] `[` 和 `]` 有颜色
- [ ] `|` 分隔符有颜色（Markdown 风格）
- [ ] 内容和批注有不同的颜色

---

## 🎨 主题兼容性

### 默认主题效果

不同的 VSCode 主题会对这些作用域应用不同的颜色。以下是一些常见主题的效果：

#### Dark+ (默认深色主题)
- `markup.heading.*` - 通常是蓝色或紫色
- `punctuation.definition.*` - 通常是青色或浅蓝色
- `string.unquoted.*` - 通常是橙色或黄色
- `entity.name.*` - 通常是绿色或黄色

#### Light+ (默认浅色主题)
- `markup.heading.*` - 通常是深蓝色或紫色
- `punctuation.definition.*` - 通常是深青色
- `string.unquoted.*` - 通常是棕色或橙色

### 自定义颜色（可选）

如果对当前颜色不满意，可以在 `settings.json` 中自定义：

```json
{
    "editor.tokenCustomizations": {
        "[你的主题名称]": {
            "punctuation.definition.heading.remup": "#FF0000",
            "punctuation.definition.explanation.remup": "#00FF00",
            "punctuation.definition.label.begin.remup": "#0000FF",
            "punctuation.definition.vibe.begin.md.remup": "#FF00FF"
        }
    }
}
```

---

## 🐛 故障排除

### 问题 1: 仍然显示白色

**可能原因**:
1. 扩展未重新加载
2. 缓存问题

**解决方法**:
1. 完全重启 VSCode
2. 清除 VSCode 缓存：删除 `%APPDATA%\Code\Cache` (Windows) 或 `~/Library/Application Support/Code/Cache` (macOS)

### 问题 2: 某些语法不高亮

**可能原因**:
1. 文件类型不正确
2. 语言模式未设置

**解决方法**:
1. 确认文件扩展名为 `.remup` 或 `.ru`
2. 点击右下角状态栏的语言模式，选择 "RemUp"

### 问题 3: 颜色不符合预期

**说明**: 这是正常的，因为不同的主题会使用不同的配色方案。

**解决方法**:
- 可以切换到其他主题查看效果
- 或者使用上面的自定义颜色配置

---

## 📊 作用域映射表

| 语法元素 | 完整作用域 | 标点作用域 |
|---------|-----------|-----------|
| `#` 归档 | `markup.heading.1.remup` | `punctuation.definition.heading.remup` |
| `##` 卡片 | `markup.heading.2.remup` | `punctuation.definition.heading.remup` |
| `###` 区域 | `markup.heading.3.remup` | `punctuation.definition.heading.remup` |
| `####` 次级 | `markup.heading.4.remup` | `punctuation.definition.heading.remup` |
| `^` 解释 | `meta.inline-explanation.md.remup` | `punctuation.definition.explanation.remup` |
| `>>` 解释 | `meta.inline-explanation.traditional.remup` | `punctuation.definition.explanation.remup` |
| `(` 标签 | `meta.label.remup` | `punctuation.definition.label.begin.remup` |
| `:` 分隔 | `meta.label.remup` | `punctuation.definition.label.separator.remup` |
| `[` 注卡 | `meta.vibe-card.md.remup` | `punctuation.definition.vibe.begin.md.remup` |
| `\|` 分隔 | `meta.vibe-card.md.remup` | `punctuation.definition.vibe.separator.md.remup` |
| `]` 注卡 | `meta.vibe-card.md.remup` | `punctuation.definition.vibe.end.md.remup` |

---

## ✅ 验证清单

完成以下检查确保所有修复都生效：

### Markdown 标题
- [ ] `#` 符号有颜色
- [ ] `##` 符号有颜色
- [ ] `###` 符号有颜色
- [ ] `####` 符号有颜色
- [ ] 不同级别的标题颜色有区分

### 行内解释
- [ ] `^` 符号有颜色
- [ ] `>>` 符号有颜色
- [ ] 解释文字颜色正确

### 标签系统
- [ ] `(` 左括号有颜色
- [ ] 标签符号（!, >, * 等）有颜色
- [ ] 分隔符（: 或 ：）有颜色
- [ ] 标签内容颜色正确

### 注卡系统
- [ ] `` ` `` 反引号有颜色
- [ ] `[` 和 `]` 有颜色
- [ ] `|` 分隔符有颜色
- [ ] 内容和批注颜色正确

### 整体效果
- [ ] 所有语法元素都有合适的高亮
- [ ] 没有纯白色的语法符号
- [ ] 颜色搭配协调，易于阅读

---

## 🎉 完成标志

如果以上所有检查项都打勾，说明修复成功！🎊

如有问题，请查看 DEVELOPMENT.md 中的调试指南或提交 Issue。

---

<div align="center">

**享受完美的语法高亮体验！** ✨

</div>