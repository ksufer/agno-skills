# 测试脚本

本目录包含项目的测试脚本。

## 测试文件

### test_connection.py
测试 DashScope API 连接和配置。

**运行：**
```bash
python test/test_connection.py
```

**功能：**
- 检查 DASHSCOPE_API_KEY 环境变量
- 测试 DashScope API 连接
- 验证模型响应
- 提供详细的诊断信息

### test_skills_agent.py
测试 Skills Agent 核心功能。

**运行：**
```bash
python test/test_skills_agent.py
```

**测试内容：**
- SkillLoader 功能
- SkillMatcher 匹配算法
- SkillExecutor 工具创建
- SkillsAgent 集成
- 渐进式披露机制

## 运行所有测试

```bash
# 运行 API 连接测试
python test/test_connection.py

# 运行 Agent 功能测试
python test/test_skills_agent.py
```

## 测试要求

- Python 3.9+
- 已安装 requirements.txt 中的依赖
- 已设置 DASHSCOPE_API_KEY 环境变量（test_connection.py）

## 注意事项

- `test_connection.py` 需要有效的 API 密钥
- `test_skills_agent.py` 可在没有 API 密钥的情况下运行大部分测试
