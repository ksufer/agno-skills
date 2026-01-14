"""
Create Skill Example - Demonstrates skill creation capabilities.

This example shows how to:
1. Use the agent to create a new skill
2. Validate skill structure
3. Package a skill for distribution
"""

import os
from pathlib import Path
from agno_skills_agent import SkillsAgent, create_skill_creator_tools

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def main():
    """Run skill creation examples."""
    
    print("=" * 60)
    print("Agno Skills Agent - Skill Creation Example")
    print("=" * 60)
    print()
    
    # Initialize the Skills Agent
    skills_dir = Path(__file__).parent.parent / "skills-examples" / "skills"
    
    if not skills_dir.exists():
        print(f"Error: Skills directory not found at {skills_dir}")
        return
    
    print("Initializing Skills Agent with skill creation tools...")
    agent = SkillsAgent(
        skills_dir=skills_dir,
        model_id="gpt-4o",
        debug=True
    )
    
    # Add skill creator tools
    creator_tools = create_skill_creator_tools(agent)
    for tool in creator_tools:
        agent.agent.add_tool(tool)
    
    print(f"Added {len(creator_tools)} skill creation tools")
    print()
    
    # Example 1: Activate skill-creator skill
    print("=" * 60)
    print("Example 1: Activate skill-creator Skill")
    print("=" * 60)
    agent.print_response("激活 skill-creator skill，我想学习如何创建 skills")
    print()
    
    # Example 2: Get guidance on creating a skill
    print("=" * 60)
    print("Example 2: Get Skill Creation Guidance")
    print("=" * 60)
    agent.print_response(
        "我想创建一个处理 CSV 文件的 skill。"
        "这个 skill 应该能够：\n"
        "1. 读取 CSV 文件\n"
        "2. 过滤和转换数据\n"
        "3. 导出处理后的结果\n\n"
        "请给我创建这个 skill 的完整指导。"
    )
    print()
    
    # Example 3: Interactive skill creation
    print("=" * 60)
    print("Example 3: Interactive Skill Creation")
    print("=" * 60)
    print("Note: This will actually create a new skill directory!")
    print()
    
    # Uncomment to actually create a skill
    # agent.print_response(
    #     "使用 create_new_skill 工具创建一个名为 'csv-processor' 的新 skill。"
    #     "将它创建在当前目录的 'my_skills' 文件夹中。"
    # )
    
    print("Skipping actual skill creation in this example.")
    print("To create a skill, uncomment the code above.")
    print()
    
    # Example 4: Understanding skill structure
    print("=" * 60)
    print("Example 4: Understanding Skill Structure")
    print("=" * 60)
    agent.print_response(
        "解释一下 Agent Skills 的目录结构。"
        "SKILL.md、scripts/、references/ 和 assets/ 分别是做什么用的？"
    )
    print()
    
    # Example 5: Best practices
    print("=" * 60)
    print("Example 5: Skill Creation Best Practices")
    print("=" * 60)
    agent.print_response(
        "创建一个高质量的 skill 需要注意什么？"
        "有哪些最佳实践和常见错误需要避免？"
    )
    print()


if __name__ == "__main__":
    main()
