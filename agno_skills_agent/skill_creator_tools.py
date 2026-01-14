"""
Skill Creator Tools - 创建和管理 skills 的辅助函数。

提供与 skills-examples 中 skill-creator 脚本的集成。
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional


class SkillCreatorTools:
    """创建和管理 skills 的工具。"""
    
    def __init__(self, skills_examples_dir: Optional[Path] = None):
        """
        初始化 skill 创建工具。
        
        参数:
            skills_examples_dir: skills-examples 目录路径
                                如果为 None，尝试相对于当前位置查找
        """
        if skills_examples_dir:
            self.skills_examples_dir = Path(skills_examples_dir)
        else:
            # 尝试相对于当前文件查找 skills-examples
            current_dir = Path(__file__).parent.parent
            self.skills_examples_dir = current_dir / "skills-examples"
        
        self.skill_creator_dir = self.skills_examples_dir / "skills" / "skill-creator"
        self.scripts_dir = self.skill_creator_dir / "scripts"
        
        # 检查 skill-creator 是否存在
        if not self.skill_creator_dir.exists():
            print(f"Warning: skill-creator not found at {self.skill_creator_dir}")
    
    def init_skill(self, skill_name: str, output_path: Optional[str] = None) -> str:
        """
        使用 init_skill.py 脚本初始化新的 skill。
        
        创建包含模板 SKILL.md 和示例文件的新 skill 目录。
        
        参数:
            skill_name: 要创建的 skill 名称
            output_path: skill 应该创建的目录（可选）
            
        返回:
            init_skill.py 脚本的输出
        """
        init_script = self.scripts_dir / "init_skill.py"
        
        if not init_script.exists():
            return f"Error: init_skill.py not found at {init_script}"
        
        cmd = [sys.executable, str(init_script), skill_name]
        
        if output_path:
            cmd.extend(["--path", output_path])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return f"Error creating skill:\n{result.stderr}"
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            return "Error: Skill creation timed out"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def package_skill(self, skill_path: str, output_dir: Optional[str] = None) -> str:
        """
        将 skill 打包为可分发的 .skill 文件。
        
        验证 skill 并创建 .skill zip 文件。
        
        参数:
            skill_path: skill 目录路径
            output_dir: 应创建 .skill 文件的目录（可选）
            
        返回:
            package_skill.py 脚本的输出
        """
        package_script = self.scripts_dir / "package_skill.py"
        
        if not package_script.exists():
            return f"Error: package_skill.py not found at {package_script}"
        
        cmd = [sys.executable, str(package_script), skill_path]
        
        if output_dir:
            cmd.append(output_dir)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return f"Error packaging skill:\n{result.stderr}"
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            return "Error: Skill packaging timed out"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def validate_skill(self, skill_path: str) -> str:
        """
        使用 quick_validate.py 脚本验证 skill。
        
        检查 skill 是否遵循 Agent Skills 规范。
        
        参数:
            skill_path: skill 目录路径
            
        返回:
            验证结果
        """
        validate_script = self.scripts_dir / "quick_validate.py"
        
        if not validate_script.exists():
            return f"Error: quick_validate.py not found at {validate_script}"
        
        cmd = [sys.executable, str(validate_script), skill_path]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return f"Validation failed:\n{result.stderr}"
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            return "Error: Validation timed out"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_init_help(self) -> str:
        """获取 init_skill.py 的帮助文本。"""
        init_script = self.scripts_dir / "init_skill.py"
        
        if not init_script.exists():
            return "init_skill.py not found"
        
        try:
            result = subprocess.run(
                [sys.executable, str(init_script), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_package_help(self) -> str:
        """获取 package_skill.py 的帮助文本。"""
        package_script = self.scripts_dir / "package_skill.py"
        
        if not package_script.exists():
            return "package_skill.py not found"
        
        try:
            result = subprocess.run(
                [sys.executable, str(package_script), "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"


def create_skill_creator_tools(skills_agent) -> list:
    """
    创建可添加到 agent 的 skill 创建工具函数。
    
    参数:
        skills_agent: SkillsAgent 实例
        
    返回:
        工具函数列表
    """
    # 查找 skills-examples 目录
    skills_examples_dir = skills_agent.skills_dir.parent
    creator = SkillCreatorTools(skills_examples_dir)
    
    def create_new_skill(skill_name: str, output_path: Optional[str] = None) -> str:
        """
        创建包含模板文件的新 skill。
        
        初始化包含以下内容的新 skill 目录：
        - 带有正确 frontmatter 的 SKILL.md 模板
        - 示例 scripts/ 目录
        - 示例 references/ 目录
        - 示例 assets/ 目录
        
        参数:
            skill_name: 新 skill 的名称（小写，空格用连字符）
            output_path: 创建 skill 的位置（可选，默认为当前目录）
            
        返回:
            状态消息
        """
        return creator.init_skill(skill_name, output_path)
    
    def package_skill_file(skill_path: str, output_dir: Optional[str] = None) -> str:
        """
        将 skill 打包为可分发的 .skill 文件。
        
        验证并将 skill 打包为可共享的 .skill zip 文件。
        
        参数:
            skill_path: skill 目录路径
            output_dir: 保存 .skill 文件的位置（可选）
            
        返回:
            包含 .skill 文件路径的状态消息
        """
        return creator.package_skill(skill_path, output_dir)
    
    def validate_skill_format(skill_path: str) -> str:
        """
        验证 skill 是否遵循 Agent Skills 规范。
        
        检查：
        - YAML frontmatter 格式和必需字段
        - Skill 命名约定
        - 目录结构
        - 文件组织
        
        参数:
            skill_path: skill 目录路径
            
        返回:
            验证结果
        """
        return creator.validate_skill(skill_path)
    
    return [create_new_skill, package_skill_file, validate_skill_format]
