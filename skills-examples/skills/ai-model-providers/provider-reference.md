# AI 模型提供商参考文档

## OpenAI

### API 文档
- 官方文档: https://platform.openai.com/docs/api-reference
- Python SDK: https://github.com/openai/openai-python

### 关键参数
- `model`: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- `temperature`: 0-2, 控制随机性
- `max_tokens`: 最大生成token数
- `stream`: 是否流式返回

### 速率限制
- 免费层: 3 RPM (每分钟请求数)
- 付费层: 根据套餐不同

---

## OpenRouter

### API 文档
- 官方文档: https://openrouter.ai/docs
- 兼容OpenAI接口

### 支持的模型
- 超过100+模型可选
- 格式: `provider/model-name`
- 示例: `anthropic/claude-3-opus`, `google/gemini-pro`

### 特殊功能
- 自动降级: 模型不可用时自动切换备选
- 成本优化: 根据成本自动选择最优模型

---

## DashScope (阿里云通义千问)

### API 文档
- 官方文档: https://help.aliyun.com/zh/dashscope/
- Python SDK: `pip install dashscope`

### 主要模型
- `qwen-turbo`: 快速响应
- `qwen-plus`: 平衡性能
- `qwen-max`: 最强性能

### 关键参数
- `result_format`: 'text' 或 'message'
- `enable_search`: 是否启用联网搜索
- `seed`: 随机种子

### 速率限制
- 免费额度: 100万tokens/月
- 并发限制: 根据实例规格

---

## GLM (智谱AI)

### API 文档
- 官方文档: https://open.bigmodel.cn/dev/api
- Python SDK: `pip install zhipuai`

### 主要模型
- `glm-4`: 最新版本
- `glm-4v`: 支持视觉
- `glm-3-turbo`: 快速版本

### 关键参数
- `do_sample`: 是否采样
- `top_p`: 核采样参数
- `temperature`: 温度参数
- `request_id`: 请求追踪ID

### 速率限制
- 免费额度: 有限制
- QPS限制: 根据套餐

---

## Ollama

### API 文档
- 官方文档: https://github.com/ollama/ollama
- Python SDK: `pip install ollama`

### 本地部署
```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 下载模型
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

### 常用模型
- `llama2`: Meta的开源模型
- `mistral`: 高性能开源模型
- `codellama`: 代码专用模型
- `qwen`: 通义千问开源版

### 关键参数
- `temperature`: 0-1
- `num_ctx`: 上下文窗口大小
- `num_predict`: 最大生成token数

### 优势
- 完全本地运行,无网络延迟
- 无API调用费用
- 数据隐私保护

---

## 统一参数映射

不同提供商的参数名称可能不同,建议使用以下映射:

| 统一参数 | OpenAI | DashScope | GLM | Ollama |
|---------|--------|-----------|-----|--------|
| temperature | temperature | temperature | temperature | temperature |
| max_tokens | max_tokens | max_tokens | max_tokens | num_predict |
| top_p | top_p | top_p | top_p | top_p |
| stream | stream | stream | stream | stream |

---

## 错误码参考

### OpenAI
- 401: 无效的API密钥
- 429: 速率限制
- 500: 服务器错误

### DashScope
- 400: 请求参数错误
- 401: 鉴权失败
- 429: 请求过于频繁

### GLM
- InvalidAPIKey: API密钥无效
- RateLimitError: 超过速率限制
- ServiceUnavailable: 服务不可用

### Ollama
- Connection Error: 无法连接到Ollama服务
- Model Not Found: 模型未下载

---

## 成本比较 (参考)

| 提供商 | 模型 | 输入价格 | 输出价格 | 备注 |
|--------|------|---------|---------|------|
| OpenAI | GPT-3.5 | $0.0005/1K | $0.0015/1K | 性价比高 |
| OpenAI | GPT-4 | $0.01/1K | $0.03/1K | 性能最强 |
| OpenRouter | 多种 | 变动 | 变动 | 根据模型 |
| DashScope | Qwen-turbo | ¥0.008/1K | ¥0.008/1K | 国内访问快 |
| GLM | GLM-4 | ¥0.1/1K | ¥0.1/1K | 中文优化 |
| Ollama | 本地 | 免费 | 免费 | 需要GPU |

*价格仅供参考,请以官方最新定价为准*
