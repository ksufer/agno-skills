# Agno Skills Agent

一个能够自动发现、匹配和执行 Agent Skills 的智能体系统，基于 [Agno](https://docs.agno.com) 框架和 [Agent Skills 规范](https://agentskills.io)。

## 特性

- **渐进式披露**：初始只加载 skill 元数据，激活时才加载完整内容，优化上下文使用
- **智能匹配**：根据用户请求自动匹配和激活相关的 skills
- **动态工具管理**：运行时动态添加 skill 工具到 agent
- **脚本执行**：自动将 skill 脚本转换为可调用的 Agno 工具
- **知识整合**：支持加载 skill 的 references 文档作为知识库
- **Skill 创建**：集成 skill-creator 功能，支持创建新的 skills

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置 API 密钥

```bash
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

Windows PowerShell:
```powershell
$env:DASHSCOPE_API_KEY="your-dashscope-api-key"
```

### 基础使用

```python
from pathlib import Path
from agno_skills_agent import SkillsAgent

# 初始化 agent，指向 skills 目录
agent = SkillsAgent(
    skills_dir="skills-examples/skills",
    model_id="qwen-plus"
)

# Agent 会自动发现、匹配和激活相关的 skills
agent.print_response("帮我创建一个新的 MCP server")
```

### 运行示例

```bash
# 基础使用示例
python examples/basic_usage.py

# Skill 创建示例
python examples/create_skill.py
```

## 架构说明

### 核心组件

```
agno_skills_agent/
├── skill_loader.py       # Skill 发现和元数据加载
├── skill_executor.py     # 脚本执行和工具转换
├── skill_matcher.py      # 智能 skill 匹配
├── skills_agent.py       # 主 Agent 类
└── skill_creator_tools.py # Skill 创建工具
```

### 工作流程

```mermaid
graph TB
    User[用户请求] --> Agent[Skills Agent]
    Agent --> Discover[发现 Skills]
    Discover --> Metadata[加载元数据<br/>name + description]
    Agent --> Match[匹配相关 Skills]
    Match --> Activate[激活 Skill]
    Activate --> LoadFull[加载完整 SKILL.md]
    Activate --> CreateTools[创建 Agno Tools]
    CreateTools --> Scripts[scripts/ → 工具函数]
    CreateTools --> References[references/ → 知识库]
    CreateTools --> Assets[assets/ → 资源访问]
    Agent --> Execute[执行任务]
```

### 渐进式披露

Skills Agent 实现了三级渐进式披露机制：

1. **元数据阶段**（启动时）：只加载 `name` 和 `description`，每个 skill 约 100 tokens
2. **指令阶段**（激活时）：加载完整的 `SKILL.md` 内容和目录信息
3. **资源阶段**（按需）：根据需要加载 scripts、references 和 assets

这种设计确保了：
- 启动快速，context 占用最小
- 只在需要时加载详细内容
- 支持大量 skills 而不影响性能

## API 文档

### SkillsAgent

主要的 agent 类，集成所有功能。

```python
agent = SkillsAgent(
    skills_dir: str | Path,      # Skills 目录路径
    model_id: str = "qwen-plus", # DashScope 模型 ID
    api_key: Optional[str] = None, # API key（可选）
    debug: bool = False           # 调试模式
)
```

**方法**：

- `run(message: str) -> Any`：运行 agent 处理用户消息
- `print_response(message: str, stream: bool = True)`：打印 agent 响应
- `activate_skill(skill_name: str) -> str`：手动激活指定 skill
- `get_activated_skills() -> list[str]`：获取已激活的 skills
- `reload_skills()`：重新加载 skills 元数据

**内置工具**（agent 自动可用）：

- `activate_skill(skill_name)`: 激活一个 skill
- `list_skills()`: 列出所有可用 skills
- `get_skill_info(skill_name)`: 获取 skill 详细信息
- `suggest_skills(user_query)`: 为查询推荐 skills

### SkillLoader

负责发现和加载 skills。

```python
loader = SkillLoader()
skills = loader.discover_skills(Path("skills-examples/skills"))
full_content = loader.load_full_skill("mcp-builder")
```

### SkillExecutor

将 skill 资源转换为可执行工具。

```python
executor = SkillExecutor()
tools = executor.create_agno_tools(skill_content)
```

### SkillMatcher

智能匹配 skills 和用户请求。

```python
matcher = SkillMatcher()
matches = matcher.match_skills("create MCP server", skills_dict)
```

## Skills 示例

本项目包含多个示例 skills（位于 `skills-examples/skills/`）：

- **mcp-builder**: 创建 MCP (Model Context Protocol) servers
- **skill-creator**: 创建新的 Agent Skills
- **webapp-testing**: 使用 Playwright 测试 web 应用
- **pdf**: PDF 文件处理（提取、填充表单等）
- **docx**: Word 文档创建和编辑
- **pptx**: PowerPoint 演示文稿处理
- **xlsx**: Excel 电子表格操作
- 更多 skills...

## 创建自己的 Skill

### 方法 1：使用 Agent

```python
from agno_skills_agent import SkillsAgent, create_skill_creator_tools

agent = SkillsAgent(skills_dir="skills-examples/skills")

# 添加创建工具
tools = create_skill_creator_tools(agent)
for tool in tools:
    agent.agent.add_tool(tool)

# 让 agent 帮你创建
agent.print_response("创建一个处理 JSON 数据的 skill")
```

### 方法 2：手动创建

1. 创建 skill 目录结构：

```
my-skill/
├── SKILL.md          # 必需：元数据和指令
├── scripts/          # 可选：Python 脚本
├── references/       # 可选：参考文档
└── assets/           # 可选：模板和资源
```

2. 编写 `SKILL.md`：

```markdown
---
name: my-skill
description: 简短描述 skill 功能和使用场景
---

# My Skill

## 使用说明

详细的使用指令...

## 示例

示例代码...
```

3. 验证 skill：

```python
from agno_skills_agent import SkillCreatorTools

creator = SkillCreatorTools()
result = creator.validate_skill("path/to/my-skill")
print(result)
```

## 技术栈

- **Agno**: AI agent 框架
- **DashScope**: 阿里云 LLM 模型（Qwen-Plus）
- **Pydantic**: 数据验证
- **PyYAML**: YAML 解析
- **Agent Skills**: Skill 规范标准

## 最佳实践

1. **Skill 命名**：使用小写字母和连字符（如 `my-skill`）
2. **描述清晰**：在 description 中明确说明何时使用该 skill
3. **渐进式披露**：将详细文档放在 references/ 中，保持 SKILL.md 简洁
4. **脚本独立**：确保脚本可以独立运行，添加 `--help` 支持
5. **文档完整**：在 SKILL.md 中提供清晰的使用指导和示例

## 性能考虑

- **元数据缓存**：已发现的 skills 元数据被缓存
- **延迟加载**：只在激活时加载完整内容
- **脚本执行**：使用 subprocess 而不是动态导入，避免依赖冲突
- **Context 优化**：通过渐进式披露最小化 token 使用

## 故障排除

### Skills 未被发现

- 确保 skills 目录路径正确
- 检查每个 skill 文件夹都包含 `SKILL.md`
- 验证 YAML frontmatter 格式正确

### Skill 激活失败

- 检查 SKILL.md 的 YAML frontmatter 是否包含必需字段（name、description）
- 确保 skill 名称匹配目录名称
- 查看错误消息获取详细信息

### 脚本执行失败

- 确保脚本有执行权限
- 检查脚本依赖是否已安装
- 使用 `--help` 查看脚本用法

## 贡献

欢迎提交 issues 和 pull requests！

## 许可证

本项目使用 MIT 许可证。Skills 示例可能有不同的许可证，请查看各自的 LICENSE 文件。

## 相关链接

- [Agno 文档](https://docs.agno.com)
- [Agent Skills 规范](https://agentskills.io)
- [Agent Skills 示例](https://github.com/anthropics/skills)
- [MCP 协议](https://modelcontextprotocol.io)

## 致谢

- [Agno](https://github.com/agno-agi/agno) - AI agent 框架
- [Anthropic](https://www.anthropic.com) - Agent Skills 规范和示例
- [Alibaba Cloud DashScope](https://dashscope.aliyun.com) - 通义千问模型

---

**Built with ❤️ using Agno and Agent Skills**
