"""
创建 Skill 示例 - 演示 skill 创建功能。

此示例展示如何：
1. 使用 agent 创建新的 skill
2. 验证 skill 结构
3. 打包 skill 以供分发
"""

import os
from pathlib import Path
from agno_skills_agent import SkillsAgent, create_skill_creator_tools

# 设置你的 DashScope API 密钥
# os.environ["DASHSCOPE_API_KEY"] = "your-api-key-here"

def main():
    """运行 skill 创建示例。"""
    
    print("=" * 60)
    print("Agno Skills Agent - Skill Creation Example")
    print("=" * 60)
    print()
    
    # 初始化 Skills Agent
    skills_dir = Path(__file__).parent.parent / "skills-examples" / "skills"
    
    if not skills_dir.exists():
        print(f"Error: Skills directory not found at {skills_dir}")
        return
    
    print("Initializing Skills Agent with skill creation tools...")
    agent = SkillsAgent(
        skills_dir=skills_dir,
        model_id="qwen-plus",
        debug=True
    )
    
    # 添加 skill 创建工具
    creator_tools = create_skill_creator_tools(agent)
    for tool in creator_tools:
        agent.agent.add_tool(tool)
    
    print(f"Added {len(creator_tools)} skill creation tools")
    print()
    
    # 示例 1: 激活 skill-creator skill
    print("=" * 60)
    print("Example 1: Activate skill-creator Skill")
    print("=" * 60)
    agent.print_response("激活 skill-creator skill，我想学习如何创建 skills")
    print()
    
    # 示例 2: 获取创建 skill 的指导
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
    
    # 示例 3: 交互式 skill 创建
    print("=" * 60)
    print("Example 3: Interactive Skill Creation")
    print("=" * 60)
    print("Note: This will actually create a new skill directory!")
    print()
    
    # 取消注释以实际创建 skill
    # agent.print_response(
    #     "使用 create_new_skill 工具创建一个名为 'csv-processor' 的新 skill。"
    #     "将它创建在当前目录的 'my_skills' 文件夹中。"
    # )
    
    print("Skipping actual skill creation in this example.")
    print("To create a skill, uncomment the code above.")
    print()
    
    # 示例 4: 理解 skill 结构
    print("=" * 60)
    print("Example 4: Understanding Skill Structure")
    print("=" * 60)
    agent.print_response(
        "解释一下 Agent Skills 的目录结构。"
        "SKILL.md、scripts/、references/ 和 assets/ 分别是做什么用的？"
    )
    print()
    
    # 示例 5: 最佳实践
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
