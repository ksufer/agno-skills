# Git 配置指南

## .gitignore 说明

项目已创建 `.gitignore` 文件，包含以下类别：

### 1. Python 相关
- `*.pyc`, `__pycache__/` - Python 编译文件
- `*.egg-info/`, `dist/`, `build/` - 打包文件
- `venv/`, `.venv/` - 虚拟环境

### 2. 环境变量和密钥
- `.env` - 环境变量文件（**重要：包含 API 密钥**）
- `credentials.json`, `secrets.yaml` - 凭证文件
- `*_api_key*`, `*secret*` - 任何包含密钥的文件

### 3. IDE 和编辑器
- `.vscode/`, `.idea/` - IDE 配置
- `.cursor/` - Cursor IDE 配置
- `*.swp`, `*.swo` - Vim 临时文件

### 4. 操作系统
- `.DS_Store` - macOS 系统文件
- `Thumbs.db` - Windows 缩略图
- `*.lnk` - Windows 快捷方式

### 5. Agno / AI Agent 特定
- `*.db`, `*.sqlite` - 数据库文件
- `tmp/`, `logs/` - 临时文件和日志
- `lancedb/`, `chromadb/` - 向量数据库
- `my_skills/`, `user_skills/` - 用户自定义 skills

### 6. 测试和文档
- `.pytest_cache/`, `test_results/` - 测试缓存
- `docs/_build/` - 文档构建输出

## ⚠️ 重要：不要提交的文件

### 1. API 密钥文件
```bash
.env                    # 包含 DASHSCOPE_API_KEY
credentials.json
*_api_key.txt
secrets.yaml
```

### 2. 数据库文件
```bash
*.db
*.sqlite
tmp/agents.db
tmp/workflow.db
```

### 3. 本地配置
```bash
.vscode/settings.json
.idea/workspace.xml
```

## ✅ 应该提交的文件

### 1. 源代码
```bash
*.py                    # Python 源文件
agno_skills_agent/      # 核心模块
examples/               # 示例代码
```

### 2. 配置示例
```bash
.env.example            # 环境变量模板（不含真实密钥）
requirements.txt        # 依赖列表
```

### 3. 文档
```bash
README.md
docs/                   # 文档目录
*.md                    # Markdown 文档
```

### 4. Skills 示例
```bash
skills-examples/        # 示例 skills（如果是公开的）
```

## Git 初始化

如果项目还没有初始化 Git：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件（.gitignore 会自动排除不需要的）
git add .

# 查看将要提交的文件
git status

# 首次提交
git commit -m "Initial commit: Agno Skills Agent with DashScope"
```

## 创建 .env.example

为了帮助其他开发者配置环境，创建 `.env.example` 模板：

```bash
# 复制 .env 为模板（先删除真实密钥）
cp .env .env.example
```

`.env.example` 内容应该是：
```env
# DashScope API 密钥
# 从 https://dashscope.console.aliyun.com/ 获取
DASHSCOPE_API_KEY=sk-your-api-key-here

# 调试模式（可选）
DEBUG_MODE=false
```

## 检查敏感信息

在提交前，检查是否有敏感信息：

```bash
# 查看即将提交的文件
git status

# 查看具体更改内容
git diff

# 搜索可能的 API 密钥（在提交前）
git grep -i "sk-" -- . ':!.gitignore'
git grep -i "api.key" -- . ':!.gitignore'
```

## 已经提交了敏感信息？

如果不小心提交了 API 密钥：

### 1. 立即撤销密钥
- 访问 DashScope 控制台
- 删除或禁用该 API 密钥
- 生成新的密钥

### 2. 清理 Git 历史

**警告：这会重写 Git 历史，仅在必要时使用**

```bash
# 使用 git filter-branch 或 BFG Repo-Cleaner
# 详见：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

### 3. 强制推送（如果已推送到远程）

```bash
git push --force origin main
```

## Git 工作流建议

### 分支策略

```bash
# 主分支
main/master         # 稳定版本

# 开发分支
dev                 # 开发版本

# 功能分支
feature/xxx         # 新功能
bugfix/xxx          # Bug 修复
docs/xxx            # 文档更新
```

### 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```bash
feat: add new skill loader feature
fix: resolve API endpoint configuration issue
docs: update quick start guide
refactor: improve skill matching algorithm
test: add unit tests for SkillExecutor
chore: update dependencies
```

### 示例工作流

```bash
# 1. 创建功能分支
git checkout -b feature/add-new-skill

# 2. 进行开发
# ... 编辑代码 ...

# 3. 提交更改
git add .
git commit -m "feat: add JSON data processing skill"

# 4. 推送到远程
git push origin feature/add-new-skill

# 5. 创建 Pull Request（如果使用 GitHub/GitLab）
```

## 常用 Git 命令

```bash
# 查看状态
git status

# 查看更改
git diff

# 添加文件
git add <file>
git add .                # 添加所有更改

# 提交
git commit -m "message"

# 查看历史
git log
git log --oneline        # 简洁视图

# 撤销更改
git checkout -- <file>   # 撤销工作区更改
git reset HEAD <file>    # 取消暂存

# 分支操作
git branch               # 查看分支
git branch <name>        # 创建分支
git checkout <branch>    # 切换分支
git merge <branch>       # 合并分支

# 远程仓库
git remote add origin <url>
git push -u origin main
git pull origin main
```

## .gitattributes（可选）

创建 `.gitattributes` 规范化行尾：

```bash
# Auto detect text files and perform LF normalization
* text=auto

# Python
*.py text eol=lf
*.pyx text eol=lf

# Shell scripts
*.sh text eol=lf
*.bash text eol=lf

# Windows scripts
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf

# Documents
*.md text eol=lf
*.txt text eol=lf
*.json text eol=lf
*.yaml text eol=lf
*.yml text eol=lf

# Binary files
*.db binary
*.sqlite binary
*.pkl binary
*.pickle binary
*.pyc binary
```

## GitHub/GitLab 配置

### README badges（可选）

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Agno](https://img.shields.io/badge/framework-Agno-orange.svg)
```

### GitHub Actions（可选）

创建 `.github/workflows/test.yml` 进行自动化测试：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python test_skills_agent.py
```

## 总结

✅ 已创建 `.gitignore` 文件  
✅ 包含所有必要的忽略规则  
✅ 保护 API 密钥和敏感信息  
✅ 适用于 Python + Agno 项目  

**重要提醒**：
- 绝不提交 `.env` 文件到 Git
- 定期检查 `git status` 确保没有敏感文件
- 使用 `.env.example` 提供配置模板

---

**参考资源**：
- [gitignore.io](https://www.toptal.com/developers/gitignore) - 生成 .gitignore
- [GitHub .gitignore 模板](https://github.com/github/gitignore)
- [Conventional Commits](https://www.conventionalcommits.org/)
