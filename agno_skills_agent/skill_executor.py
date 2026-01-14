"""
Skill Executor - Converts skill resources into executable Agno tools.

Handles dynamic loading of scripts, references, and assets from skills.
"""

import sys
import importlib.util
import subprocess
from pathlib import Path
from typing import Callable, List, Dict, Any, Optional
from .skill_loader import SkillContent


class SkillExecutor:
    """Executes skill resources and converts them to Agno-compatible tools."""
    
    def __init__(self):
        self._loaded_scripts: Dict[str, List[Callable]] = {}
        self._loaded_references: Dict[str, str] = {}
    
    def create_agno_tools(self, skill_content: SkillContent) -> List[Callable]:
        """
        Create Agno-compatible tool functions from skill resources.
        
        Converts skill scripts into callable functions that can be added
        to an Agno agent as tools.
        
        Args:
            skill_content: Full skill content with paths to resources
            
        Returns:
            List of callable functions to use as Agno tools
        """
        tools = []
        skill_name = skill_content.metadata.name
        
        # Load scripts if available
        if skill_content.scripts_dir:
            script_tools = self.load_skill_scripts(skill_content.scripts_dir, skill_name)
            tools.extend(script_tools)
        
        # Create a tool to access references if available
        if skill_content.references_dir:
            reference_tool = self._create_reference_accessor(
                skill_content.references_dir,
                skill_name
            )
            tools.append(reference_tool)
        
        # Create a tool to access assets if available
        if skill_content.assets_dir:
            assets_tool = self._create_assets_accessor(
                skill_content.assets_dir,
                skill_name
            )
            tools.append(assets_tool)
        
        return tools
    
    def load_skill_scripts(self, scripts_dir: Path, skill_name: str) -> List[Callable]:
        """
        Load Python scripts from skill's scripts directory.
        
        Dynamically imports Python files and creates wrapper functions
        that can be used as Agno tools.
        
        Args:
            scripts_dir: Path to scripts directory
            skill_name: Name of the skill (for namespacing)
            
        Returns:
            List of callable wrapper functions
        """
        if skill_name in self._loaded_scripts:
            return self._loaded_scripts[skill_name]
        
        tools = []
        
        # Find all Python files
        python_files = list(scripts_dir.glob("*.py"))
        
        for script_path in python_files:
            # Skip __init__.py and private files
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
        Create a wrapper function that runs a Python script.
        
        Instead of importing the script (which may have complex dependencies),
        we create a function that runs it as a subprocess.
        
        Args:
            script_path: Path to Python script
            skill_name: Name of the skill
            
        Returns:
            Callable wrapper function
        """
        script_name = script_path.stem
        
        def run_script(*args, **kwargs) -> str:
            """
            Run the skill script with provided arguments.
            
            Args:
                *args: Positional arguments passed to script
                **kwargs: Keyword arguments passed as --key=value
                
            Returns:
                Script output as string
            """
            cmd = [sys.executable, str(script_path)]
            
            # Add positional args
            for arg in args:
                cmd.append(str(arg))
            
            # Add keyword args as --key=value
            for key, value in kwargs.items():
                cmd.append(f"--{key}={value}")
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    cwd=script_path.parent
                )
                
                if result.returncode != 0:
                    return f"Error running script: {result.stderr}"
                
                return result.stdout
                
            except subprocess.TimeoutExpired:
                return "Error: Script execution timed out (5 minutes)"
            except Exception as e:
                return f"Error: {str(e)}"
        
        # Set function metadata for Agno
        run_script.__name__ = f"{skill_name}_{script_name}"
        run_script.__doc__ = f"Run {script_name} script from {skill_name} skill. Use --help flag to see script usage."
        
        return run_script
    
    def _create_reference_accessor(self, references_dir: Path, skill_name: str) -> Callable:
        """
        Create a tool function to access reference documentation.
        
        Args:
            references_dir: Path to references directory
            skill_name: Name of the skill
            
        Returns:
            Callable function to read reference files
        """
        def read_reference(filename: str) -> str:
            """
            Read a reference file from the skill's references directory.
            
            Args:
                filename: Name of the reference file (e.g., 'finance.md', 'REFERENCE.md')
                
            Returns:
                Content of the reference file
            """
            ref_path = references_dir / filename
            
            if not ref_path.exists():
                # List available references
                available = [f.name for f in references_dir.iterdir() if f.is_file()]
                return f"Reference file '{filename}' not found. Available references: {', '.join(available)}"
            
            try:
                with open(ref_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content
            except Exception as e:
                return f"Error reading reference: {str(e)}"
        
        read_reference.__name__ = f"{skill_name}_read_reference"
        read_reference.__doc__ = f"Read reference documentation from {skill_name} skill. Provide the filename to read."
        
        return read_reference
    
    def _create_assets_accessor(self, assets_dir: Path, skill_name: str) -> Callable:
        """
        Create a tool function to list and access assets.
        
        Args:
            assets_dir: Path to assets directory
            skill_name: Name of the skill
            
        Returns:
            Callable function to work with assets
        """
        def list_assets(pattern: str = "*") -> str:
            """
            List assets available in the skill's assets directory.
            
            Args:
                pattern: Glob pattern to filter assets (default: "*" for all)
                
            Returns:
                List of asset files and their paths
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
        list_assets.__doc__ = f"List asset files from {skill_name} skill. Provide a glob pattern to filter (optional)."
        
        return list_assets
    
    def load_skill_references(self, references_dir: Path, skill_name: str) -> str:
        """
        Load all reference content as a single string.
        
        Useful for adding references to agent context or knowledge base.
        
        Args:
            references_dir: Path to references directory
            skill_name: Name of the skill
            
        Returns:
            Combined content of all reference files
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
        Get help text from a script by running it with --help flag.
        
        Args:
            script_path: Path to the script
            
        Returns:
            Help text output
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
        """Clear all cached scripts and references."""
        self._loaded_scripts.clear()
        self._loaded_references.clear()
