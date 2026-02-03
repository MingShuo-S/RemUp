#!/usr/bin/env python3
"""
RemUp编译器 v3.3 - 优化文件占用处理和复制逻辑
"""

import os
import sys
import shutil
import time
import hashlib
from pathlib import Path
from typing import Optional, List
from remup.parser import Parser
from remup.lexer import Lexer
from remup.html_generator import HTMLGenerator

class Compiler:
    """RemUp编译器 - 协调编译流程"""
    
    def __init__(self, project_root: str = None):
        """
        初始化编译器
        
        Args:
            project_root: 项目根目录，用于查找静态资源
        """
        # 检测项目根目录
        self.project_root = self._detect_project_root(project_root)
        self.html_generator = HTMLGenerator(project_root=str(self.project_root))
        
        print(f"🔧 编译器初始化完成")
        print(f"📁 项目根目录: {self.project_root}")
    
    def _detect_project_root(self, project_root: str = None) -> Path:
        """
        检测项目根目录
        
        Args:
            project_root: 用户指定的项目根目录
            
        Returns:
            检测到的项目根目录Path对象
        """
        # 如果用户指定了项目根目录，直接使用
        if project_root:
            root_path = Path(project_root)
            if (root_path / "static" / "css").exists():
                return root_path
            else:
                print(f"⚠️ 指定目录无static/css: {root_path}")
        
        # 自动检测项目根目录
        possible_roots = [
            # 1. 当前工作目录
            Path.cwd(),
            # 2. 脚本文件所在目录的父目录（编译器在remup包内）
            Path(__file__).parent.parent,
            # 3. 环境变量指定的目录
            Path(os.environ.get('REMUP_PROJECT_ROOT', '')),
        ]
        
        # 检查可能的根目录
        for root in possible_roots:
            if root.exists():
                css_dir = root / "static" / "css"
                if css_dir.exists():
                    print(f"✅ 检测到项目根目录: {root}")
                    return root
        
        # 如果都没找到，使用当前工作目录
        fallback_root = Path.cwd()
        print(f"⚠️ 未检测到标准项目结构，使用回退目录: {fallback_root}")
        return fallback_root
    
    def _is_file_locked(self, filepath: Path) -> bool:
        """
        检查文件是否被占用（Windows系统）
        
        Args:
            filepath: 要检查的文件路径
            
        Returns:
            bool: True表示文件被占用，False表示文件可用
        """
        if os.name != 'nt':  # 非Windows系统直接返回False
            return False
            
        try:
            # 尝试以独占模式打开文件，如果成功则文件未被占用
            with open(filepath, 'a', encoding='utf-8') as f:
                pass
            return False
        except (PermissionError, OSError) as e:
            # 特定的错误码表示文件被占用
            if hasattr(e, 'winerror') and e.winerror == 32:  # ERROR_SHARING_VIOLATION
                return True
            # 其他权限错误也视为文件被占用
            if "Permission denied" in str(e):
                return True
            return False
    
    def _are_files_identical(self, file1: Path, file2: Path) -> bool:
        """
        比较两个文件的内容是否完全相同。
        先比较文件大小，如果不同则直接返回False；如果相同，再比较MD5哈希值。
        """
        # 检查文件是否存在
        if not file1.exists() or not file2.exists():
            return False
            
        # 快速检查：文件大小不同则内容必然不同
        try:
            if file1.stat().st_size != file2.stat().st_size:
                return False
        except OSError:
            return False

        # 详细检查：计算并比较MD5哈希值
        def get_file_md5(filepath):
            hash_md5 = hashlib.md5()
            try:
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                return hash_md5.hexdigest()
            except (OSError, IOError):
                return None

        md5_1 = get_file_md5(file1)
        md5_2 = get_file_md5(file2)
        
        if md5_1 is None or md5_2 is None:
            return False
            
        return md5_1 == md5_2

    def _safe_copy_file(self, source: Path, target: Path, max_retries: int = 3, retry_delay: float = 0.5) -> bool:
        """
        安全复制文件，处理文件占用情况
        
        Args:
            source: 源文件路径
            target: 目标文件路径
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            
        Returns:
            bool: 复制是否成功
        """
        # 检查源文件是否存在
        if not source.exists():
            print(f"❌ 源文件不存在: {source}")
            return False
            
        # 检查是否是同一个文件（避免自我复制）
        if source.resolve() == target.resolve():
            print(f"⏩ 跳过自我复制: {source.name}")
            return True

        for attempt in range(max_retries + 1):  # +1 包括第一次尝试
            try:
                # 检查源文件是否被占用
                if self._is_file_locked(source):
                    if attempt < max_retries:
                        print(f"⏳ 源文件被占用，等待重试... ({attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"⚠️ 跳过文件 {source.name}，重试{max_retries}次后仍被占用")
                        return False
                
                # 检查目标文件是否被占用（如果存在）
                if target.exists() and self._is_file_locked(target):
                    if attempt < max_retries:
                        print(f"⏳ 目标文件被占用，等待重试... ({attempt + 1}/{max_retries})")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"⚠️ 跳过文件 {target.name}，重试{max_retries}次后目标文件仍被占用")
                        return False
                
                # 执行复制操作
                shutil.copy2(source, target)
                return True
                
            except PermissionError as e:
                if attempt < max_retries:
                    print(f"⏳ 权限错误，等待重试... ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    print(f"❌ 复制文件失败 {source.name}: 权限错误 - {e}")
                    return False
                    
            except OSError as e:
                # 处理其他系统错误
                if attempt < max_retries:
                    print(f"⏳ 系统错误，等待重试... ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    print(f"❌ 复制文件失败 {source.name}: 系统错误 - {e}")
                    return False
                    
            except Exception as e:
                print(f"❌ 复制文件失败 {source.name}: 未知错误 - {e}")
                return False
        
        return False

    def _copy_static_css_files(self, output_dir: Path):
        """
        安全地复制静态CSS文件到输出目录。
        优化版本：避免重复复制和文件占用问题。
        """
        source_css_dir = self.project_root / "static" / "css"
        if not source_css_dir.exists():
            print(f"⚠️ 源CSS目录不存在: {source_css_dir}")
            return

        # 检查源目录和目标目录是否相同
        target_css_dir = output_dir / "static" / "css"
        if source_css_dir.resolve() == target_css_dir.resolve():
            print(f"⏩ 跳过静态资源复制: 源目录和目标目录相同")
            return

        target_css_dir.mkdir(parents=True, exist_ok=True)

        css_files = list(source_css_dir.glob("*.css"))
        if not css_files:
            print(f"⚠️ 在 {source_css_dir} 中未找到CSS文件")
            return

        copied_count = 0
        skipped_count = 0
        error_count = 0

        for css_file in css_files:
            target_file = target_css_dir / css_file.name
            
            # 检查目标文件是否已存在且内容相同
            if target_file.exists():
                if self._are_files_identical(css_file, target_file):
                    skipped_count += 1
                    print(f"⏩ 跳过CSS文件: {css_file.name} (目标文件已存在且内容相同)")
                    continue
                else:
                    # 内容不同，尝试覆盖
                    if self._safe_copy_file(css_file, target_file):
                        copied_count += 1
                        print(f"🔄 更新CSS文件: {css_file.name} -> {target_file}")
                    else:
                        error_count += 1
            else:
                # 目标文件不存在，直接复制
                if self._safe_copy_file(css_file, target_file):
                    copied_count += 1
                    print(f"✅ 复制CSS文件: {css_file.name} -> {target_file}")
                else:
                    error_count += 1

        # 输出最终报告
        print(f"📄 静态资源处理完成: 新增/更新 {copied_count} 个, 跳过 {skipped_count} 个, 失败 {error_count} 个")
        
        # 如果所有文件都跳过了，说明目标目录已经有完整的静态资源
        if skipped_count == len(css_files) and copied_count == 0 and error_count == 0:
            print("💡 提示: 所有CSS文件都已存在且内容相同，无需更新")
    
    def compile(self, input_path: str, output_path: str = None, 
                theme: str = "RemStyle", page_title: str = None) -> str:
        """
        编译RemUp文件为HTML - 优化文件处理流程
        """
        print(f"🔨 开始编译: {input_path}")
        print(f"🎨 使用主题: {theme}")
        
        # 验证输入文件
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
        
        # 自动生成输出路径
        if output_path is None:
            output_path = input_path.with_suffix('.html')
        else:
            output_path = Path(output_path)
        
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制静态CSS文件到输出目录（优化后的版本）
        self._copy_static_css_files(output_path.parent)
        
        # 读取源代码
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            raise IOError(f"无法读取源文件 {input_path}: {e}")
        
        # 词法分析和语法分析
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)
        parser = Parser(tokens)
        document = parser.parse()
        
        # 生成HTML
        try:
            result_path = self.html_generator.generate(
                document=document,
                output_path=str(output_path),
                theme=theme,
                page_title=page_title
            )
        except Exception as e:
            # 特别处理文件占用错误
            if "WinError 32" in str(e) or "另一个程序正在使用此文件" in str(e):
                print("💡 提示: 文件被占用，请关闭可能正在使用CSS文件的程序（如资源管理器、编辑器）")
                print("💡 临时解决方案: 使用 --no-static 参数跳过静态资源复制")
            raise e
        
        # 打印编译摘要
        self._print_compilation_summary(document, result_path, theme)
        
        return result_path
    
    def compile_directory(self, input_dir: str, output_dir: str = None,
                         theme: str = "RemStyle", recursive: bool = False) -> List[str]:
        """
        编译目录中的所有RemUp文件
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录（可选）
            theme: 主题名称
            recursive: 是否递归处理子目录
            
        Returns:
            成功编译的文件路径列表
        """
        input_dir = Path(input_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"输入目录不存在: {input_dir}")
        
        # 设置输出目录
        if output_dir is None:
            output_dir = input_dir / "html_output"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 查找RemUp文件
        pattern = "**/*.remup" if recursive else "*.remup"
        remup_files = list(input_dir.glob(pattern))
        
        if not remup_files:
            print(f"⚠️ 在目录 {input_dir} 中未找到 .remup 文件")
            return []
        
        print(f"📁 发现 {len(remup_files)} 个RemUp文件")
        
        compiled_files = []
        for remup_file in remup_files:
            try:
                # 保持目录结构
                relative_path = remup_file.relative_to(input_dir)
                output_file = output_dir / relative_path.with_suffix('.html')
                
                # 确保输出子目录存在
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 编译文件
                result_path = self.compile(
                    input_path=str(remup_file),
                    output_path=str(output_file),
                    theme=theme
                )
                compiled_files.append(result_path)
                
            except Exception as e:
                print(f"❌ 编译失败 {remup_file}: {e}")
                continue
        
        print(f"✅ 成功编译 {len(compiled_files)}/{len(remup_files)} 个文件")
        return compiled_files
    
    def list_available_themes(self) -> List[str]:
        """列出所有可用的主题"""
        return self.html_generator.get_available_themes()
    
    def _print_compilation_summary(self, document, output_path: str, theme: str):
        """打印编译摘要"""
        total_cards = sum(len(archive.cards) for archive in document.archives)
        total_vibe_cards = 0
        for archive in document.archives:
            for card in archive.cards:
                total_vibe_cards += len(card.vibe_cards)
        
        print("=" * 60)
        print("🎉 编译完成!")
        print("=" * 60)
        print(f"📁 输出文件: {output_path}")
        print(f"🎨 使用主题: {theme}")
        print(f"📂 归档数量: {len(document.archives)}")
        print(f"🃏 卡片总数: {total_cards}")
        print(f"💡 注卡数量: {total_vibe_cards}")
        print(f"📋 注卡归档: {'✅ 有' if document.vibe_archive else '❌ 无'}")
        print("=" * 60)
        
        # 显示可用主题
        available_themes = self.list_available_themes()
        if len(available_themes) > 1:
            print("🎨 可用主题: " + ", ".join(available_themes))
            print("💡 使用 -t 参数切换主题，例如: -t DarkTheme")
            print("=" * 60)

def compile_remup(input_path: str, output_path: str = None, 
                 theme: str = "RemStyle", page_title: str = None) -> str:
    """
    便捷函数：编译单个RemUp文件
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        theme: 主题名称
        page_title: 自定义页面标题
        
    Returns:
        输出文件路径
    """
    compiler = Compiler()
    return compiler.compile(input_path, output_path, theme, page_title)

def compile_remup_directory(input_dir: str, output_dir: str = None,
                          theme: str = "RemStyle", recursive: bool = False) -> List[str]:
    """
    便捷函数：编译目录中的RemUp文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        theme: 主题名称
        recursive: 是否递归处理子目录
        
    Returns:
        成功编译的文件路径列表
    """
    compiler = Compiler()
    return compiler.compile_directory(input_dir, output_dir, theme, recursive)

if __name__ == "__main__":
    # 命令行测试
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        try:
            result = compile_remup(input_file)
            print(f"✅ 编译成功: {result}")
        except Exception as e:
            print(f"❌ 编译失败: {e}")
    else:
        print("用法: python compiler.py <input_file.remup>")