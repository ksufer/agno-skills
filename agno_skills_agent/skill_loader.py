"""
Skill Loader - Discovers and loads Agent Skills metadata and content.

Implements progressive disclosure by loading only metadata initially,
and full content only when needed.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field


class SkillMetadata(BaseModel):
    """Metadata for a skill extracted from SKILL.md frontmatter."""
    
    name: str = Field(description="Skill name from frontmatter")
    description: str = Field(description="Skill description - when to use this skill")
    path: Path = Field(description="Full path to skill directory")
    license: Optional[str] = Field(default=None, description="License information")
    compatibility: Optional[str] = Field(default=None, description="Compatibility requirements")
    metadata: Optional[Dict[str, str]] = Field(default=None, description="Additional metadata")
    
    class Config:
        arbitrary_types_allowed = True


class SkillContent(BaseModel):
    """Full skill content including metadata and instructions."""
    
    metadata: SkillMetadata
    instructions: str = Field(description="Full SKILL.md body content")
    scripts_dir: Optional[Path] = Field(default=None, description="Path to scripts directory")
    references_dir: Optional[Path] = Field(default=None, description="Path to references directory")
    assets_dir: Optional[Path] = Field(default=None, description="Path to assets directory")
    
    class Config:
        arbitrary_types_allowed = True


class SkillLoader:
    """Loads and manages Agent Skills from filesystem."""
    
    def __init__(self):
        self._metadata_cache: Dict[str, SkillMetadata] = {}
        self._content_cache: Dict[str, SkillContent] = {}
    
    def discover_skills(self, skills_dir: Path) -> Dict[str, SkillMetadata]:
        """
        Discover all skills in the given directory.
        
        Scans for directories containing SKILL.md files and loads their metadata.
        Implements progressive disclosure - only loads frontmatter, not full content.
        
        Args:
            skills_dir: Path to directory containing skill folders
            
        Returns:
            Dictionary mapping skill names to their metadata
        """
        skills_dir = Path(skills_dir)
        if not skills_dir.exists():
            raise ValueError(f"Skills directory does not exist: {skills_dir}")
        
        discovered_skills = {}
        
        # Scan for skill directories
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
        Load metadata from SKILL.md frontmatter.
        
        Only parses YAML frontmatter, does not load the full Markdown body.
        This keeps context usage minimal during skill discovery.
        
        Args:
            skill_path: Path to skill directory
            skill_md_path: Path to SKILL.md file
            
        Returns:
            SkillMetadata object
        """
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract YAML frontmatter
        frontmatter = self._extract_frontmatter(content)
        if not frontmatter:
            raise ValueError(f"No valid YAML frontmatter found in {skill_md_path}")
        
        # Parse YAML
        try:
            data = yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {skill_md_path}: {e}")
        
        # Validate required fields
        if "name" not in data:
            raise ValueError(f"Missing required 'name' field in {skill_md_path}")
        if "description" not in data:
            raise ValueError(f"Missing required 'description' field in {skill_md_path}")
        
        # Create metadata object
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
        Extract YAML frontmatter from Markdown content.
        
        Frontmatter is delimited by --- at start and end.
        
        Args:
            content: Full Markdown content
            
        Returns:
            YAML frontmatter string, or None if not found
        """
        pattern = r"^---\s*\n(.*?)\n---\s*\n"
        match = re.match(pattern, content, re.DOTALL)
        if match:
            return match.group(1)
        return None
    
    def load_full_skill(self, skill_name: str) -> SkillContent:
        """
        Load full skill content including instructions.
        
        This is called when a skill is activated and needs full context.
        Implements the second stage of progressive disclosure.
        
        Args:
            skill_name: Name of the skill to load
            
        Returns:
            SkillContent object with full instructions
        """
        # Check cache first
        if skill_name in self._content_cache:
            return self._content_cache[skill_name]
        
        # Get metadata
        if skill_name not in self._metadata_cache:
            raise ValueError(f"Skill not found: {skill_name}")
        
        metadata = self._metadata_cache[skill_name]
        skill_md_path = metadata.path / "SKILL.md"
        
        # Load full content
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract instructions (everything after frontmatter)
        frontmatter_end = content.find("---\n", 4)  # Find second ---
        if frontmatter_end == -1:
            instructions = ""
        else:
            instructions = content[frontmatter_end + 4:].strip()
        
        # Check for optional directories
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
        
        # Cache the result
        self._content_cache[skill_name] = skill_content
        
        return skill_content
    
    def get_metadata(self, skill_name: str) -> Optional[SkillMetadata]:
        """Get cached metadata for a skill."""
        return self._metadata_cache.get(skill_name)
    
    def list_skills(self) -> list[str]:
        """Get list of all discovered skill names."""
        return list(self._metadata_cache.keys())
    
    def clear_cache(self):
        """Clear all caches."""
        self._metadata_cache.clear()
        self._content_cache.clear()
