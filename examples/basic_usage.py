"""
基础使用示例 - 演示 Skills Agent 的核心功能。

此示例展示如何：
1. 初始化 Skills Agent
2. 列出可用的 skills
3. 让 agent 自动匹配和激活 skills
4. 使用 skill 工具完成任务
"""

import os
from pathlib import Path
from agno_skills_agent import SkillsAgent

# 设置你的 DashScope API 密钥
# os.environ["DASHSCOPE_API_KEY"] = "your-api-key-here"

def main():
    """运行基础使用示例。"""
    
    print("=" * 60)
    print("Agno Skills Agent - Basic Usage Example")
    print("=" * 60)
    print()
    
    # 初始化 Skills Agent
    # 指向 skills-examples/skills 目录
    skills_dir = Path(__file__).parent.parent / "skills-examples" / "skills"
    
    if not skills_dir.exists():
        print(f"Error: Skills directory not found at {skills_dir}")
        print("Please ensure skills-examples directory exists in the project root.")
        return
    
    print("Initializing Skills Agent...")
    agent = SkillsAgent(
        skills_dir=skills_dir,
        model_id="qwen-plus",
        debug=True  # 显示工具调用以便学习
    )
    print()
    
    # 示例 1: 列出所有可用的 skills
    print("=" * 60)
    print("Example 1: List Available Skills")
    print("=" * 60)
    agent.print_response("请列出所有可用的 skills")
    print()
    
    # 示例 2: 获取特定 skill 的信息
    print("=" * 60)
    print("Example 2: Get Skill Information")
    print("=" * 60)
    agent.print_response("告诉我 mcp-builder skill 是做什么的")
    print()
    
    # 示例 3: 让 agent 为任务推荐 skills
    print("=" * 60)
    print("Example 3: Suggest Skills for Task")
    print("=" * 60)
    agent.print_response("我想创建一个新的 MCP server，你推荐哪些 skills？")
    print()
    
    # 示例 4: 自动激活和使用 skill
    print("=" * 60)
    print("Example 4: Automatic Skill Activation")
    print("=" * 60)
    agent.print_response(
        "我想了解如何创建一个高质量的 MCP server。"
        "请激活相关的 skill 并给我详细的指导。"
    )
    print()
    
    # 示例 5: 使用多个 skills 完成复杂任务
    print("=" * 60)
    print("Example 5: Using Multiple Skills")
    print("=" * 60)
    agent.print_response(
        "我想创建一个新的 skill 来处理 JSON 数据。"
        "请帮我完成这个任务。"
    )
    print()
    
    # 显示已激活的 skills
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
