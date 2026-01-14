"""
Skill Executor - 将 skill 资源转换为可执行的 Agno 工具。

处理从 skills 动态加载脚本、references 和 assets。
"""

import sys
import importlib.util
import subprocess
from pathlib import Path
from typing import Callable, List, Dict, Any, Optional
from .skill_loader import SkillContent


class SkillExecutor:
    """执行 skill 资源并将其转换为 Agno 兼容的工具。"""
    
    def __init__(self):
        self._loaded_scripts: Dict[str, List[Callable]] = {}
        self._loaded_references: Dict[str, str] = {}
    
    def create_agno_tools(self, skill_content: SkillContent) -> List[Callable]:
        """
        从 skill 资源创建 Agno 兼容的工具函数。
        
        将 skill 脚本转换为可调用的函数，可以作为工具
        添加到 Agno agent 中。
        
        参数:
            skill_content: 包含资源路径的完整 skill 内容
            
        返回:
            用作 Agno 工具的可调用函数列表
        """
        tools = []
        skill_name = skill_content.metadata.name
        
        # 如果可用，加载脚本
        if skill_content.scripts_dir:
            script_tools = self.load_skill_scripts(skill_content.scripts_dir, skill_name)
            tools.extend(script_tools)
        
        # 如果可用，创建访问 references 的工具
        if skill_content.references_dir:
            reference_tool = self._create_reference_accessor(
                skill_content.references_dir,
                skill_name
            )
            tools.append(reference_tool)
        
        # 如果可用，创建访问 assets 的工具
        if skill_content.assets_dir:
            assets_tool = self._create_assets_accessor(
                skill_content.assets_dir,
                skill_name
            )
            tools.append(assets_tool)
        
        return tools
    
    def load_skill_scripts(self, scripts_dir: Path, skill_name: str) -> List[Callable]:
        """
        从 skill 的 scripts 目录加载 Python 脚本。
        
        动态导入 Python 文件并创建包装函数，
        可用作 Agno 工具。
        
        参数:
            scripts_dir: scripts 目录路径
            skill_name: skill 名称（用于命名空间）
            
        返回:
            可调用包装函数列表
        """
        if skill_name in self._loaded_scripts:
            return self._loaded_scripts[skill_name]
        
        tools = []
        
        # 查找所有 Python 文件
        python_files = list(scripts_dir.glob("*.py"))
        
        for script_path in python_files:
            # 跳过 __init__.py 和私有文件
            if script_path.name.startswith("_"):
                continue
            
            try:
                tool = self._create_script_runner(script_path, skill_name)
                tools.append(tool)
            except Exception as e:
                print(f"Warning: Failed to load script {script_path}: {e}")
                continue
        
        self._loaded_scripts[skill_name] = tools
        return tools
    
    def _create_script_runner(self, script_path: Path, skill_name: str) -> Callable:
        """
        创建运行 Python 脚本的包装函数。
        
        不导入脚本（可能有复杂依赖），
        而是创建一个作为子进程运行它的函数。
        
        参数:
            script_path: Python 脚本路径
            skill_name: skill 名称
            
        返回:
            可调用包装函数
        """
        script_name = script_path.stem
        
        def run_script(*args, **kwargs) -> str:
            """
            使用提供的参数运行 skill 脚本。
            
            参数:
                *args: 传递给脚本的位置参数
                **kwargs: 以 --key=value 形式传递的关键字参数
                
            返回:
                脚本输出字符串
            """
            cmd = [sys.executable, str(script_path)]
            
            # 添加位置参数
            for arg in args:
                cmd.append(str(arg))
            
            # 添加关键字参数为 --key=value
            for key, value in kwargs.items():
                cmd.append(f"--{key}={value}")
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 分钟超时
                    cwd=script_path.parent
                )
                
                if result.returncode != 0:
                    return f"Error running script: {result.stderr}"
                
                return result.stdout
                
            except subprocess.TimeoutExpired:
                return "Error: Script execution timed out (5 minutes)"
            except Exception as e:
                return f"Error: {str(e)}"
        
        # 为 Agno 设置函数元数据
        run_script.__name__ = f"{skill_name}_{script_name}"
        run_script.__doc__ = f"从 {skill_name} skill 运行 {script_name} 脚本。使用 --help 标志查看脚本用法。"
        
        return run_script
    
    def _create_reference_accessor(self, references_dir: Path, skill_name: str) -> Callable:
        """
        创建访问参考文档的工具函数。
        
        参数:
            references_dir: references 目录路径
            skill_name: skill 名称
            
        返回:
            读取参考文件的可调用函数
        """
        def read_reference(filename: str) -> str:
            """
            从 skill 的 references 目录读取参考文件。
            
            参数:
                filename: 参考文件名称（例如 'finance.md', 'REFERENCE.md'）
                
            返回:
                参考文件内容
            """
            ref_path = references_dir / filename
            
            if not ref_path.exists():
                # 列出可用的参考文件
                available = [f.name for f in references_dir.iterdir() if f.is_file()]
                return f"Reference file '{filename}' not found. Available references: {', '.join(available)}"
            
            try:
                with open(ref_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content
            except Exception as e:
                return f"Error reading reference: {str(e)}"
        
        read_reference.__name__ = f"{skill_name}_read_reference"
        read_reference.__doc__ = f"从 {skill_name} skill 读取参考文档。提供要读取的文件名。"
        
        return read_reference
    
    def _create_assets_accessor(self, assets_dir: Path, skill_name: str) -> Callable:
        """
        创建列出和访问资源的工具函数。
        
        参数:
            assets_dir: assets 目录路径
            skill_name: skill 名称
            
        返回:
            处理资源的可调用函数
        """
        def list_assets(pattern: str = "*") -> str:
            """
            列出 skill 的 assets 目录中可用的资源。
            
            参数:
                pattern: 过滤资源的 Glob 模式（默认："*" 表示全部）
                
            返回:
                资源文件及其路径列表
            """
            try:
                assets = list(assets_dir.glob(pattern))
                if not assets:
                    return f"No assets found matching pattern '{pattern}'"
                
                result = [f"Assets in {skill_name}:"]
                for asset in assets:
                    rel_path = asset.relative_to(assets_dir)
                    asset_type = "dir" if asset.is_dir() else "file"
                    result.append(f"- {rel_path} ({asset_type})")
                
                return "\n".join(result)
            except Exception as e:
                return f"Error listing assets: {str(e)}"
        
        list_assets.__name__ = f"{skill_name}_list_assets"
        list_assets.__doc__ = f"列出 {skill_name} skill 的资源文件。可选提供 glob 模式进行过滤。"
        
        return list_assets
    
    def load_skill_references(self, references_dir: Path, skill_name: str) -> str:
        """
        将所有参考内容加载为单个字符串。
        
        用于将参考文档添加到 agent 上下文或知识库。
        
        参数:
            references_dir: references 目录路径
            skill_name: skill 名称
            
        返回:
            所有参考文件的合并内容
        """
        if skill_name in self._loaded_references:
            return self._loaded_references[skill_name]
        
        content_parts = [f"# References for {skill_name} skill\n"]
        
        for ref_file in references_dir.glob("*.md"):
            try:
                with open(ref_file, "r", encoding="utf-8") as f:
                    content = f.read()
                content_parts.append(f"\n## {ref_file.name}\n")
                content_parts.append(content)
            except Exception as e:
                content_parts.append(f"\n## {ref_file.name}\nError loading: {e}\n")
        
        combined = "\n".join(content_parts)
        self._loaded_references[skill_name] = combined
        
        return combined
    
    def get_script_help(self, script_path: Path) -> str:
        """
        通过运行脚本的 --help 标志获取帮助文本。
        
        参数:
            script_path: 脚本路径
            
        返回:
            帮助文本输出
        """
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Could not get help: {str(e)}"
    
    def clear_cache(self):
        """清除所有缓存的脚本和参考文档。"""
        self._loaded_scripts.clear()
        self._loaded_references.clear()
