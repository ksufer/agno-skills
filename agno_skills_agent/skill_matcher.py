"""
Skill Matcher - Intelligently matches user requests to appropriate skills.

Uses LLM-based matching to select the most relevant skill(s) for a given task.
"""

from typing import Dict, List, Optional
from .skill_loader import SkillMetadata


class SkillMatcher:
    """Matches user queries to relevant skills based on descriptions."""
    
    def __init__(self):
        self._match_cache: Dict[str, List[str]] = {}
    
    def match_skills(
        self,
        user_query: str,
        skills: Dict[str, SkillMetadata],
        top_k: int = 3
    ) -> List[str]:
        """
        Match user query to most relevant skills.
        
        Uses keyword matching and description analysis to find skills
        that are most likely to help with the user's request.
        
        Args:
            user_query: User's request or question
            skills: Dictionary of available skills
            top_k: Maximum number of skills to return
            
        Returns:
            List of skill names, ordered by relevance
        """
        if not skills:
            return []
        
        # Calculate relevance scores
        scores = {}
        query_lower = user_query.lower()
        
        for skill_name, metadata in skills.items():
            score = self._calculate_relevance(query_lower, metadata)
            scores[skill_name] = score
        
        # Sort by score and return top k
        sorted_skills = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Filter out skills with zero score
        relevant_skills = [name for name, score in sorted_skills if score > 0]
        
        return relevant_skills[:top_k]
    
    def _calculate_relevance(self, query: str, metadata: SkillMetadata) -> float:
        """
        Calculate relevance score between query and skill.
        
        Uses simple keyword matching and description analysis.
        More sophisticated approaches (embeddings) can be added later.
        
        Args:
            query: Lowercased user query
            metadata: Skill metadata
            
        Returns:
            Relevance score (higher is more relevant)
        """
        score = 0.0
        
        # Check if skill name appears in query
        skill_name_lower = metadata.name.lower()
        if skill_name_lower in query:
            score += 10.0
        
        # Check description keywords
        description_lower = metadata.description.lower()
        
        # Split into words for keyword matching
        query_words = set(query.split())
        description_words = set(description_lower.split())
        
        # Count matching keywords
        matching_words = query_words.intersection(description_words)
        score += len(matching_words) * 1.0
        
        # Bonus for matching common action words
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
        
        # Specific skill detection
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
        Format skills metadata for inclusion in agent prompt.
        
        Creates XML-formatted list of available skills that the agent
        can use to understand what capabilities are available.
        
        Args:
            skills: Dictionary of skill metadata
            
        Returns:
            XML-formatted string describing available skills
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
        Get a brief summary of a skill.
        
        Args:
            metadata: Skill metadata
            
        Returns:
            Formatted summary string
        """
        summary = f"**{metadata.name}**\n"
        summary += f"{metadata.description}\n"
        if metadata.license:
            summary += f"License: {metadata.license}\n"
        return summary
    
    def find_exact_skill(self, skill_name: str, skills: Dict[str, SkillMetadata]) -> Optional[str]:
        """
        Find skill by exact name match (case-insensitive).
        
        Args:
            skill_name: Name to search for
            skills: Dictionary of available skills
            
        Returns:
            Exact skill name if found, None otherwise
        """
        skill_name_lower = skill_name.lower()
        
        for name in skills.keys():
            if name.lower() == skill_name_lower:
                return name
        
        return None
    
    def clear_cache(self):
        """Clear matching cache."""
        self._match_cache.clear()
