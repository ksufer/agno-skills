# 解决 DashScope API 密钥问题

## 🔴 当前问题

你遇到了 **401 Unauthorized** 错误：
```
ERROR: Incorrect API key provided
```

这表示 `DASHSCOPE_API_KEY` 环境变量未设置或设置不正确。

## ✅ 解决步骤

### 步骤 1：获取 API 密钥

1. 访问 **阿里云 DashScope 控制台**：
   - 🔗 https://dashscope.console.aliyun.com/
   
2. 登录你的阿里云账号

3. 在左侧菜单找到 **"API-KEY 管理"**

4. 点击 **"创建新的 API-KEY"** 或查看现有密钥

5. 复制 API 密钥（格式类似：`sk-xxxxxxxxxxxxxxxxxx`）

### 步骤 2：设置环境变量

#### 🎯 方法 1：使用 .env 文件（最推荐）

在项目根目录 `d:\Gitrepos\agno_skills\` 创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=sk-你的实际API密钥
```

**优点**：
- ✅ 不需要每次都设置
- ✅ 不会暴露在代码中
- ✅ 已自动添加到 .gitignore

#### 🎯 方法 2：PowerShell 永久设置

在 PowerShell 中运行：

```powershell
# 设置用户级环境变量（重启后仍有效）
[System.Environment]::SetEnvironmentVariable('DASHSCOPE_API_KEY', 'sk-你的实际API密钥', 'User')

# 验证设置
echo $env:DASHSCOPE_API_KEY
```

**重要**：设置后需要 **重新打开 PowerShell 窗口** 使环境变量生效。

#### 方法 3：PowerShell 临时设置

在当前 PowerShell 窗口中运行：

```powershell
$env:DASHSCOPE_API_KEY="sk-你的实际API密钥"
```

**注意**：关闭窗口后失效，需要重新设置。

#### 方法 4：CMD

```cmd
set DASHSCOPE_API_KEY=sk-你的实际API密钥
```

### 步骤 3：验证配置

运行测试脚本：

```bash
python test_connection.py
```

**预期输出**：
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

🎉 配置完成！现在可以运行示例了：
   python examples/basic_usage.py
```

### 步骤 4：运行你的程序

连接成功后，运行：

```bash
python examples/basic_usage.py
```

## 🔍 常见问题

### Q1: 设置后仍然报 401 错误

**可能原因**：
1. API 密钥复制不完整或有多余空格
2. PowerShell 环境变量未生效（需重新打开终端）
3. 使用了错误的密钥格式

**解决方法**：
```powershell
# 检查当前环境变量
echo $env:DASHSCOPE_API_KEY

# 如果为空或不正确，重新设置
$env:DASHSCOPE_API_KEY="sk-完整的密钥"

# 立即在同一窗口测试
python test_connection.py
```

### Q2: API 密钥在哪里获取？

访问：https://dashscope.console.aliyun.com/

如果没有账号，需要先注册阿里云账号并开通 DashScope 服务。

### Q3: .env 文件不生效

确保：
1. 文件名正确：`.env`（注意开头的点）
2. 文件位置：项目根目录 `d:\Gitrepos\agno_skills\.env`
3. 代码中已调用 `load_dotenv()`（示例代码已更新）

验证 .env 文件：
```powershell
# 查看文件是否存在
Test-Path "d:\Gitrepos\agno_skills\.env"

# 查看文件内容
Get-Content "d:\Gitrepos\agno_skills\.env"
```

### Q4: 多个终端窗口的问题

环境变量只在设置它的终端窗口中有效（除非使用永久设置）。

**建议**：
- 使用 `.env` 文件方法（最可靠）
- 或使用永久环境变量设置

## 📋 检查清单

完成以下检查：

- [ ] 已从 DashScope 控制台获取 API 密钥
- [ ] API 密钥包含 `sk-` 前缀
- [ ] 已设置环境变量（使用上述任一方法）
- [ ] 运行 `python test_connection.py` 成功
- [ ] 能正常运行示例程序

## 🆘 仍然有问题？

### 详细诊断

运行以下 Python 代码查看详细信息：

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("=== 环境检查 ===")
print(f"当前工作目录: {os.getcwd()}")
print(f"API 密钥是否设置: {'是' if os.getenv('DASHSCOPE_API_KEY') else '否'}")

if os.getenv('DASHSCOPE_API_KEY'):
    key = os.getenv('DASHSCOPE_API_KEY')
    print(f"API 密钥前缀: {key[:3]}")
    print(f"API 密钥长度: {len(key)}")
else:
    print("❌ DASHSCOPE_API_KEY 未设置")
    print("\n请按照《解决API密钥问题.md》设置环境变量")
```

保存为 `check_env.py` 并运行：
```bash
python check_env.py
```

### 查看文档

- 📖 **快速开始**：`docs/quick_start.md`
- 🔧 **迁移文档**：`docs/dashscope_migration.md`
- 📝 **修改记录**：`CHANGES.md`

### 联系支持

- **Agno 文档**：https://docs.agno.com/integrations/models/native/dashscope/overview
- **DashScope 帮助**：https://help.aliyun.com/zh/dashscope/

## 💡 最佳实践

1. **使用 .env 文件**：最简单可靠的方法
2. **不要在代码中硬编码密钥**：有安全风险
3. **定期检查密钥有效性**：运行 `test_connection.py`
4. **妥善保管密钥**：不要上传到 Git 仓库

---

**祝你成功配置！** 🎉

如果按照上述步骤仍有问题，请提供详细的错误信息以便进一步诊断。
