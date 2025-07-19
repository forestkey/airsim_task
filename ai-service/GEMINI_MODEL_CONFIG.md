# Gemini 模型配置说明

## 当前配置
默认使用模型：`gemini-2.5-flash` (Gemini 2.5 Flash)

## 可用模型
Google Gemini 提供以下模型：
- `gemini-pro` - 标准版本
- `gemini-1.5-pro` - 1.5 Pro版本
- `gemini-1.5-flash` - 1.5 Flash版本
- `gemini-2.5-pro` - 2.5 Pro版本
- `gemini-2.5-flash` - 2.5 Flash版本（最新、推荐）

## 更改模型

### 方法1：修改 .env 文件
编辑 `ai-service/.env` 文件，添加或修改：
```
GEMINI_MODEL=gemini-2.5-flash
```

### 方法2：修改默认配置
编辑 `ai-service/app/core/config.py`：
```python
GEMINI_MODEL: str = "gemini-2.5-flash"
```

### 方法3：启动时设置环境变量
```bash
# Windows CMD
set GEMINI_MODEL=gemini-2.5-flash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Windows PowerShell
$env:GEMINI_MODEL="gemini-2.5-flash"
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 模型特点

### Gemini 2.5 Flash
- ✅ 最新版本（2024）
- ✅ 响应速度极快
- ✅ 优秀的中文理解和生成能力
- ✅ 适合实时控制场景
- ✅ 支持复杂的工具调用

### Gemini 2.5 Pro
- ✅ 更强大的推理能力
- ✅ 适合复杂任务
- ✅ 响应时间稍长

### 模型选择建议
- **推荐**: `gemini-2.5-flash` - 最新、快速、性价比高
- **高级**: `gemini-2.5-pro` - 更强大但响应较慢
- **备选**: `gemini-1.5-flash` - 较旧但稳定的版本

## 验证模型
运行测试脚本查看当前使用的模型：
```bash
cd ai-service
python test_connections.py
```

## 注意事项
1. 如果指定的模型不可用，系统会自动回退到 `gemini-1.5-flash`
2. 模型名称必须与Google API支持的名称完全匹配
3. 实验版模型（带-exp后缀）可能会有变动 