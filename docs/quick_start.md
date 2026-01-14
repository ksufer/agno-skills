# 快速开始指南

## 1. 获取 API 密钥

访问阿里云 DashScope 控制台：
- 🔗 https://dashscope.console.aliyun.com/
- 登录后在 "API-KEY 管理" 页面创建或查看你的 API 密钥

## 2. 设置环境变量

### 方法 1：使用 .env 文件（推荐）

在项目根目录创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=sk-your-dashscope-api-key-here
```

**注意**：`.env` 文件不要提交到 Git（已在 .gitignore 中）

### 方法 2：设置系统环境变量

**Windows PowerShell:**
```powershell
# 当前会话
$env:DASHSCOPE_API_KEY="sk-your-api-key"

# 永久设置（推荐）
[System.Environment]::SetEnvironmentVariable('DASHSCOPE_API_KEY', 'sk-your-api-key', 'User')
```

**Windows CMD:**
```cmd
set DASHSCOPE_API_KEY=sk-your-api-key
```

**Linux/macOS:**
```bash
export DASHSCOPE_API_KEY="sk-your-api-key"
```

### 方法 3：在代码中直接设置（仅用于测试）

```python
import os
os.environ["DASHSCOPE_API_KEY"] = "sk-your-api-key"
```

## 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 4. 运行示例

```bash
# 基础使用示例
python examples/basic_usage.py

# Skill 创建示例
python examples/create_skill.py

# 运行测试
python test_skills_agent.py
```

## 5. 验证安装

运行以下 Python 代码验证配置：

```python
import os
from agno.agent import Agent
from agno.models.dashscope import DashScope

# 检查 API 密钥
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    print("❌ DASHSCOPE_API_KEY 未设置")
    print("请按照上述方法设置 API 密钥")
else:
    print(f"✅ API 密钥已设置（前 10 位）: {api_key[:10]}...")
    
    # 测试连接
    try:
        agent = Agent(model=DashScope(id="qwen-plus"), markdown=True)
        response = agent.run("你好")
        print("✅ DashScope 连接成功！")
        print(f"响应: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
```

保存为 `test_connection.py` 并运行：
```bash
python test_connection.py
```

## 常见问题

### Q1: 401 错误 - Incorrect API key

**可能原因**：

1. **API 密钥未设置或不正确**
   - 检查 API 密钥是否正确复制（包括 `sk-` 前缀）
   - 确认环境变量已正确设置

2. **API 端点地区不匹配**（最常见❗）
   - 本项目默认使用**中国大陆端点**
   - 如果你的 API 密钥来自国际版阿里云，会导致 401 错误
   - 解决方法：查看 [API 端点配置文档](dashscope_endpoints.md)

3. **环境变量未生效**
   - 如果使用 PowerShell，重新打开终端窗口使环境变量生效

### Q2: 找不到模块错误

**原因**：依赖未安装

**解决方法**：
```bash
pip install -r requirements.txt
```

### Q3: .env 文件不生效

**原因**：未调用 `load_dotenv()`

**解决方法**：
在代码开头添加：
```python
from dotenv import load_dotenv
load_dotenv()
```

### Q4: 如何检查环境变量是否设置成功？

**Windows PowerShell:**
```powershell
echo $env:DASHSCOPE_API_KEY
```

**Windows CMD:**
```cmd
echo %DASHSCOPE_API_KEY%
```

**Linux/macOS:**
```bash
echo $DASHSCOPE_API_KEY
```

## 下一步

- 📖 查看 [README.md](../README.md) 了解完整功能
- 🔧 阅读 [DashScope 迁移文档](dashscope_migration.md) 了解更多配置选项
- 💡 浏览 [examples/](../examples/) 目录查看更多示例

## 获取帮助

- **Agno 文档**：https://docs.agno.com
- **DashScope 文档**：https://help.aliyun.com/zh/dashscope/
- **项目 Issues**：在 GitHub 上提问
