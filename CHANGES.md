# 修改记录

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

#### 新增文件 (2 个)

8. **docs/dashscope_migration.md**
   - 完整的迁移文档
   - 使用说明和代码示例
   - 模型对比和优势分析

9. **CHANGES.md**
   - 本文件（修改记录）

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
