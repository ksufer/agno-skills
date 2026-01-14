"""
Skills Agent - Main agent class that orchestrates skill discovery, matching, and execution.

Integrates SkillLoader, SkillMatcher, and SkillExecutor to create an intelligent
agent that can dynamically discover and use skills based on user requests.
"""

from pathlib import Path
from typing import Optional, Dict, Any
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from .skill_loader import SkillLoader, SkillMetadata, SkillContent
from .skill_executor import SkillExecutor
from .skill_matcher import SkillMatcher


class SkillsAgent:
    """
    Intelligent agent that can discover, match, and execute Agent Skills.
    
    Implements progressive disclosure:
    1. Loads only skill metadata at startup (~100 tokens per skill)
    2. Activates full skill content when needed
    3. Dynamically adds skill tools to the agent
    """
    
    def __init__(
        self,
        skills_dir: str | Path,
        model_id: str = "gpt-4o",
        api_key: Optional[str] = None,
        debug: bool = False
    ):
        """
        Initialize the Skills Agent.
        
        Args:
            skills_dir: Path to directory containing skill folders
            model_id: OpenAI model ID to use
            api_key: OpenAI API key (optional, uses env var if not provided)
            debug: Enable debug mode
        """
        self.skills_dir = Path(skills_dir)
        self.debug = debug
        
        # Initialize components
        self.skill_loader = SkillLoader()
        self.skill_executor = SkillExecutor()
        self.skill_matcher = SkillMatcher()
        
        # Discover available skills (metadata only)
        print(f"Discovering skills in {self.skills_dir}...")
        self.skills_metadata = self.skill_loader.discover_skills(self.skills_dir)
        print(f"Found {len(self.skills_metadata)} skills")
        
        # Track activated skills
        self.activated_skills: Dict[str, SkillContent] = {}
        
        # Create base Agno agent
        model_kwargs = {"id": model_id}
        if api_key:
            model_kwargs["api_key"] = api_key
        
        self.agent = Agent(
            model=OpenAIChat(**model_kwargs),
            instructions=self._build_instructions(),
            markdown=True,
            debug_mode=debug,
        )
        
        # Add skill management tools
        self._add_skill_management_tools()
    
    def _build_instructions(self) -> str:
        """
        Build agent instructions including available skills metadata.
        
        Uses progressive disclosure: only includes skill names and descriptions,
        not full content.
        
        Returns:
            Formatted instructions string
        """
        instructions = """You are an intelligent agent with access to specialized skills.

Skills are modular capabilities that provide specialized knowledge, workflows, and tools.
You can activate skills when needed to help users accomplish tasks.

"""
        # Add available skills metadata
        skills_xml = self.skill_matcher.format_skills_for_prompt(self.skills_metadata)
        instructions += skills_xml
        
        instructions += """

When a user's request matches a skill's description:
1. Call activate_skill with the skill name
2. Use the newly available tools from that skill
3. Follow the skill's instructions to complete the task

You can activate multiple skills if needed for complex tasks.
"""
        return instructions
    
    def _add_skill_management_tools(self):
        """Add tools for managing skills to the agent."""
        
        def activate_skill(skill_name: str) -> str:
            """
            Activate a skill to access its tools and instructions.
            
            After activation, you will have access to the skill's:
            - Scripts (as callable tools)
            - References (documentation)
            - Assets (resources)
            
            Args:
                skill_name: Name of the skill to activate
                
            Returns:
                Status message with available tools
            """
            return self.activate_skill(skill_name)
        
        def list_skills() -> str:
            """
            List all available skills with their descriptions.
            
            Returns:
                Formatted list of skills
            """
            if not self.skills_metadata:
                return "No skills available."
            
            result = ["Available Skills:\n"]
            for name, metadata in self.skills_metadata.items():
                activated = " [ACTIVATED]" if name in self.activated_skills else ""
                result.append(f"- **{name}**{activated}")
                result.append(f"  {metadata.description}")
                result.append("")
            
            return "\n".join(result)
        
        def get_skill_info(skill_name: str) -> str:
            """
            Get detailed information about a specific skill.
            
            Args:
                skill_name: Name of the skill
                
            Returns:
                Skill information including instructions if activated
            """
            # Find skill (case-insensitive)
            actual_name = self.skill_matcher.find_exact_skill(
                skill_name,
                self.skills_metadata
            )
            
            if not actual_name:
                return f"Skill '{skill_name}' not found. Use list_skills to see available skills."
            
            metadata = self.skills_metadata[actual_name]
            info = [f"# {metadata.name}\n"]
            info.append(f"**Description:** {metadata.description}\n")
            
            if metadata.license:
                info.append(f"**License:** {metadata.license}\n")
            
            # If activated, include instructions
            if actual_name in self.activated_skills:
                skill_content = self.activated_skills[actual_name]
                info.append("\n## Instructions\n")
                info.append(skill_content.instructions)
            else:
                info.append("\n*Skill not activated. Call activate_skill to access full instructions and tools.*")
            
            return "\n".join(info)
        
        def suggest_skills(user_query: str) -> str:
            """
            Suggest relevant skills for a user query.
            
            Args:
                user_query: User's question or request
                
            Returns:
                List of suggested skills
            """
            suggestions = self.skill_matcher.match_skills(
                user_query,
                self.skills_metadata,
                top_k=3
            )
            
            if not suggestions:
                return "No relevant skills found for this query."
            
            result = ["Suggested skills:\n"]
            for skill_name in suggestions:
                metadata = self.skills_metadata[skill_name]
                result.append(f"- **{skill_name}**")
                result.append(f"  {metadata.description}")
                result.append("")
            
            return "\n".join(result)
        
        # Add tools to agent
        self.agent.add_tool(activate_skill)
        self.agent.add_tool(list_skills)
        self.agent.add_tool(get_skill_info)
        self.agent.add_tool(suggest_skills)
    
    def activate_skill(self, skill_name: str) -> str:
        """
        Activate a skill and add its tools to the agent.
        
        This implements the second stage of progressive disclosure:
        loads full skill content and creates tools.
        
        Args:
            skill_name: Name of skill to activate
            
        Returns:
            Status message
        """
        # Find exact skill name (case-insensitive)
        actual_name = self.skill_matcher.find_exact_skill(
            skill_name,
            self.skills_metadata
        )
        
        if not actual_name:
            return f"Skill '{skill_name}' not found. Use list_skills to see available skills."
        
        # Check if already activated
        if actual_name in self.activated_skills:
            return f"Skill '{actual_name}' is already activated."
        
        try:
            # Load full skill content
            if self.debug:
                print(f"Loading full content for skill: {actual_name}")
            
            skill_content = self.skill_loader.load_full_skill(actual_name)
            
            # Create tools from skill resources
            tools = self.skill_executor.create_agno_tools(skill_content)
            
            # Add tools to agent
            for tool in tools:
                self.agent.add_tool(tool)
            
            # Mark as activated
            self.activated_skills[actual_name] = skill_content
            
            # Build response
            response = [f"✓ Activated skill: {actual_name}\n"]
            response.append(f"**Description:** {skill_content.metadata.description}\n")
            
            if tools:
                response.append(f"\n**Available tools:** {len(tools)}")
                for tool in tools:
                    response.append(f"- {tool.__name__}")
            
            response.append(f"\n**Instructions:**\n{skill_content.instructions[:500]}...")
            
            return "\n".join(response)
            
        except Exception as e:
            return f"Error activating skill '{actual_name}': {str(e)}"
    
    def run(self, message: str, stream: bool = False) -> Any:
        """
        Run the agent with a user message.
        
        The agent will automatically:
        1. Analyze the request
        2. Match and activate relevant skills
        3. Use skill tools to complete the task
        
        Args:
            message: User's request
            stream: Whether to stream the response
            
        Returns:
            Agent response
        """
        if stream:
            return self.agent.print_response(message, stream=True)
        else:
            return self.agent.run(message)
    
    def print_response(self, message: str, stream: bool = True):
        """
        Run agent and print response (convenience method).
        
        Args:
            message: User's request
            stream: Whether to stream the response
        """
        return self.agent.print_response(message, stream=stream)
    
    def get_activated_skills(self) -> list[str]:
        """Get list of currently activated skill names."""
        return list(self.activated_skills.keys())
    
    def clear_activated_skills(self):
        """
        Clear all activated skills and their tools.
        
        Note: This does not remove tools from the agent,
        only clears the activation tracking.
        """
        self.activated_skills.clear()
    
    def reload_skills(self):
        """
        Reload skill metadata from filesystem.
        
        Useful if skills were added or modified after agent initialization.
        """
        self.skill_loader.clear_cache()
        self.skills_metadata = self.skill_loader.discover_skills(self.skills_dir)
        
        # Update agent instructions
        self.agent.instructions = self._build_instructions()
        
        print(f"Reloaded {len(self.skills_metadata)} skills")
