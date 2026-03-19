import re
from typing import List, Tuple, Optional

class Lexer:
    """
    词法分析器 - 支持传统语法和极简 Markdown 语法双模式
    """
    
    # 定义词法规则（正则表达式模式）- 新增极简语法支持
    PATTERNS = {
        # 传统语法
        'archive': re.compile(r'^\s*--<([^>]+)>--\s*$'),
        'card_start': re.compile(r'^\s*<\+([^/]+)\s*$'),
        'card_end': re.compile(r'^\s*/\+>\s*$'),
        'region': re.compile(r'^\s*---\s*([^\s].*?)\s*$'),
        # 极简语法（Markdown 风格）
        'archive_md': re.compile(r'^\s*#\s+([^#].*?)\s*$'),  # # 归档名
        'card_md': re.compile(r'^\s*##\s+(.+?)\s*$'),  # ## 卡片主题
        'region_md': re.compile(r'^\s*###\s+(.+?)\s*$'),  # ### 区域名
        'sub_card_md': re.compile(r'^\s*####\s+(.+?)\s*$'),  # #### 次级卡片（新增）
        
        # 标签和注卡
        'label': re.compile(r'\s*\(([^:：]+)[:：]\s*([^)]+)\)'),  # 传统：(!: 内容) 支持中英文冒号
        'vibe_card': re.compile(r'`([^`\n]+)`\[([^\]]*)\]'),  # 传统：`内容 `[批注]
        'vibe_card_md': re.compile(r'\[([^\[\]\|]+)\s*\|\s*([^\[\]]*)\]'),  # 极简：[内容 | 批注]
        
        'inline_explanation': re.compile(r'>>\s*([^\n]+?)\s*$'),  # 传统：>>解释
        'inline_explanation_md': re.compile(r'\^([^\n]+)'),  # 极简：^解释
        
        # 代码块和列表
        'code_block_start': re.compile(r'^\s*```\s*(\w*)\s*$'),
        'code_block_end': re.compile(r'^\s*```\s*$'),
        'ordered_list': re.compile(r'^\s*(\d+\.\s+.*)$'),
        'unordered_list': re.compile(r'^\s*(-\\s+.*)$'),
        'empty_line': re.compile(r'^\s*$')
    }
    
    def __init__(self):
        self.tokens = []
        self.current_line_num = 0
        self.in_code_block = False
        self.current_code_block_lang = ""
        self.current_code_block_content = []
    
    def tokenize(self, text: str) -> List[Tuple[str, str, int]]:
        """将输入文本分解为词法标记"""
        self.tokens = []
        self.current_line_num = 0
        self.in_code_block = False
        lines = text.split('\n')
        
        for line in lines:
            self.current_line_num += 1
            self._process_line(line)
        
        return self.tokens
    
    def _process_line(self, line: str):
        """处理单行文本 - 支持双语法"""
        # 处理代码块状态
        if self.in_code_block:
            if self.PATTERNS['code_block_end'].match(line):
                # 结束代码块
                if self.current_code_block_content:
                    code_content = '\n'.join(self.current_code_block_content)
                    self.tokens.append(('CODE_BLOCK_CONTENT', code_content, self.current_line_num - len(self.current_code_block_content)))
                
                self.tokens.append(('CODE_BLOCK_END', '', self.current_line_num))
                self.in_code_block = False
                self.current_code_block_content = []
            else:
                # 在代码块中，收集内容
                self.current_code_block_content.append(line)
            return
        
        # 检查空行
        if self.PATTERNS['empty_line'].match(line):
            self.tokens.append(('EMPTY_LINE', '', self.current_line_num))
            return
        
        # 检查代码块开始
        code_start_match = self.PATTERNS['code_block_start'].match(line)
        if code_start_match:
            self.tokens.append(('CODE_BLOCK_START', code_start_match.group(1), self.current_line_num))
            self.in_code_block = True
            self.current_code_block_lang = code_start_match.group(1)
            self.current_code_block_content = []
            return
        
        # 检查归档定义（优先匹配极简语法）
        archive_md_match = self.PATTERNS['archive_md'].match(line)
        if archive_md_match:
            self.tokens.append(('ARCHIVE', archive_md_match.group(1), self.current_line_num))
            return
        
        archive_match = self.PATTERNS['archive'].match(line)
        if archive_match:
            self.tokens.append(('ARCHIVE', archive_match.group(1), self.current_line_num))
            return
        
        # 检查卡片开始（优先匹配极简语法）
        card_md_match = self.PATTERNS['card_md'].match(line)
        if card_md_match:
            self.tokens.append(('CARD_START', card_md_match.group(1), self.current_line_num))
            return
        
        card_start_match = self.PATTERNS['card_start'].match(line)
        if card_start_match:
            self.tokens.append(('CARD_START', card_start_match.group(1), self.current_line_num))
            return
        
        # 检查卡片结束（传统语法）
        card_end_match = self.PATTERNS['card_end'].match(line)
        if card_end_match:
            self.tokens.append(('CARD_END', '', self.current_line_num))
            return
        
        # 检查次级卡片定义（极简语法，新增）
        sub_card_md_match = self.PATTERNS['sub_card_md'].match(line)
        if sub_card_md_match:
            self.tokens.append(('SUB_CARD', sub_card_md_match.group(1), self.current_line_num))
            return
        
        # 检查区域定义（优先匹配极简语法）
        region_md_match = self.PATTERNS['region_md'].match(line)
        if region_md_match:
            self.tokens.append(('REGION', region_md_match.group(1), self.current_line_num))
            return
        
        region_match = self.PATTERNS['region'].match(line)
        if region_match:
            self.tokens.append(('REGION', region_match.group(1), self.current_line_num))
            return
        
        # 处理行内元素
        self._process_inline_elements(line)
    
    def _process_inline_elements(self, line: str):
        """处理行内的各种元素 - 仅支持传统标签语法"""
        remaining = line.strip()
        
        # 循环处理一行中的多个标签
        while remaining:
            label_match = self.PATTERNS['label'].match(remaining)
            if label_match:
                symbol = label_match.group(1).strip()
                content = [c.strip() for c in label_match.group(2).split(',')]
                self.tokens.append(('LABEL', f"{symbol}:{','.join(content)}", self.current_line_num))
                # 移动到下一个标签
                remaining = remaining[label_match.end():].strip()
                continue
            
            # 如果没有匹配到标签，退出循环
            break
        
        # 处理剩余的普通行内容
        if remaining:
            self._process_line_content(remaining)

    def _process_line_content(self, content: str):
        """处理行内容中的各种行内元素 - 支持双语法"""
        remaining = content.strip()
        text = ''
        explanation = ''
        while remaining:
            # 1. 检查传统注卡 `内容 `[批注]
            vibe_card_match = self.PATTERNS['vibe_card'].search(remaining)
            if vibe_card_match:
                before_text = remaining[:vibe_card_match.start()].strip()
                card_content = vibe_card_match.group(1)
                annotation = vibe_card_match.group(2)
                remaining = remaining[vibe_card_match.end():].strip()
                text += before_text + ' ' + f'__{card_content}__' + ' '
                self.tokens.append(('VIBE_CARD', f"{card_content}[{annotation}]", self.current_line_num))
                continue
            
            # 2. 检查极简注卡 [内容 | 批注]
            vibe_card_md_match = self.PATTERNS['vibe_card_md'].search(remaining)
            if vibe_card_md_match:
                before_text = remaining[:vibe_card_md_match.start()].strip()
                card_content = vibe_card_md_match.group(1).strip()
                annotation = vibe_card_md_match.group(2).strip()
                remaining = remaining[vibe_card_md_match.end():].strip()
                text += before_text + ' ' + f'__{card_content}__' + ' '
                self.tokens.append(('VIBE_CARD', f"{card_content}[{annotation}]", self.current_line_num))
                continue
            
            # 3. 检查传统行内解释 >>解释
            inline_exp_match = self.PATTERNS['inline_explanation'].search(remaining)
            if inline_exp_match:
                before_text = remaining[:inline_exp_match.start()].strip()
                if before_text:
                    text += before_text
                explanation = inline_exp_match.group(1)
                remaining = remaining[inline_exp_match.end():].strip()
                continue
            
            # 4. 检查极简行内解释 ^解释
            inline_exp_md_match = self.PATTERNS['inline_explanation_md'].search(remaining)
            if inline_exp_md_match:
                before_text = remaining[:inline_exp_md_match.start()].strip()
                if before_text:
                    text += before_text
                explanation = inline_exp_md_match.group(1)
                remaining = remaining[inline_exp_md_match.end():].strip()
                continue
            
            # 5. 如果没有匹配到任何特殊模式，将剩余内容作为普通文本
            if remaining:
                text += remaining
                break
        
        # 添加普通文本
        if text:
            self.tokens.append(('TEXT', text, self.current_line_num))
        if explanation:
            self.tokens.append(('INLINE_EXPLANATION', explanation, self.current_line_num))

def print_tokens(tokens):
    """打印词法分析结果"""
    print("词法分析结果:")
    print("-" * 50)
    for token_type, token_value, line_num in tokens:
        print(f"行 {line_num:3d}: {token_type:20} {token_value}")
    print("-" * 50)

# 测试代码
if __name__ == "__main__":
    # 测试用例 - 传统语法
    test_code_traditional = """
--<Vocabulary>--
gugugaga
<+vigilant
(>: #careful, #watchful, 近义词)
(!: 重要)
---解释
adj. 警惕的；警觉的；戒备的
---词组
- be vigilant about/against/over >>对…保持警惕
- remain/stay vigilant >>保持警惕
- require vigilance >>（需要警惕性）
1. rrrr  >> 很烦恼的样子
3. aaaa  >> 123123
---例句
- Citizens are urged to remain vigilant against cyber scams. `网络诈骗`[指通过互联网进行的欺诈行为] >>敦促公民对网络诈骗保持警惕
/+>
"""
    
    # 测试用例 - 极简语法
    test_code_markdown = """
# 词汇表

## vigilant
[@参考:#careful, #watchful, 近义词]
[@重要]

### 释义
adj. 警惕的；警觉的；戒备的 ^来自拉丁语

### 词组
- be vigilant about/against/over ^对…保持警惕
- remain/stay vigilant ^保持警惕

### 例句
- Citizens are urged to remain vigilant [cyber scams|网络骗局] against cyber scams. ^敦促公民对网络诈骗保持警惕
"""
    
    # 测试用例 - 混合语法
    test_code_mixed = """
# 混合语法测试

## 传统卡片
(!: 重要标签)
---区域 1
这是传统语法的内容 `注卡`[批注内容] >>行内解释

## 极简卡片
[@参考:#传统卡片]
### 极简区域
这是极简语法的内容 [注卡 | 批注] ^行内解释
"""
    
    print("=" * 60)
    print("传统语法测试:")
    print("=" * 60)
    lexer = Lexer()
    tokens = lexer.tokenize(test_code_traditional)
    print_tokens(tokens)
    
    print("\n" + "=" * 60)
    print("极简语法测试:")
    print("=" * 60)
    lexer2 = Lexer()
    tokens2 = lexer2.tokenize(test_code_markdown)
    print_tokens(tokens2)
    
    print("\n" + "=" * 60)
    print("混合语法测试:")
    print("=" * 60)
    lexer3 = Lexer()
    tokens3 = lexer3.tokenize(test_code_mixed)
    print_tokens(tokens3)
