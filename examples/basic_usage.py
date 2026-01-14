"""
Basic Usage Example - Demonstrates core functionality of Skills Agent.

This example shows how to:
1. Initialize the Skills Agent
2. List available skills
3. Let the agent automatically match and activate skills
4. Use skill tools to accomplish tasks
"""

import os
from pathlib import Path
from agno_skills_agent import SkillsAgent

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def main():
    """Run basic usage examples."""
    
    print("=" * 60)
    print("Agno Skills Agent - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Initialize the Skills Agent
    # Point it to the skills-examples/skills directory
    skills_dir = Path(__file__).parent.parent / "skills-examples" / "skills"
    
    if not skills_dir.exists():
        print(f"Error: Skills directory not found at {skills_dir}")
        print("Please ensure skills-examples directory exists in the project root.")
        return
    
    print("Initializing Skills Agent...")
    agent = SkillsAgent(
        skills_dir=skills_dir,
        model_id="gpt-4o",
        debug=True  # Show tool calls for learning
    )
    print()
    
    # Example 1: List all available skills
    print("=" * 60)
    print("Example 1: List Available Skills")
    print("=" * 60)
    agent.print_response("请列出所有可用的 skills")
    print()
    
    # Example 2: Get information about a specific skill
    print("=" * 60)
    print("Example 2: Get Skill Information")
    print("=" * 60)
    agent.print_response("告诉我 mcp-builder skill 是做什么的")
    print()
    
    # Example 3: Let agent suggest skills for a task
    print("=" * 60)
    print("Example 3: Suggest Skills for Task")
    print("=" * 60)
    agent.print_response("我想创建一个新的 MCP server，你推荐哪些 skills？")
    print()
    
    # Example 4: Automatic skill activation and usage
    print("=" * 60)
    print("Example 4: Automatic Skill Activation")
    print("=" * 60)
    agent.print_response(
        "我想了解如何创建一个高质量的 MCP server。"
        "请激活相关的 skill 并给我详细的指导。"
    )
    print()
    
    # Example 5: Multiple skills for complex task
    print("=" * 60)
    print("Example 5: Using Multiple Skills")
    print("=" * 60)
    agent.print_response(
        "我想创建一个新的 skill 来处理 JSON 数据。"
        "请帮我完成这个任务。"
    )
    print()
    
    # Show activated skills
    print("=" * 60)
    print("Activated Skills Summary")
    print("=" * 60)
    activated = agent.get_activated_skills()
    if activated:
        print(f"Total activated skills: {len(activated)}")
        for skill_name in activated:
            print(f"  - {skill_name}")
    else:
        print("No skills were activated.")
    print()


if __name__ == "__main__":
    main()
