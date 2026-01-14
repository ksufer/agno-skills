# DashScope 模型迁移文档

## 概述

本文档记录了将 Agno Skills Agent 项目从 OpenAI 模型迁移到 Alibaba Cloud DashScope（通义千问）模型的过程。

## 修改时间

2026-01-14

## 修改内容

### 1. 代码文件修改

#### 1.1 核心 Agent 类 (`agno_skills_agent/skills_agent.py`)

**修改内容：**
- 导入语句：`from agno.models.openai import OpenAIChat` → `from agno.models.dashscope import DashScope`
- 默认模型 ID：`model_id: str = "gpt-4o"` → `model_id: str = "qwen-plus"`
- 模型实例化：`OpenAIChat(**model_kwargs)` → `DashScope(**model_kwargs)`
- 文档字符串更新：将 "OpenAI" 改为 "DashScope"

**影响范围：**
- 第 11 行：导入语句
- 第 31 行：默认参数
- 第 39-41 行：文档字符串
- 第 66 行：模型实例化

#### 1.2 基础使用示例 (`examples/basic_usage.py`)

**修改内容：**
- API 密钥注释：`OPENAI_API_KEY` → `DASHSCOPE_API_KEY`
- 模型 ID：`model_id="gpt-4o"` → `model_id="qwen-plus"`

**影响范围：**
- 第 15-16 行：API 密钥注释
- 第 38 行：模型 ID 参数

#### 1.3 Skill 创建示例 (`examples/create_skill.py`)

**修改内容：**
- API 密钥注释：`OPENAI_API_KEY` → `DASHSCOPE_API_KEY`
- 模型 ID：`model_id="gpt-4o"` → `model_id="qwen-plus"`

**影响范围：**
- 第 15-16 行：API 密钥注释
- 第 35 行：模型 ID 参数

#### 1.4 测试脚本 (`test_skills_agent.py`)

**修改内容：**
- 注释中的 API 密钥引用：`OPENAI_API_KEY` → `DASHSCOPE_API_KEY`（2 处）

**影响范围：**
- 第 154 行：初始化注释
- 第 187 行：错误提示注释

### 2. 文档文件修改

#### 2.1 README.md

**修改内容：**
- API 密钥设置说明（Bash 和 PowerShell）
- 示例代码中的模型 ID
- API 文档中的默认模型 ID 和注释
- 技术栈说明
- 致谢部分

**修改位置：**
- 第 22-31 行：API 密钥设置
- 第 40-46 行：基础使用示例
- 第 109-114 行：API 文档
- 第 232-238 行：技术栈
- 第 289-294 行：致谢

#### 2.2 PROJECT_SUMMARY.md

**修改内容：**
- 依赖项列表：`openai>=1.0.0` → `dashscope>=1.0.0`
- 致谢部分：OpenAI → Alibaba Cloud DashScope

**修改位置：**
- 第 176-184 行：依赖项
- 第 240-244 行：致谢

### 3. 依赖文件修改

#### 3.1 requirements.txt

**修改内容：**
- 移除 `openai>=1.0.0` 依赖（DashScope 支持已内置在 agno 中）

## 使用 DashScope 模型

### 配置 API 密钥

在使用前需要设置 DashScope API 密钥：

**Linux/macOS:**
```bash
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

**Windows CMD:**
```cmd
set DASHSCOPE_API_KEY=your-dashscope-api-key
```

**Windows PowerShell:**
```powershell
$env:DASHSCOPE_API_KEY="your-dashscope-api-key"
```

### 获取 API 密钥

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 在 API 密钥管理页面创建新的 API Key

### 支持的模型

根据 Agno 文档，DashScope 支持以下模型：

- **qwen-plus**（推荐）：适合大多数使用场景，平衡性能和成本
- **qwen-max**：最强性能，适合复杂任务
- **qwen-turbo**：快速响应，适合简单任务
- **qvq-max**：支持视觉和推理的多模态模型（需要启用 `enable_thinking=True`）
- **qwen-vl-plus**：图像理解模型

### 代码示例

#### 基础使用

```python
from agno.agent import Agent
from agno.models.dashscope import DashScope

agent = Agent(
    model=DashScope(id="qwen-plus", temperature=0.5),
    markdown=True
)

agent.print_response("你好，请介绍一下你自己")
```

#### 带工具的 Agent

```python
from agno.agent import Agent
from agno.models.dashscope import DashScope
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=DashScope(id="qwen-plus"),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

agent.print_response("搜索今天的 AI 新闻")
```

#### 图像分析

```python
from agno.agent import Agent
from agno.media import Image
from agno.models.dashscope import DashScope

agent = Agent(
    model=DashScope(id="qwen-vl-plus"),
    markdown=True,
)

agent.print_response(
    "分析这张图片的内容",
    images=[Image(url="https://example.com/image.jpg")],
    stream=True,
)
```

#### 思维推理模式

```python
from agno.agent import Agent
from agno.models.dashscope import DashScope

agent = Agent(
    model=DashScope(id="qvq-max", enable_thinking=True),
)

agent.print_response(
    "请逐步分析如何解决这个问题...",
    stream=True,
)
```

## 迁移优势

### 1. 成本优化
- DashScope 通义千问模型在中文场景下性能优异
- 价格相比 OpenAI 更具竞争力

### 2. 网络稳定性
- 国内访问更稳定，无需代理
- 响应速度更快

### 3. 合规性
- 符合中国数据安全和隐私保护要求
- 适合需要数据本地化的项目

### 4. 中文优化
- 通义千问在中文理解和生成方面表现优秀
- 更适合中文为主的应用场景

## 兼容性说明

### 代码兼容性
- Agno 框架对不同模型提供统一的 API 接口
- 迁移后代码逻辑无需修改
- 工具调用、流式输出等功能完全兼容

### 功能对比

| 功能 | OpenAI (GPT-4o) | DashScope (Qwen-Plus) |
|------|----------------|----------------------|
| 文本生成 | ✅ | ✅ |
| 工具调用 | ✅ | ✅ |
| 流式输出 | ✅ | ✅ |
| 图像理解 | ✅ (GPT-4o) | ✅ (qwen-vl-plus) |
| 函数调用 | ✅ | ✅ |
| 结构化输出 | ✅ | ✅ |
| 思维链推理 | ✅ | ✅ (qvq-max) |

## 测试验证

所有现有测试应继续通过：

```bash
python test_skills_agent.py
```

预期结果：
```
============================================================
TEST SUMMARY
============================================================
[OK] PASSED: Skill Loader
[OK] PASSED: Skill Matcher
[OK] PASSED: Skill Executor
[OK] PASSED: Skills Agent
[OK] PASSED: Progressive Disclosure

Total: 5/5 tests passed

[SUCCESS] All tests passed!
```

## 回滚方案

如需回滚到 OpenAI 模型，执行以下步骤：

1. 恢复导入语句：
```python
from agno.models.openai import OpenAIChat
```

2. 恢复模型实例化：
```python
model=OpenAIChat(id="gpt-4o")
```

3. 恢复 requirements.txt：
```
openai>=1.0.0
```

4. 设置环境变量：
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

## 参考资料

- [Agno DashScope 文档](https://docs.agno.com/integrations/models/native/dashscope/overview)
- [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
- [通义千问模型介绍](https://help.aliyun.com/zh/dashscope/)
- [Agno 框架文档](https://docs.agno.com/)

## 总结

✅ 成功将所有模型引用从 OpenAI 迁移到 DashScope  
✅ 更新了所有相关文档和示例  
✅ 保持了代码的完整功能和兼容性  
✅ 优化了依赖项配置  

迁移后的系统可以充分利用通义千问模型的优势，特别是在中文场景下的表现。
