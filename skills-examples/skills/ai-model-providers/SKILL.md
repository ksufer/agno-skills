---
name: ai-model-providers
description: 生成支持OpenAI、OpenRouter、DashScope、GLM、Ollama等多个AI模型提供商的统一Python接口。自动生成.env.example配置文件和使用python-dotenv的代码。当用户需要接入AI大模型、创建智能体接口、多提供商支持或配置环境变量时使用。
---

# AI 模型提供商接口生成器

## 概述

自动生成支持多个AI模型提供商的统一Python接口,包括配置管理和环境变量模板。

## 支持的提供商

- **OpenAI**: GPT系列模型
- **OpenRouter**: 多模型聚合平台
- **DashScope**: 阿里云通义千问
- **GLM**: 智谱AI (ChatGLM)
- **Ollama**: 本地模型部署

## 生成工作流

### 步骤 1: 创建统一接口类

生成 `ai_client.py` 文件,包含:

```python
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class AIModelClient:
    """统一的AI模型客户端接口"""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider.lower()
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """根据提供商初始化对应的客户端"""
        if self.provider == "openai":
            return self._init_openai()
        elif self.provider == "openrouter":
            return self._init_openrouter()
        elif self.provider == "dashscope":
            return self._init_dashscope()
        elif self.provider == "glm":
            return self._init_glm()
        elif self.provider == "ollama":
            return self._init_ollama()
        else:
            raise ValueError(f"不支持的提供商: {self.provider}")
    
    def _init_openai(self):
        """初始化OpenAI客户端"""
        from openai import OpenAI
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
    
    def _init_openrouter(self):
        """初始化OpenRouter客户端"""
        from openai import OpenAI
        return OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
    
    def _init_dashscope(self):
        """初始化DashScope客户端"""
        import dashscope
        dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
        return dashscope
    
    def _init_glm(self):
        """初始化GLM客户端"""
        from zhipuai import ZhipuAI
        return ZhipuAI(api_key=os.getenv("GLM_API_KEY"))
    
    def _init_ollama(self):
        """初始化Ollama客户端"""
        from ollama import Client
        return Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    
    def chat(self, messages: list, model: Optional[str] = None, **kwargs) -> str:
        """统一的对话接口"""
        if self.provider in ["openai", "openrouter"]:
            return self._chat_openai_compatible(messages, model, **kwargs)
        elif self.provider == "dashscope":
            return self._chat_dashscope(messages, model, **kwargs)
        elif self.provider == "glm":
            return self._chat_glm(messages, model, **kwargs)
        elif self.provider == "ollama":
            return self._chat_ollama(messages, model, **kwargs)
    
    def _chat_openai_compatible(self, messages: list, model: Optional[str], **kwargs) -> str:
        """OpenAI兼容接口"""
        if model is None:
            model = os.getenv(f"{self.provider.upper()}_MODEL", "gpt-3.5-turbo")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    def _chat_dashscope(self, messages: list, model: Optional[str], **kwargs) -> str:
        """DashScope接口"""
        from dashscope import Generation
        if model is None:
            model = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
        
        response = Generation.call(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.output.text
    
    def _chat_glm(self, messages: list, model: Optional[str], **kwargs) -> str:
        """GLM接口"""
        if model is None:
            model = os.getenv("GLM_MODEL", "glm-4")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    def _chat_ollama(self, messages: list, model: Optional[str], **kwargs) -> str:
        """Ollama接口"""
        if model is None:
            model = os.getenv("OLLAMA_MODEL", "llama2")
        
        response = self.client.chat(
            model=model,
            messages=messages,
            **kwargs
        )
        return response['message']['content']
```

### 步骤 2: 生成环境变量模板

创建 `.env.example` 文件:

```bash
# OpenAI 配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# OpenRouter 配置
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# DashScope (阿里云通义千问) 配置
DASHSCOPE_API_KEY=your_dashscope_api_key_here
DASHSCOPE_MODEL=qwen-turbo

# GLM (智谱AI) 配置
GLM_API_KEY=your_glm_api_key_here
GLM_MODEL=glm-4

# Ollama 配置
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

# 默认提供商 (openai/openrouter/dashscope/glm/ollama)
DEFAULT_PROVIDER=openai
```

### 步骤 3: 生成使用示例

创建 `example_usage.py`:

```python
from ai_client import AIModelClient

# 使用默认提供商 (从环境变量读取)
client = AIModelClient()

# 或指定提供商
client_openai = AIModelClient(provider="openai")
client_glm = AIModelClient(provider="glm")

# 发送对话
messages = [
    {"role": "user", "content": "你好,请介绍一下你自己"}
]

response = client.chat(messages)
print(response)

# 使用特定模型
response = client.chat(messages, model="gpt-4")
print(response)
```

### 步骤 4: 生成依赖文件

创建 `requirements.txt`:

```
python-dotenv>=1.0.0
openai>=1.0.0
dashscope>=1.14.0
zhipuai>=2.0.0
ollama>=0.1.0
```

## 使用说明

1. **生成文件**: 按照上述步骤生成所有必要文件
2. **配置环境**: 复制 `.env.example` 为 `.env` 并填入实际的API密钥
3. **安装依赖**: `pip install -r requirements.txt`
4. **使用接口**: 参考 `example_usage.py` 调用统一接口

## 错误处理建议

在生成的代码中添加错误处理:

```python
try:
    response = client.chat(messages)
except Exception as e:
    print(f"调用{client.provider}时出错: {str(e)}")
```

## 扩展提供商

添加新提供商时:
1. 在 `_initialize_client` 中添加新的条件分支
2. 实现对应的 `_init_xxx` 方法
3. 实现对应的 `_chat_xxx` 方法
4. 在 `.env.example` 中添加配置项

## 最佳实践

- **密钥安全**: 永远不要将 `.env` 文件提交到版本控制
- **降级策略**: 实现提供商降级逻辑,主提供商失败时自动切换
- **速率限制**: 根据各提供商的限制实现请求队列
- **日志记录**: 记录每次API调用的提供商、模型和耗时
- **缓存机制**: 对相同请求实现缓存以节省成本

## 提供商参考信息

详细的API文档和参数说明见 [provider-reference.md](provider-reference.md)
