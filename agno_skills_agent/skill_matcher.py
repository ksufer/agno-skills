"""
Skill Matcher - 智能地将用户请求匹配到合适的 skills。

使用基于 LLM 的匹配来为给定任务选择最相关的 skill(s)。
"""

from typing import Dict, List, Optional
from .skill_loader import SkillMetadata


class SkillMatcher:
    """基于描述将用户查询匹配到相关的 skills。"""
    
    def __init__(self):
        self._match_cache: Dict[str, List[str]] = {}
    
    def match_skills(
        self,
        user_query: str,
        skills: Dict[str, SkillMetadata],
        top_k: int = 3
    ) -> List[str]:
        """
        将用户查询匹配到最相关的 skills。
        
        使用关键词匹配和描述分析来找到
        最有可能帮助用户请求的 skills。
        
        参数:
            user_query: 用户的请求或问题
            skills: 可用 skills 的字典
            top_k: 要返回的最大 skill 数量
            
        返回:
            按相关性排序的 skill 名称列表
        """
        if not skills:
            return []
        
        # 计算相关性分数
        scores = {}
        query_lower = user_query.lower()
        
        for skill_name, metadata in skills.items():
            score = self._calculate_relevance(query_lower, metadata)
            scores[skill_name] = score
        
        # 按分数排序并返回前 k 个
        sorted_skills = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 过滤掉零分的 skills
        relevant_skills = [name for name, score in sorted_skills if score > 0]
        
        return relevant_skills[:top_k]
    
    def _calculate_relevance(self, query: str, metadata: SkillMetadata) -> float:
        """
        计算查询和 skill 之间的相关性分数。
        
        使用简单的关键词匹配和描述分析。
        后续可以添加更复杂的方法（embeddings）。
        
        参数:
            query: 小写的用户查询
            metadata: Skill 元数据
            
        返回:
            相关性分数（越高越相关）
        """
        score = 0.0
        
        # 检查 skill 名称是否出现在查询中
        skill_name_lower = metadata.name.lower()
        if skill_name_lower in query:
            score += 10.0
        
        # 检查描述关键词
        description_lower = metadata.description.lower()
        
        # 分割为单词进行关键词匹配
        query_words = set(query.split())
        description_words = set(description_lower.split())
        
        # 计算匹配的关键词
        matching_words = query_words.intersection(description_words)
        score += len(matching_words) * 1.0
        
        # 匹配常见动作词的加分
        action_words = {
            "create": ["creating", "create", "build", "generate"],
            "test": ["test", "testing", "verify", "check"],
            "analyze": ["analyze", "analysis", "examine"],
            "process": ["process", "processing", "handle"],
            "extract": ["extract", "extraction", "parse"],
            "convert": ["convert", "conversion", "transform"],
            "edit": ["edit", "editing", "modify", "update"],
            "search": ["search", "find", "look"],
            "design": ["design", "designing", "layout"],
        }
        
        for base_action, variants in action_words.items():
            if any(variant in query for variant in variants):
                if any(variant in description_lower for variant in variants):
                    score += 5.0
        
        # 特定 skill 检测
        skill_indicators = {
            "mcp": ["mcp", "model context protocol", "mcp server"],
            "pdf": ["pdf", "document"],
            "excel": ["excel", "xlsx", "spreadsheet"],
            "powerpoint": ["powerpoint", "pptx", "presentation", "slides"],
            "word": ["word", "docx", "document"],
            "web": ["web", "webapp", "website", "browser", "localhost"],
            "skill": ["skill", "create skill", "new skill"],
            "test": ["test", "testing", "playwright"],
            "brand": ["brand", "branding", "guidelines"],
            "design": ["design", "ui", "frontend"],
            "art": ["art", "artistic", "generative"],
            "gif": ["gif", "animation"],
            "slack": ["slack"],
        }
        
        for indicator_key, indicators in skill_indicators.items():
            if any(ind in query for ind in indicators):
                if any(ind in skill_name_lower or ind in description_lower for ind in indicators):
                    score += 8.0
        
        return score
    
    def format_skills_for_prompt(self, skills: Dict[str, SkillMetadata]) -> str:
        """
        格式化 skills 元数据以包含在 agent 提示中。
        
        创建 XML 格式的可用 skills 列表，agent
        可以用它来了解有哪些可用能力。
        
        参数:
            skills: skill 元数据字典
            
        返回:
            描述可用 skills 的 XML 格式字符串
        """
        if not skills:
            return "<available_skills>\nNo skills available.\n</available_skills>"
        
        lines = ["<available_skills>"]
        lines.append("The following skills are available. To use a skill, call the activate_skill tool with the skill name.")
        lines.append("")
        
        for skill_name, metadata in skills.items():
            lines.append(f"<skill>")
            lines.append(f"  <name>{metadata.name}</name>")
            lines.append(f"  <description>{metadata.description}</description>")
            if metadata.license:
                lines.append(f"  <license>{metadata.license}</license>")
            lines.append(f"</skill>")
            lines.append("")
        
        lines.append("</available_skills>")
        
        return "\n".join(lines)
    
    def get_skill_summary(self, metadata: SkillMetadata) -> str:
        """
        获取 skill 的简要摘要。
        
        参数:
            metadata: Skill 元数据
            
        返回:
            格式化的摘要字符串
        """
        summary = f"**{metadata.name}**\n"
        summary += f"{metadata.description}\n"
        if metadata.license:
            summary += f"License: {metadata.license}\n"
        return summary
    
    def find_exact_skill(self, skill_name: str, skills: Dict[str, SkillMetadata]) -> Optional[str]:
        """
        通过精确名称匹配查找 skill（不区分大小写）。
        
        参数:
            skill_name: 要搜索的名称
            skills: 可用 skills 的字典
            
        返回:
            如果找到返回精确的 skill 名称，否则返回 None
        """
        skill_name_lower = skill_name.lower()
        
        for name in skills.keys():
            if name.lower() == skill_name_lower:
                return name
        
        return None
    
    def clear_cache(self):
        """清除匹配缓存。"""
        self._match_cache.clear()
