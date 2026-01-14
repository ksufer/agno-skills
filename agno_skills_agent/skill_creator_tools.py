"""
Skill Creator Tools - Helper functions to create and manage skills.

Provides integration with skill-creator scripts from the skills-examples.
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional


class SkillCreatorTools:
    """Tools for creating and managing skills."""
    
    def __init__(self, skills_examples_dir: Optional[Path] = None):
        """
        Initialize skill creator tools.
        
        Args:
            skills_examples_dir: Path to skills-examples directory
                                If None, tries to find it relative to current location
        """
        if skills_examples_dir:
            self.skills_examples_dir = Path(skills_examples_dir)
        else:
            # Try to find skills-examples relative to current file
            current_dir = Path(__file__).parent.parent
            self.skills_examples_dir = current_dir / "skills-examples"
        
        self.skill_creator_dir = self.skills_examples_dir / "skills" / "skill-creator"
        self.scripts_dir = self.skill_creator_dir / "scripts"
        
        # Check if skill-creator exists
        if not self.skill_creator_dir.exists():
            print(f"Warning: skill-creator not found at {self.skill_creator_dir}")
    
    def init_skill(self, skill_name: str, output_path: Optional[str] = None) -> str:
        """
        Initialize a new skill using init_skill.py script.
        
        Creates a new skill directory with template SKILL.md and example files.
        
        Args:
            skill_name: Name of the skill to create
            output_path: Directory where skill should be created (optional)
            
        Returns:
            Output from init_skill.py script
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
        Package a skill into a distributable .skill file.
        
        Validates the skill and creates a .skill zip file.
        
        Args:
            skill_path: Path to skill directory
            output_dir: Directory where .skill file should be created (optional)
            
        Returns:
            Output from package_skill.py script
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
        Validate a skill using quick_validate.py script.
        
        Checks if skill follows the Agent Skills specification.
        
        Args:
            skill_path: Path to skill directory
            
        Returns:
            Validation results
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
        """Get help text for init_skill.py."""
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
        """Get help text for package_skill.py."""
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
    Create tool functions for skill creation that can be added to an agent.
    
    Args:
        skills_agent: SkillsAgent instance
        
    Returns:
        List of tool functions
    """
    # Find skills-examples directory
    skills_examples_dir = skills_agent.skills_dir.parent
    creator = SkillCreatorTools(skills_examples_dir)
    
    def create_new_skill(skill_name: str, output_path: Optional[str] = None) -> str:
        """
        Create a new skill with template files.
        
        Initializes a new skill directory with:
        - SKILL.md template with proper frontmatter
        - Example scripts/ directory
        - Example references/ directory
        - Example assets/ directory
        
        Args:
            skill_name: Name for the new skill (lowercase, hyphens for spaces)
            output_path: Where to create the skill (optional, defaults to current directory)
            
        Returns:
            Status message
        """
        return creator.init_skill(skill_name, output_path)
    
    def package_skill_file(skill_path: str, output_dir: Optional[str] = None) -> str:
        """
        Package a skill into a distributable .skill file.
        
        Validates and packages the skill into a .skill zip file that can be shared.
        
        Args:
            skill_path: Path to the skill directory
            output_dir: Where to save the .skill file (optional)
            
        Returns:
            Status message with path to .skill file
        """
        return creator.package_skill(skill_path, output_dir)
    
    def validate_skill_format(skill_path: str) -> str:
        """
        Validate that a skill follows the Agent Skills specification.
        
        Checks:
        - YAML frontmatter format and required fields
        - Skill naming conventions
        - Directory structure
        - File organization
        
        Args:
            skill_path: Path to the skill directory
            
        Returns:
            Validation results
        """
        return creator.validate_skill(skill_path)
    
    return [create_new_skill, package_skill_file, validate_skill_format]
