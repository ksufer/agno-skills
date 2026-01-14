# DashScope API 端点说明

## API 端点类型

DashScope 提供两种 API 格式：

### 1. OpenAI 兼容模式（推荐，Agno 使用此模式）

**国际版（默认）：**
```
https://dashscope-intl.aliyuncs.com/compatible-mode/v1
```

**中国大陆版：**
```
https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 2. DashScope 原生 API（Agno 不使用）

```
https://dashscope.aliyuncs.com/api/v1
```

## ⚠️ 重要说明

### 中国大陆用户必读

如果你的 API 密钥是从**中国大陆阿里云账号**获取的，**必须**显式指定 `base_url`：

```python
from agno.models.dashscope import DashScope

model = DashScope(
    id="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 必须指定
)
```

**不指定会导致 401 错误**：
```
ERROR: Incorrect API key provided
```

### 国际版用户

如果你的 API 密钥是从**国际版阿里云**获取的，可以使用默认配置：

```python
model = DashScope(id="qwen-plus")  # 使用默认国际版端点
```

## 如何判断你的账号类型

### 方法 1：查看登录地址

- **中国大陆版**：https://dashscope.console.aliyun.com/
- **国际版**：https://dashscope-intl.console.aliyun.com/

### 方法 2：查看 API 密钥来源

在 DashScope 控制台查看你创建 API 密钥时使用的区域。

## 完整配置示例

### 中国大陆用户

```python
import os
from agno.agent import Agent
from agno.models.dashscope import DashScope

# 设置 API 密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-your-api-key"

# 创建 Agent（必须指定 base_url）
agent = Agent(
    model=DashScope(
        id="qwen-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    ),
    markdown=True
)

agent.print_response("你好")
```

### 国际版用户

```python
import os
from agno.agent import Agent
from agno.models.dashscope import DashScope

# 设置 API 密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-your-api-key"

# 创建 Agent（使用默认端点）
agent = Agent(
    model=DashScope(id="qwen-plus"),
    markdown=True
)

agent.print_response("Hello")
```

## 在项目中的应用

### SkillsAgent 类

项目的 `SkillsAgent` 类已经配置为使用中国大陆端点：

```python
from agno_skills_agent import SkillsAgent

agent = SkillsAgent(
    skills_dir="skills-examples/skills",
    model_id="qwen-plus"  # 内部已配置正确的 base_url
)
```

如果需要使用国际版端点，可以直接修改 `agno_skills_agent/skills_agent.py` 中的 `base_url` 配置。

## 常见错误

### 错误 1：使用了原生 API 端点

❌ **错误配置**：
```python
model = DashScope(
    id="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/api/v1"  # 错误！
)
```

✅ **正确配置**：
```python
model = DashScope(
    id="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 正确
)
```

### 错误 2：地区不匹配

如果你是中国大陆用户但使用了默认（国际版）端点：

```python
# 会导致 401 错误
model = DashScope(id="qwen-plus")  # 默认使用国际版端点
```

必须显式指定：
```python
model = DashScope(
    id="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```

## 参数完整列表

根据 Agno 文档，DashScope 支持以下参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | str | "qwen-plus" | 模型 ID |
| `name` | str | "Qwen" | 模型名称 |
| `provider` | str | "Dashscope" | 提供商 |
| `api_key` | Optional[str] | None | API 密钥（默认从环境变量读取） |
| `base_url` | str | "https://dashscope-intl.aliyuncs.com/compatible-mode/v1" | API 端点 |
| `enable_thinking` | bool | False | 启用推理过程（用于 qvq-max 模型） |
| `include_thoughts` | Optional[bool] | None | 在响应中包含思考过程 |
| `thinking_budget` | Optional[int] | None | 思考 token 预算 |

## 测试连接

运行测试脚本验证配置：

```bash
python test_connection.py
```

成功输出示例：
```
✅ API 密钥已设置
   前 10 位: sk-xxxxxxx...
   长度: XX 字符

正在测试 DashScope 连接...

✅ DashScope 连接成功！

模型响应：
------------------------------------------------------------
你好！我是通义千问...
------------------------------------------------------------
```

## 参考资料

- **Agno DashScope 文档**：https://docs.agno.com/integrations/models/native/dashscope/overview
- **阿里云 DashScope 控制台**：https://dashscope.console.aliyun.com/
- **DashScope 官方文档**：https://help.aliyun.com/zh/dashscope/

## 总结

✅ **使用 OpenAI 兼容模式**：`/compatible-mode/v1`  
✅ **中国大陆用户必须显式指定 base_url**  
✅ **不要使用原生 API 端点** `/api/v1`  
✅ **运行测试脚本验证配置**  
