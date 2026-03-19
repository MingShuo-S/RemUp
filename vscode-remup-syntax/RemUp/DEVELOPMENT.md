# RemUp VSCode 扩展开发和测试指南

## 📦 本地安装测试

### 方法一：直接加载未打包的扩展（推荐用于开发）

1. **打开 VSCode**

2. **进入扩展面板**
   - Windows/Linux: `Ctrl+Shift+X`
   - macOS: `Cmd+Shift+X`

3. **点击右上角菜单** (三个点 ...)

4. **选择 "从 VSIX 安装..."** 
   - 或者选择 "从目录加载未打包的扩展"

5. **选择扩展目录**
   ```
   c:\Users\29548\Desktop\Sunshine\RemUp\vscode-remup-syntax\RemUp
   ```

6. **重新加载 VSCode**
   - 按 `Ctrl+Shift+P` (或 `Cmd+Shift+P`)
   - 输入 "Reload Window" 并回车

### 方法二：打包成 VSIX 安装

1. **安装 vsce 工具**
   ```bash
   npm install -g vsce
   ```

2. **打包扩展**
   ```bash
   cd c:\Users\29548\Desktop\Sunshine\RemUp\vscode-remup-syntax\RemUp
   vsce package
   ```

3. **安装生成的 VSIX 文件**
   - 会生成类似 `RemUp-1.0.0.vsix` 的文件
   - 双击文件或通过 VSCode 的 "从 VSIX 安装" 功能安装

## 🧪 测试语法高亮

### 步骤 1：打开测试文件

```bash
# 在 VSCode 中打开测试文件
c:\Users\29548\Desktop\Sunshine\RemUp\vscode-remup-syntax\RemUp\test-syntax.remup
```

### 步骤 2：验证语法高亮

检查以下元素是否正确高亮：

#### Markdown 风格语法
- [ ] `# 标题` - 归档（一级标题，醒目颜色）
- [ ] `## 卡片` - 卡片标题（二级颜色）
- [ ] `### 区域` - 区域标题（三级颜色）
- [ ] `#### 次级卡片` - 次级卡片标题

#### 传统语法
- [ ] `--<归档>--` - 传统归档标记
- [ ] `<+卡片` ... `/+>` - 传统卡片结构
- [ ] `---区域` - 传统区域标记

#### 标签系统
- [ ] `(!: 内容)` - 重要标签（通常红色）
- [ ] `(>: #目标)` - 参考链接（通常蓝色）
- [ ] `(*: ⭐⭐⭐)` - 评级标签
- [ ] `(备注：说明)` - 普通备注（灰色）

#### 注卡系统
- [ ] `` `内容`[批注] `` - 传统注卡
- [ ] `[内容 | 批注]` - Markdown 注卡

#### 行内解释
- [ ] `>>解释文字` - 传统行内解释
- [ ] `^解释文字` - Markdown 行内解释

#### 其他元素
- [ ] 代码块（```language ... ```）
- [ ] 有序列表（1. 2. 3.）
- [ ] 无序列表（- 项目）
- [ ] 粗体文本（**文字**）

### 步骤 3：测试智能功能

#### 自动闭合测试
1. 输入 `<+` 应该自动添加 `/+>`
2. 输入 `` ` `` 应该自动配对
3. 输入 `(` 应该自动添加 `)`
4. 输入 `\`\`\`` 应该自动添加结束的代码块标记

#### 折叠功能测试
1. 点击归档旁边的折叠箭头，应该能折叠整个归档
2. 点击卡片旁边的折叠箭头，应该能折叠卡片
3. 点击区域旁边的折叠箭头，应该能折叠区域

#### 代码片段测试
1. 在新文件中输入 `##card` 然后按 `Tab`
2. 输入 `vibe` 然后按 `Tab`
3. 输入 `!label` 然后按 `Tab`
4. 输入 `fullcard` 然后按 `Tab`

## 🐛 调试指南

### 如果语法高亮不工作

#### 检查点 1：文件扩展名
确保文件扩展名为 `.remup` 或 `.ru`

#### 检查点 2：语言模式
1. 查看 VSCode 右下角状态栏
2. 应该显示 "RemUp"
3. 如果不是，点击它并选择 "RemUp"

#### 检查点 3：语法定义文件
打开开发者工具检查：
1. `Help` → `Toggle Developer Tools`
2. 查看 Console 是否有错误信息

### 如果代码片段不显示

#### 手动触发
按 `Ctrl+Space` (Windows/Linux) 或 `Cmd+Space` (macOS)

#### 检查文件类型
确保在 `.remup` 或 `.ru` 文件中

#### 检查冲突扩展
禁用其他可能冲突的 Markdown 扩展

### 如果自动闭合不工作

#### 检查 VSCode 设置
```json
{
    "editor.autoClosingBrackets": true,
    "editor.autoClosingQuotes": true,
    "editor.autoSurround": "languageDefined"
}
```

## 📝 修改语法定义

### 语法定义文件位置
```
c:\Users\29548\Desktop\Sunshine\RemUp\vscode-remup-syntax\RemUp\syntaxes\remup.tmLanguage.json
```

### TextMate 语法格式

基本结构：
```json
{
  "name": "scope.name.here",
  "match": "regex-pattern",
  "captures": {
    "1": { "name": "specific.scope.1" },
    "2": { "name": "specific.scope.2" }
  }
}
```

### 常用正则表达式

- 匹配行首：`^`
- 匹配行尾：`$`
- 匹配空白：`\\s*`
- 匹配任意字符：`.`
- 匹配分组：`(...)`
- 转义特殊字符：`\\`, `\\[`, `\\]` 等

### 作用域命名约定

- `entity.name.*` - 名称定义
- `keyword.control.*` - 控制关键字
- `string.quoted.*` - 引用字符串
- `comment.line.*` - 注释
- `markup.heading.*` - 标题
- `markup.list.*` - 列表
- `markup.bold` - 粗体

## 🎨 自定义主题颜色

### 在 settings.json 中添加

```json
{
    "editor.tokenCustomizations": {
        "light": {
            "entity.name.section.archive.md.remup": "#FF0000",
            "entity.name.title.card.md.remup": "#00FF00",
            "entity.name.section.region.md.remup": "#0000FF"
        },
        "dark": {
            "entity.name.section.archive.md.remup": "#FF8800",
            "entity.name.title.card.md.remup": "#88FF00",
            "entity.name.section.region.md.remup": "#0088FF"
        }
    }
}
```

## 📤 发布扩展

### 准备工作

1. **创建 Publisher**
   ```bash
   vsce login <publisher-name>
   ```

2. **更新 package.json**
   - 版本号
   - 发布日期
   - 更新日志

### 发布

```bash
vsce publish
```

或指定版本：
```bash
vsce publish 1.0.1
```

## 🔗 有用链接

- [TextMate 语法指南](https://macromates.com/manual/en/language_grammars)
- [VSCode 扩展指南](https://code.visualstudio.com/api)
- [RemUp 官方文档](https://github.com/MingShuo-S/PPL_Project-RemUp)

## ❓ 常见问题

**Q: 修改后如何重新加载扩展？**
A: 按 `Ctrl+Shift+P`，输入 "Reload Window"

**Q: 如何查看扩展的激活事件？**
A: 打开输出面板，选择 "Extension Host"

**Q: 语法高亮混乱怎么办？**
A: 检查正则表达式是否有重叠或优先级问题

---

祝开发和测试顺利！🚀