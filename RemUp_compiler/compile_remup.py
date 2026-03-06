#!/usr/bin/env python3
"""
RemUp 文件拖拽编译器 v3.3 - 修复参数错误版本
"""

import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到 Python 路径，确保可以导入 remup 模块
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from remup.compiler import Compiler, compile_remup, compile_remup_directory
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("💡 请确保在正确的项目目录中运行此脚本")
    input("按任意键退出...")
    sys.exit(1)

def get_project_root():
    """检测项目根目录（包含static/css的目录）"""
    possible_roots = [
        Path.cwd(),
        Path(__file__).parent,
        Path(os.environ.get('REMUP_PROJECT_ROOT', '')),
    ]
    
    # 向上查找逻辑
    current = Path.cwd()
    for _ in range(3):
        if (current / "static" / "css").exists():
            possible_roots.append(current)
        current = current.parent
    
    for root in possible_roots:
        if root.exists():
            css_dir = root / "static" / "css"
            if css_dir.exists():
                print(f"✅ 检测到项目根目录: {root}")
                return root
    
    fallback_root = Path.cwd()
    print(f"⚠️ 未检测到标准项目结构，使用回退目录: {fallback_root}")
    return fallback_root

def get_available_themes(project_root: Path):
    """获取可用的主题列表"""
    try:
        compiler = Compiler()
        themes = compiler.list_available_themes()
        return themes if themes else ["RemStyle"]
    except Exception as e:
        print(f"⚠️ 无法获取主题列表: {e}")
        return ["RemStyle"]

def compile_remup_file(file_path, theme="RemStyle", page_title=None):
    """编译单个 .remup 文件 - 修复参数错误"""
    try:
        if page_title is None:  # 添加默认标题
            page_title = os.path.splitext(file_path.name)[0]

        abs_file_path = file_path.resolve()
        print(f"🔨 编译文件: {abs_file_path.name}")
        print(f"🎨 使用主题: {theme}")
        
        # 修复：移除不存在的 copy_static_resources 参数
        result_path = compile_remup(
            input_path=str(abs_file_path),
            output_path=None,  # 使用默认输出路径
            theme=theme,
            page_title=page_title
            # 移除：copy_static_resources=copy_static
        )
        
        print(f"✅ 编译成功: {result_path}")
        return True
            
    except Exception as e:
        print(f"❌ 编译失败: {file_path.name}")
        print(f"   错误详情: {e}")
        return False

def compile_remup_directory(dir_path, theme="RemStyle", recursive=True):
    """编译整个目录 - 修复参数错误"""
    try:
        print(f"📁 编译目录: {dir_path}")
        if recursive:
            print("🔍 递归处理子目录")
        
        # 修复：移除不存在的 copy_static_resources 参数
        result_files = compile_remup_directory(
            input_dir=str(dir_path),
            output_dir=None,  # 使用默认输出路径
            theme=theme,
            recursive=recursive
            # 移除：copy_static_resources=copy_static
        )
        
        if result_files:
            print(f"✅ 成功编译 {len(result_files)} 个文件")
            return True
        else:
            print("❌ 没有文件被成功编译")
            return False
            
    except Exception as e:
        print(f"❌ 目录编译失败: {dir_path}")
        print(f"   错误详情: {e}")
        return False

def main():
    """主函数"""
    # 检测项目根目录
    project_root = get_project_root()
    
    parser = argparse.ArgumentParser(
        description='RemUp 拖拽编译器 v3.3 - 修复参数错误版本',
        add_help=False
    )
    
    # 主参数
    parser.add_argument('paths', nargs='*', help='要编译的文件或目录路径')
    
    # 编译选项
    parser.add_argument('-t', '--theme', default='RemStyle', 
                       help='指定CSS主题 (默认: RemStyle)')
    parser.add_argument('--title', help='自定义页面标题')
    # 移除不存在的参数选项
    # parser.add_argument('--no-static', action='store_true',
    #                    help='不复制静态CSS文件')
    
    # 目录选项
    parser.add_argument('-d', '--directory', action='store_true',
                       help='编译整个目录')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='递归处理子目录')
    
    # 信息选项
    parser.add_argument('-l', '--list-themes', action='store_true',
                       help='列出可用主题')
    parser.add_argument('-v', '--version', action='store_true',
                       help='显示版本信息')
    parser.add_argument('-h', '--help', action='store_true',
                       help='显示帮助信息')
    
    # 解析参数
    args, unknown_args = parser.parse_known_args()
    all_paths = args.paths + unknown_args
    
    # 处理帮助和版本信息
    if args.help or (not all_paths and not args.list_themes and not args.version):
        print("=" * 60)
        print("      RemUp 拖拽编译器 v3.3 - 修复版")
        print("=" * 60)
        print("📁 项目根目录:", project_root)
        print()
        print("修复内容：")
        print("  ✅ 修复了 copy_static_resources 参数错误")
        print("  ✅ 静态资源复制现已内置在编译器中")
        print("  ✅ 优化了错误处理和用户提示")
        print()
        print("用法：")
        print("  1. 拖拽 .remup 文件到此脚本上")
        print("  2. 拖拽包含 .remup 文件的文件夹")
        print("  3. 或使用命令行: python compile_remup.py [选项] 文件或文件夹...")
        print()
        print("编译选项：")
        print("  -t, --theme THEME     指定CSS主题 (默认: RemStyle)")
        print("  --title TITLE         自定义页面标题")
        print("  -d, --directory       编译整个目录")
        print("  -r, --recursive       递归处理子目录")
        print()
        print("信息选项：")
        print("  -l, --list-themes     列出可用主题")
        print("  -v, --version         显示版本信息")
        print("  -h, --help           显示此帮助信息")
        print()
        print("💡 提示：静态CSS文件会自动复制到输出目录")
        print()
        
        themes = get_available_themes(project_root)
        if themes:
            print("🎨 可用主题:")
            for theme in themes:
                print(f"  • {theme}")
            print()
            print("💡 示例: python compile_remup.py -t DarkTheme 文件.remup")
        print("=" * 60)
        
        if not all_paths:
            input("按 Enter 键退出...")
        return 0
    
    if args.version:
        print("RemUp拖拽编译器 v3.3 - 修复版")
        print("修复内容：")
        print("  • 修复了 copy_static_resources 参数错误")
        print("  • 静态资源复制逻辑现已内置在编译器中")
        print("  • 改进了错误提示和用户体验")
        print("  • 保持拖拽编译的便捷性")
        return 0
    
    if args.list_themes:
        themes = get_available_themes(project_root)
        if themes:
            print("🎨 可用主题:")
            for theme in themes:
                print(f"  • {theme}")
        else:
            print("❌ 无法获取主题列表")
        return 0
    
    # 开始处理
    print("=" * 60)
    print("      RemUp 拖拽编译器 v3.3 - 修复版")
    print("=" * 60)
    print(f"📁 项目根目录: {project_root}")
    print("💡 提示: 静态CSS文件会自动复制到输出目录")
    print()
    
    # 编译模式
    all_success = True
    processed_files = 0
    successful_compiles = 0
    
    for path_arg in all_paths:
        path = Path(path_arg)
        
        if not path.exists():
            print(f"❌ 路径不存在: {path}")
            all_success = False
            continue
        
        if args.directory or path.is_dir():
            # 编译目录
            processed_files += 1
            if compile_remup_directory(
                path, 
                theme=args.theme, 
                recursive=args.recursive
                # 移除：copy_static=not args.no_static
            ):
                successful_compiles += 1
            else:
                all_success = False
        
        elif path.is_file() and path.suffix.lower() == '.remup':
            # 单个文件编译
            processed_files += 1
            if compile_remup_file(
                path, 
                theme=args.theme, 
                page_title=args.title
                # 移除：copy_static=not args.no_static
            ):
                successful_compiles += 1
            else:
                all_success = False
        
        else:
            print(f"❌ 忽略不支持的文件: {path}")
        
        print()  # 空行分隔
    
    # 输出总结报告
    print("=" * 60)
    print("编译总结:")
    print(f"  🎨 使用主题: {args.theme}")
    print(f"  📁 处理文件: {processed_files} 个")
    print(f"  ✅ 成功编译: {successful_compiles} 个")
    print(f"  ❌ 失败文件: {processed_files - successful_compiles} 个")
    
    if all_success and processed_files > 0:
        print("🎉 所有文件编译完成！")
        print("💡 静态CSS文件已自动复制到输出目录")
    elif processed_files > 0:
        print("⚠️  部分文件编译失败，请检查错误信息")
    else:
        print("❌ 未找到可编译的文件")
    
    print("=" * 60)
    
    # 如果是拖拽运行，暂停显示结果
    if len(all_paths) > 0:
        input("按 Enter 键退出...")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n🛑 操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生未预期错误: {e}")
        sys.exit(1)