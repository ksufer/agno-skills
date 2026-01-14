# ⚠️ API 端点配置重要说明

## 🔴 如果你遇到 401 错误

```
ERROR: Incorrect API key provided
```

**最常见原因：API 端点地区不匹配！**

## ✅ 已修复

项目代码已更新，**默认使用中国大陆 DashScope 端点**。

### 现在你只需要：

1. **设置 API 密钥**：
   ```powershell
   $env:DASHSCOPE_API_KEY="sk-your-api-key"
   ```

2. **运行测试**：
   ```bash
   python test_connection.py
   ```

3. **应该成功了！** ✅

## 🌍 关于 API 端点

### DashScope 有两种端点：

#### 1. OpenAI 兼容模式（Agno 使用这个）✅

- **中国大陆**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- **国际版**：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

#### 2. 原生 API（不要用）❌

- `https://dashscope.aliyuncs.com/api/v1` ← Agno 不支持

## 🔧 代码已修复

### 之前的代码（会导致 401）：

```python
agent = Agent(
    model=DashScope(id="qwen-plus")  # 使用默认国际版端点
)
```

### 现在的代码（已修复）：

```python
agent = Agent(
    model=DashScope(
        id="qwen-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 指定中国大陆端点
    )
)
```

## 📍 你的账号是哪个版本？

### 检查方法：

- **中国大陆版**：在 https://dashscope.console.aliyun.com/ 获取的 API 密钥
- **国际版**：在 https://dashscope-intl.console.aliyun.com/ 获取的 API 密钥

### 如果是国际版：

修改 `agno_skills_agent/skills_agent.py` 第 65 行：

```python
# 改为国际版端点
"base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
```

## 📚 详细文档

- **API 端点完整说明**：[docs/dashscope_endpoints.md](docs/dashscope_endpoints.md)
- **快速开始指南**：[docs/quick_start.md](docs/quick_start.md)
- **修改记录**：[CHANGES.md](CHANGES.md)

## 🆘 仍然有问题？

1. 运行诊断脚本：`python test_connection.py`
2. 查看详细错误信息
3. 检查 API 密钥是否正确设置：`echo $env:DASHSCOPE_API_KEY`
4. 确认 API 密钥来源（中国大陆 vs 国际版）

## ✨ 总结

- ✅ **项目已配置中国大陆端点**
- ✅ **大多数用户现在可以直接使用**
- ✅ **国际版用户需要修改 base_url**
- ✅ **运行测试脚本验证配置**

---

**更新时间**：2026-01-14  
**相关问题**：401 Unauthorized, Incorrect API key provided
