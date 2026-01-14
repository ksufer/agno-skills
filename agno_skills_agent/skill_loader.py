"""
Skill Loader - 发现和加载 Agent Skills 的元数据和内容。

通过渐进式披露实现：初始时只加载元数据，
仅在需要时才加载完整内容。
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field


class SkillMetadata(BaseModel):
    """从 SKILL.md frontmatter 提取的 skill 元数据。"""
    
    name: str = Field(description="从 frontmatter 获取的 skill 名称")
    description: str = Field(description="Skill 描述 - 何时使用此 skill")
    path: Path = Field(description="skill 目录的完整路径")
    license: Optional[str] = Field(default=None, description="许可证信息")
    compatibility: Optional[str] = Field(default=None, description="兼容性要求")
    metadata: Optional[Dict[str, str]] = Field(default=None, description="附加元数据")
    
    class Config:
        arbitrary_types_allowed = True


class SkillContent(BaseModel):
    """包含元数据和指令的完整 skill 内容。"""
    
    metadata: SkillMetadata
    instructions: str = Field(description="完整的 SKILL.md 正文内容")
    scripts_dir: Optional[Path] = Field(default=None, description="scripts 目录路径")
    references_dir: Optional[Path] = Field(default=None, description="references 目录路径")
    assets_dir: Optional[Path] = Field(default=None, description="assets 目录路径")
    
    class Config:
        arbitrary_types_allowed = True


class SkillLoader:
    """从文件系统加载和管理 Agent Skills。"""
    
    def __init__(self):
        self._metadata_cache: Dict[str, SkillMetadata] = {}
        self._content_cache: Dict[str, SkillContent] = {}
    
    def discover_skills(self, skills_dir: Path) -> Dict[str, SkillMetadata]:
        """
        发现指定目录中的所有 skills。
        
        扫描包含 SKILL.md 文件的目录并加载其元数据。
        实现渐进式披露 - 只加载 frontmatter，不加载完整内容。
        
        参数:
            skills_dir: 包含 skill 文件夹的目录路径
            
        返回:
            将 skill 名称映射到其元数据的字典
        """
        skills_dir = Path(skills_dir)
        if not skills_dir.exists():
            raise ValueError(f"Skills directory does not exist: {skills_dir}")
        
        discovered_skills = {}
        
        # 扫描 skill 目录
        for skill_path in skills_dir.iterdir():
            if not skill_path.is_dir():
                continue
            
            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue
            
            try:
                metadata = self._load_metadata(skill_path, skill_md)
                discovered_skills[metadata.name] = metadata
                self._metadata_cache[metadata.name] = metadata
            except Exception as e:
                print(f"Warning: Failed to load skill from {skill_path}: {e}")
                continue
        
        return discovered_skills
    
    def _load_metadata(self, skill_path: Path, skill_md_path: Path) -> SkillMetadata:
        """
        从 SKILL.md frontmatter 加载元数据。
        
        只解析 YAML frontmatter，不加载完整的 Markdown 正文。
        这在 skill 发现期间保持最小的上下文使用。
        
        参数:
            skill_path: skill 目录路径
            skill_md_path: SKILL.md 文件路径
            
        返回:
            SkillMetadata 对象
        """
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取 YAML frontmatter
        frontmatter = self._extract_frontmatter(content)
        if not frontmatter:
            raise ValueError(f"No valid YAML frontmatter found in {skill_md_path}")
        
        # 解析 YAML
        try:
            data = yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {skill_md_path}: {e}")
        
        # 验证必需字段
        if "name" not in data:
            raise ValueError(f"Missing required 'name' field in {skill_md_path}")
        if "description" not in data:
            raise ValueError(f"Missing required 'description' field in {skill_md_path}")
        
        # 创建元数据对象
        return SkillMetadata(
            name=data["name"],
            description=data["description"],
            path=skill_path,
            license=data.get("license"),
            compatibility=data.get("compatibility"),
            metadata=data.get("metadata"),
        )
    
    def _extract_frontmatter(self, content: str) -> Optional[str]:
        """
        从 Markdown 内容中提取 YAML frontmatter。
        
        Frontmatter 由开头和结尾的 --- 分隔。
        
        参数:
            content: 完整的 Markdown 内容
            
        返回:
            YAML frontmatter 字符串，如果未找到则返回 None
        """
        pattern = r"^---\s*\n(.*?)\n---\s*\n"
        match = re.match(pattern, content, re.DOTALL)
        if match:
            return match.group(1)
        return None
    
    def load_full_skill(self, skill_name: str) -> SkillContent:
        """
        加载包含指令的完整 skill 内容。
        
        当 skill 被激活并需要完整上下文时调用此方法。
        实现渐进式披露的第二阶段。
        
        参数:
            skill_name: 要加载的 skill 名称
            
        返回:
            包含完整指令的 SkillContent 对象
        """
        # 首先检查缓存
        if skill_name in self._content_cache:
            return self._content_cache[skill_name]
        
        # 获取元数据
        if skill_name not in self._metadata_cache:
            raise ValueError(f"Skill not found: {skill_name}")
        
        metadata = self._metadata_cache[skill_name]
        skill_md_path = metadata.path / "SKILL.md"
        
        # 加载完整内容
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取指令（frontmatter 之后的所有内容）
        frontmatter_end = content.find("---\n", 4)  # 找到第二个 ---
        if frontmatter_end == -1:
            instructions = ""
        else:
            instructions = content[frontmatter_end + 4:].strip()
        
        # 检查可选目录
        scripts_dir = metadata.path / "scripts"
        references_dir = metadata.path / "references"
        assets_dir = metadata.path / "assets"
        
        skill_content = SkillContent(
            metadata=metadata,
            instructions=instructions,
            scripts_dir=scripts_dir if scripts_dir.exists() else None,
            references_dir=references_dir if references_dir.exists() else None,
            assets_dir=assets_dir if assets_dir.exists() else None,
        )
        
        # 缓存结果
        self._content_cache[skill_name] = skill_content
        
        return skill_content
    
    def get_metadata(self, skill_name: str) -> Optional[SkillMetadata]:
        """获取 skill 的缓存元数据。"""
        return self._metadata_cache.get(skill_name)
    
    def list_skills(self) -> list[str]:
        """获取所有已发现的 skill 名称列表。"""
        return list(self._metadata_cache.keys())
    
    def clear_cache(self):
        """清除所有缓存。"""
        self._metadata_cache.clear()
        self._content_cache.clear()
