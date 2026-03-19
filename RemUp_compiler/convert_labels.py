import re

def convert_labels(input_file, output_file):
    """将 [@标签] 格式转换为 (符号：内容) 格式"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计信息
    stats = {
        '重要': 0,
        '系列': 0,
        '基础概念': 0,
        '重要性': 0,
        '核心特色': 0,
        '参考': 0,
        '前置': 0,
        '相关': 0,
        '对比': 0,
        '进阶': 0,
        '应用': 0,
        '难度': 0,
        '示例': 0,
        '信息': 0,
        '问题': 0,
        '完成': 0,
        '后续': 0,
        '优先级': 0,
        '分类': 0,
        '时间估算': 0,
        '状态': 0,
        '高级特性': 0,
        '其他': 0
    }
    
    def replace_label(match):
        """替换单个标签"""
        label_text = match.group(1).strip()
        
        # 解析标签类型和内容
        if ':' in label_text:
            parts = label_text.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
        else:
            key = label_text
            value = ''
        
        # 映射规则
        mapping = {
            '重要': ('!', '重要'),
            '基础概念': ('!', '基础概念'),
            '核心特色': ('!', '核心特色'),
            '核心概念': ('!', '核心概念'),
            '参考': ('>', value),
            '前置': ('>', value),
            '后续': ('>', value),
            '相关': ('>', value),
            '对比': ('>', value),
            '应用': ('>', value),
            '示例': ('>', value),
            '系列': ('系列', value),
            '重要性': ('*', value),
            '难度': ('难度', value),
            '信息': ('i', '信息'),
            '问题': ('?', '问题'),
            '完成': ('✓', '完成'),
            '优先级': ('优先级', value),
            '分类': ('分类', value),
            '时间估算': ('时间', value),
            '状态': ('状态', value),
            '高级特性': ('*', '高级特性'),
            '进阶': ('*', '进阶'),
        }
        
        # 查找匹配的规则
        for pattern_key, (symbol, default_value) in mapping.items():
            if key == pattern_key or key.startswith(pattern_key):
                final_value = value if value else default_value
                stats[key] = stats.get(key, 0) + 1
                return f'({symbol}: {final_value})'
        
        # 默认处理
        if value:
            stats['其他'] = stats.get('其他', 0) + 1
            return f'(!: {label_text})'
        else:
            stats['其他'] = stats.get('其他', 0) + 1
            return f'(!: {key})'
    
    # 正则表达式匹配 [@...] 格式
    pattern = r'\[@([^\]]+)\]'
    new_content = re.sub(pattern, replace_label, content)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # 打印统计信息
    print("=" * 60)
    print("标签转换统计:")
    print("=" * 60)
    for label_type, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"{label_type:15} {count:3d} 个")
    print("=" * 60)
    print(f"总计：{sum(stats.values())} 个标签已转换")
    print("=" * 60)
    print(f"\n✅ 转换完成！")
    print(f"   源文件：{input_file}")
    print(f"   目标文件：{output_file}")

if __name__ == "__main__":
    convert_labels('INTRODUCTION.remup', 'INTRODUCTION_converted.remup')