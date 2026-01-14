"""
Skills Agent - 协调 skill 发现、匹配和执行的主 agent 类。

集成 SkillLoader、SkillMatcher 和 SkillExecutor 来创建一个智能的
agent，可以基于用户请求动态发现和使用 skills。
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
    能够发现、匹配和执行 Agent Skills 的智能 agent。
    
    实现渐进式披露：
    1. 启动时只加载 skill 元数据（每个 skill 约100个token）
    2. 在需要时激活完整的 skill 内容
    3. 动态添加 skill 工具到 agent
    """
    
    def __init__(
        self,
        skills_dir: str | Path,
        model_id: str = "gpt-4o",
        api_key: Optional[str] = None,
        debug: bool = False
    ):
        """
        初始化 Skills Agent。
        
        参数:
            skills_dir: 包含 skill 文件夹的目录路径
            model_id: 要使用的 OpenAI 模型 ID
            api_key: OpenAI API 密钥（可选，未提供时使用环境变量）
            debug: 启用调试模式
        """
        self.skills_dir = Path(skills_dir)
        self.debug = debug
        
        # 初始化组件
        self.skill_loader = SkillLoader()
        self.skill_executor = SkillExecutor()
        self.skill_matcher = SkillMatcher()
        
        # 发现可用的 skills（仅元数据）
        print(f"Discovering skills in {self.skills_dir}...")
        self.skills_metadata = self.skill_loader.discover_skills(self.skills_dir)
        print(f"Found {len(self.skills_metadata)} skills")
        
        # 跟踪已激活的 skills
        self.activated_skills: Dict[str, SkillContent] = {}
        
        # 创建基础 Agno agent
        model_kwargs = {"id": model_id}
        if api_key:
            model_kwargs["api_key"] = api_key
        
        self.agent = Agent(
            model=OpenAIChat(**model_kwargs),
            instructions=self._build_instructions(),
            markdown=True,
            debug_mode=debug,
        )
        
        # 添加 skill 管理工具
        self._add_skill_management_tools()
    
    def _build_instructions(self) -> str:
        """
        构建包含可用 skills 元数据的 agent 指令。
        
        使用渐进式披露：只包含 skill 名称和描述，
        不包含完整内容。
        
        返回:
            格式化的指令字符串
        """
        instructions = """You are an intelligent agent with access to specialized skills.

Skills are modular capabilities that provide specialized knowledge, workflows, and tools.
You can activate skills when needed to help users accomplish tasks.

"""
        # 添加可用的 skills 元数据
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
        """向 agent 添加管理 skills 的工具。"""
        
        def activate_skill(skill_name: str) -> str:
            """
            激活 skill 以访问其工具和指令。
            
            激活后，你将可以访问 skill 的：
            - Scripts（作为可调用工具）
            - References（文档）
            - Assets（资源）
            
            参数:
                skill_name: 要激活的 skill 名称
                
            返回:
                包含可用工具的状态消息
            """
            return self.activate_skill(skill_name)
        
        def list_skills() -> str:
            """
            列出所有可用的 skills 及其描述。
            
            返回:
                格式化的 skills 列表
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
            获取特定 skill 的详细信息。
            
            参数:
                skill_name: skill 名称
                
            返回:
                包含指令的 skill 信息（如果已激活）
            """
            # 查找 skill（不区分大小写）
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
            
            # 如果已激活，包含指令
            if actual_name in self.activated_skills:
                skill_content = self.activated_skills[actual_name]
                info.append("\n## Instructions\n")
                info.append(skill_content.instructions)
            else:
                info.append("\n*Skill not activated. Call activate_skill to access full instructions and tools.*")
            
            return "\n".join(info)
        
        def suggest_skills(user_query: str) -> str:
            """
            为用户查询推荐相关的 skills。
            
            参数:
                user_query: 用户的问题或请求
                
            返回:
                推荐的 skills 列表
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
        
        # 将工具添加到 agent
        self.agent.add_tool(activate_skill)
        self.agent.add_tool(list_skills)
        self.agent.add_tool(get_skill_info)
        self.agent.add_tool(suggest_skills)
    
    def activate_skill(self, skill_name: str) -> str:
        """
        激活 skill 并将其工具添加到 agent。
        
        这实现了渐进式披露的第二阶段：
        加载完整的 skill 内容并创建工具。
        
        参数:
            skill_name: 要激活的 skill 名称
            
        返回:
            状态消息
        """
        # 查找精确的 skill 名称（不区分大小写）
        actual_name = self.skill_matcher.find_exact_skill(
            skill_name,
            self.skills_metadata
        )
        
        if not actual_name:
            return f"Skill '{skill_name}' not found. Use list_skills to see available skills."
        
        # 检查是否已激活
        if actual_name in self.activated_skills:
            return f"Skill '{actual_name}' is already activated."
        
        try:
            # 加载完整的 skill 内容
            if self.debug:
                print(f"Loading full content for skill: {actual_name}")
            
            skill_content = self.skill_loader.load_full_skill(actual_name)
            
            # 从 skill 资源创建工具
            tools = self.skill_executor.create_agno_tools(skill_content)
            
            # 将工具添加到 agent
            for tool in tools:
                self.agent.add_tool(tool)
            
            # 标记为已激活
            self.activated_skills[actual_name] = skill_content
            
            # 构建响应
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
        使用用户消息运行 agent。
        
        agent 将自动：
        1. 分析请求
        2. 匹配并激活相关的 skills
        3. 使用 skill 工具完成任务
        
        参数:
            message: 用户的请求
            stream: 是否流式传输响应
            
        返回:
            Agent 响应
        """
        if stream:
            return self.agent.print_response(message, stream=True)
        else:
            return self.agent.run(message)
    
    def print_response(self, message: str, stream: bool = True):
        """
        运行 agent 并打印响应（便捷方法）。
        
        参数:
            message: 用户的请求
            stream: 是否流式传输响应
        """
        return self.agent.print_response(message, stream=stream)
    
    def get_activated_skills(self) -> list[str]:
        """获取当前已激活的 skill 名称列表。"""
        return list(self.activated_skills.keys())
    
    def clear_activated_skills(self):
        """
        清除所有已激活的 skills 及其工具。
        
        注意：这不会从 agent 中删除工具，
        只是清除激活跟踪。
        """
        self.activated_skills.clear()
    
    def reload_skills(self):
        """
        从文件系统重新加载 skill 元数据。
        
        如果在 agent 初始化后添加或修改了 skills，此方法很有用。
        """
        self.skill_loader.clear_cache()
        self.skills_metadata = self.skill_loader.discover_skills(self.skills_dir)
        
        # 更新 agent 指令
        self.agent.instructions = self._build_instructions()
        
        print(f"Reloaded {len(self.skills_metadata)} skills")
