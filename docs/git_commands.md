# Git 常用命令速查

## 📋 快速开始

### 查看当前状态
```bash
git status              # 查看完整状态
git status -s           # 简洁视图
git status --short      # 同上
```

### 添加文件到暂存区
```bash
git add <file>          # 添加指定文件
git add .               # 添加所有更改
git add *.py            # 添加所有 Python 文件
git add docs/           # 添加整个目录
```

### 提交更改
```bash
git commit -m "commit message"              # 提交并附带消息
git commit -am "message"                    # 添加并提交已跟踪的文件
git commit --amend                          # 修改最后一次提交
```

### 查看历史
```bash
git log                 # 查看提交历史
git log --oneline       # 简洁单行视图
git log --graph         # 图形化显示分支
git log -p              # 显示差异
git log -n 5            # 显示最近 5 次提交
```

## 🔍 查看更改

### 查看差异
```bash
git diff                # 工作区 vs 暂存区
git diff --staged       # 暂存区 vs 最后一次提交
git diff HEAD           # 工作区 vs 最后一次提交
git diff <file>         # 查看特定文件的更改
```

### 查看文件状态
```bash
git status
git diff --name-only    # 只显示更改的文件名
git diff --stat         # 显示统计信息
```

## 🔙 撤销更改

### 撤销工作区的更改
```bash
git checkout -- <file>  # 撤销对文件的修改
git restore <file>      # 新版本命令（推荐）
git restore .           # 撤销所有更改
```

### 取消暂存
```bash
git reset HEAD <file>   # 从暂存区移除
git restore --staged <file>  # 新版本命令（推荐）
```

### 撤销提交
```bash
git reset --soft HEAD~1     # 撤销提交，保留更改在暂存区
git reset --mixed HEAD~1    # 撤销提交，更改回到工作区
git reset --hard HEAD~1     # 完全撤销（危险！）
```

## 🌿 分支操作

### 查看分支
```bash
git branch              # 查看本地分支
git branch -a           # 查看所有分支（包括远程）
git branch -v           # 显示最后一次提交
```

### 创建和切换分支
```bash
git branch <name>       # 创建分支
git checkout <name>     # 切换分支
git checkout -b <name>  # 创建并切换到新分支
git switch <name>       # 新版本切换命令
git switch -c <name>    # 新版本创建并切换
```

### 合并和删除分支
```bash
git merge <branch>      # 合并分支到当前分支
git branch -d <name>    # 删除分支（安全删除）
git branch -D <name>    # 强制删除分支
```

## 🌐 远程仓库

### 查看远程仓库
```bash
git remote              # 查看远程仓库
git remote -v           # 查看详细信息
git remote show origin  # 查看 origin 详细信息
```

### 添加和删除远程仓库
```bash
git remote add origin <url>     # 添加远程仓库
git remote remove origin        # 删除远程仓库
git remote rename old new       # 重命名
```

### 推送和拉取
```bash
git push origin <branch>        # 推送到远程分支
git push -u origin main         # 首次推送并设置上游
git push --all                  # 推送所有分支
git pull origin <branch>        # 拉取并合并
git fetch origin                # 仅获取，不合并
```

## 🏷️ 标签操作

### 创建标签
```bash
git tag v1.0.0                  # 创建轻量标签
git tag -a v1.0.0 -m "version 1.0.0"  # 创建附注标签
git tag -a v1.0.0 <commit-id>   # 为特定提交打标签
```

### 查看和推送标签
```bash
git tag                         # 列出所有标签
git show v1.0.0                 # 查看标签信息
git push origin v1.0.0          # 推送单个标签
git push origin --tags          # 推送所有标签
```

## 🧹 清理和维护

### 清理未跟踪的文件
```bash
git clean -n            # 预览要删除的文件
git clean -f            # 删除未跟踪的文件
git clean -fd           # 删除文件和目录
git clean -fX           # 只删除忽略的文件
```

### 垃圾回收
```bash
git gc                  # 清理不必要的文件并优化
git prune               # 删除不可达的对象
```

## 🔍 搜索和查找

### 在文件中搜索
```bash
git grep "search term"          # 在工作区搜索
git grep "term" <branch>        # 在特定分支搜索
git grep -n "term"              # 显示行号
```

### 查找提交
```bash
git log --grep="keyword"        # 搜索提交消息
git log -S "code"               # 搜索代码更改
git blame <file>                # 查看文件每行的修改者
```

## 📦 存储和恢复

### 暂存工作
```bash
git stash               # 暂存当前更改
git stash save "message"  # 附带消息暂存
git stash list          # 查看暂存列表
git stash pop           # 恢复并删除最新暂存
git stash apply         # 恢复但保留暂存
git stash drop          # 删除最新暂存
git stash clear         # 清空所有暂存
```

## 🎯 本项目常用工作流

### 1. 日常开发流程
```bash
# 1. 查看当前状态
git status

# 2. 拉取最新代码
git pull origin main

# 3. 创建功能分支
git checkout -b feature/my-new-feature

# 4. 进行开发...
# 编辑文件

# 5. 查看更改
git status
git diff

# 6. 添加更改
git add .

# 7. 提交
git commit -m "feat: add new feature"

# 8. 推送到远程
git push -u origin feature/my-new-feature
```

### 2. 快速提交
```bash
git add .
git commit -m "feat: implement skill matching algorithm"
git push
```

### 3. 提交前检查
```bash
# 查看将要提交的内容
git status
git diff --staged

# 确保没有敏感信息
git grep -i "sk-" -- . ':!.gitignore'
git grep -i "api.key" -- . ':!.gitignore'

# 确认后提交
git commit -m "your message"
```

### 4. 修复提交消息
```bash
# 修改最后一次提交消息（未推送）
git commit --amend -m "new message"

# 如果已推送（谨慎使用）
git commit --amend -m "new message"
git push --force-with-lease
```

### 5. 同步远程更改
```bash
# 方法 1: Pull（获取并合并）
git pull origin main

# 方法 2: Fetch + Merge（更安全）
git fetch origin
git merge origin/main

# 方法 3: Rebase（保持线性历史）
git pull --rebase origin main
```

## ⚠️ 危险命令（谨慎使用）

```bash
git reset --hard HEAD~1         # 完全删除最后一次提交
git push --force                # 强制推送（可能覆盖他人工作）
git clean -fd                   # 删除所有未跟踪的文件和目录
git branch -D <name>            # 强制删除分支（丢失未合并的更改）
```

**使用这些命令前请三思！**

## 🆘 常见问题解决

### 撤销错误的 git add
```bash
git reset HEAD <file>
# 或
git restore --staged <file>
```

### 修改最后一次提交
```bash
# 修改提交消息
git commit --amend

# 添加遗漏的文件到最后一次提交
git add forgotten_file
git commit --amend --no-edit
```

### 放弃所有本地更改
```bash
git reset --hard HEAD
git clean -fd
```

### 恢复已删除的分支
```bash
# 查找删除前的提交 ID
git reflog

# 恢复分支
git checkout -b <branch-name> <commit-id>
```

### 合并冲突解决
```bash
# 1. 查看冲突文件
git status

# 2. 编辑冲突文件，解决冲突标记
# <<<<<<< HEAD
# 你的更改
# =======
# 他人的更改
# >>>>>>> branch

# 3. 标记为已解决
git add <resolved-file>

# 4. 完成合并
git commit
```

## 📝 提交消息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```bash
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 重构
test: 测试相关
chore: 构建或辅助工具
perf: 性能优化
ci: CI/CD 相关
```

**示例：**
```bash
git commit -m "feat: add DashScope model support"
git commit -m "fix: resolve API endpoint configuration issue"
git commit -m "docs: update quick start guide"
git commit -m "refactor: improve skill matching algorithm"
```

## 🔧 Git 配置

### 用户信息
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 编辑器
```bash
git config --global core.editor "code --wait"  # VSCode
git config --global core.editor "vim"          # Vim
```

### 别名
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph"
```

### 查看配置
```bash
git config --list
git config --global --list
git config user.name
```

## 📚 参考资源

- [Git 官方文档](https://git-scm.com/doc)
- [Git 简明指南](https://rogerdudler.github.io/git-guide/index.zh.html)
- [Learn Git Branching](https://learngitbranching.js.org/)
- [GitHub Git 备忘单](https://education.github.com/git-cheat-sheet-education.pdf)

---

**提示**：将此文件添加到书签，随时查阅！
