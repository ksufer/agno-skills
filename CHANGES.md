# 修改记录

## 2026-01-14: Git 配置文件创建

### 📦 新增文件

1. **`.gitignore`**
   - Python 相关忽略规则（*.pyc, __pycache__, venv 等）
   - 环境变量和密钥文件（.env, credentials.json 等）
   - IDE 配置（.vscode, .idea, .cursor 等）
   - 操作系统文件（.DS_Store, Thumbs.db 等）
   - Agno 特定文件（数据库、日志、向量数据库等）
   - 测试和构建产物

2. **`.env.example`**
   - 环境变量配置模板
   - 不包含真实 API 密钥
   - 供新用户参考配置

3. **`docs/git_setup.md`**
   - Git 仓库配置指南
   - .gitignore 详细说明
   - 敏感信息保护建议
   - Git 工作流程和最佳实践

4. **`docs/git_commands.md`**
   - Git 常用命令速查表
   - 分类清晰的命令列表
   - 本项目的常用工作流
   - 问题解决方案

### ✅ 验证结果

- ✅ `.env` 文件已被正确忽略（不会被提交）
- ✅ Python 缓存文件被忽略
- ✅ IDE 配置文件被忽略
- ✅ 所有敏感信息受保护

### 🎯 使用说明

1. **首次使用**：复制 `.env.example` 为 `.env` 并填入真实 API 密钥
2. **提交代码**：使用 `git status` 检查，确保没有敏感文件
3. **参考文档**：查看 `docs/git_setup.md` 和 `docs/git_commands.md`

---

## 2026-01-14: DashScope API 端点配置修复

### 🔧 重要修复

**问题**：用户遇到 401 "Incorrect API key provided" 错误

**原因**：中国大陆用户必须使用指定的 API 端点，否则即使 API 密钥正确也会报 401 错误

**解决**：
- 在 `SkillsAgent` 类中显式配置中国大陆 DashScope 端点
- 更新测试脚本使用正确的端点
- 添加详细的端点配置文档

### 修改内容

1. **agno_skills_agent/skills_agent.py**
   - 添加 `base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"` 配置

2. **test_connection.py**
   - 添加 `base_url` 参数到测试代码

3. **docs/dashscope_endpoints.md**（新增）
   - API 端点类型说明
   - 中国大陆 vs 国际版配置
   - 常见错误和解决方法

4. **README.md**
   - 更新故障排除部分，强调端点配置问题
   - 添加端点配置文档链接

5. **docs/quick_start.md**
   - 更新常见问题，添加端点地区不匹配说明

### 关键信息

- ✅ **正确端点**：`https://dashscope.aliyuncs.com/compatible-mode/v1`（中国大陆）
- ❌ **错误端点**：`https://dashscope.aliyuncs.com/api/v1`（原生 API，Agno 不支持）
- ℹ️ **默认端点**：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`（国际版）

---

## 2026-01-14: DashScope 模型迁移

### 修改摘要

将项目从 OpenAI (GPT-4o) 迁移到 Alibaba Cloud DashScope (Qwen-Plus) 模型。

### 修改文件列表

#### 代码文件 (4 个)

1. **agno_skills_agent/skills_agent.py**
   - 修改导入：`OpenAIChat` → `DashScope`
   - 修改默认模型：`gpt-4o` → `qwen-plus`
   - 更新文档注释

2. **examples/basic_usage.py**
   - 更新 API 密钥注释：`OPENAI_API_KEY` → `DASHSCOPE_API_KEY`
   - 修改模型 ID：`gpt-4o` → `qwen-plus`

3. **examples/create_skill.py**
   - 更新 API 密钥注释：`OPENAI_API_KEY` → `DASHSCOPE_API_KEY`
   - 修改模型 ID：`gpt-4o` → `qwen-plus`

4. **test_skills_agent.py**
   - 更新测试注释中的 API 密钥引用

#### 文档文件 (2 个)

5. **README.md**
   - 更新 API 密钥设置说明
   - 修改所有示例代码中的模型配置
   - 更新技术栈说明
   - 修改致谢部分

6. **PROJECT_SUMMARY.md**
   - 更新依赖项列表
   - 修改致谢部分

#### 依赖文件 (1 个)

7. **requirements.txt**
   - 移除 `openai>=1.0.0`（DashScope 已集成在 agno 中）

#### 新增文件 (4 个)

8. **docs/dashscope_migration.md**
   - 完整的迁移文档
   - 使用说明和代码示例
   - 模型对比和优势分析

9. **docs/quick_start.md**
   - 快速开始指南
   - API 密钥配置详细说明
   - 常见问题解答

10. **test_connection.py**
    - API 连接测试脚本
    - 自动诊断配置问题
    - 提供详细的错误提示

11. **CHANGES.md**
    - 本文件（修改记录）

#### 功能增强 (2 个)

12. **examples/basic_usage.py**
    - 添加 `load_dotenv()` 支持 .env 文件

13. **examples/create_skill.py**
    - 添加 `load_dotenv()` 支持 .env 文件

### 验证结果

✅ 所有代码文件中的导入已更新为 DashScope  
✅ 所有默认模型 ID 已改为 qwen-plus  
✅ 所有 API 密钥引用已更新  
✅ 文档完全同步更新  
✅ 依赖项已优化  

### 使用方法

设置 API 密钥后即可使用：

```bash
# Windows CMD
set DASHSCOPE_API_KEY=your-api-key

# Windows PowerShell
$env:DASHSCOPE_API_KEY="your-api-key"

# Linux/macOS
export DASHSCOPE_API_KEY="your-api-key"
```

运行示例：

```bash
python examples/basic_usage.py
```

### 相关文档

- 详细迁移文档：`docs/dashscope_migration.md`
- 项目 README：`README.md`
- Agno DashScope 文档：https://docs.agno.com/integrations/models/native/dashscope/overview
