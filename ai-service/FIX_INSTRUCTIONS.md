# AI 服务修复说明

## 问题描述
原始的 Gemini 客户端使用了可能不存在的 API 特性（`genai.Tool`），导致启动失败。

## 已执行的修复

1. **更新了 Gemini 客户端**
   - 使用基于提示的工具调用方法
   - 不依赖可能不存在的 API 特性
   - 更稳定和兼容

2. **更新了依赖版本**
   - `google-generativeai>=0.5.0`

## 设置步骤

### 1. 更新依赖
```bash
conda activate ai-chat  # 或您的环境名
cd ai-service
pip install -r requirements.txt
```

### 2. 创建环境配置
```bash
# Windows
create_env.bat

# 或手动
copy env_template.txt .env
```

### 3. 测试配置
```bash
python test_gemini.py
```

如果测试通过，您应该看到：
- ✓ google-generativeai 包已安装
- ✓ GEMINI_API_KEY 已设置
- ✓ API 连接成功
- ✓ 客户端测试成功

### 4. 启动服务
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 工具调用格式

新的实现使用基于提示的方法。AI 会生成如下格式的工具调用：

```
我将让无人机起飞到15米高度。

[TOOL_CALL]
{
  "tool": "takeoff",
  "parameters": {"altitude": 15}
}
[/TOOL_CALL]
```

系统会自动解析并执行这些工具调用。

## 故障排除

### 如果仍然遇到导入错误
1. 确保在正确的 conda 环境中
2. 重新安装 google-generativeai：
   ```bash
   pip uninstall google-generativeai
   pip install google-generativeai
   ```

### 如果 API 连接失败
1. 检查 API 密钥是否正确
2. 检查网络连接
3. 尝试使用代理（如果需要）：
   ```python
   # 在 .env 中添加
   HTTP_PROXY=http://your-proxy:port
   HTTPS_PROXY=http://your-proxy:port
   ``` 