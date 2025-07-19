# 修复AI助手回答失败问题

## 问题描述
AI助手无法正常回答，可能出现以下情况：
- 显示"回答失败"
- 无法连接
- API错误

## 诊断步骤

### 1. 检查AI服务是否正常运行
查看AI服务（端口8001）的控制台输出，检查是否有错误信息。

### 2. 检查API Key配置
确保 `ai-service/.env` 文件存在并包含有效的API key：
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. 测试Gemini API连接
```bash
cd ai-service
python test_gemini.py
```

### 4. 重启AI服务
```bash
# 停止当前服务 (Ctrl+C)
# 重新启动
cd ai-service
conda activate drone_312  # 或你的Python 3.12环境
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 常见错误和解决方案

### 错误1: AttributeError: module 'google.generativeai' has no attribute 'Tool'
**原因**: API版本不兼容
**解决**: 已修复，使用基于提示的工具调用

### 错误2: TypeError: GenerativeModel.__init__() got an unexpected keyword argument
**原因**: 模型初始化参数不兼容
**解决**: 已修复，使用最小化配置

### 错误3: API Key错误
**症状**: 显示 "INVALID_API_KEY" 或类似错误
**解决**:
1. 检查 `.env` 文件中的 API key 是否正确
2. 确保 API key 有效且未过期
3. 在 Google AI Studio 重新生成 API key

### 错误4: 连接失败
**症状**: WebSocket连接失败或超时
**解决**:
1. 确保AI服务运行在8001端口
2. 检查防火墙设置
3. 确保前端配置正确指向8001端口

## 快速修复脚本
```bash
# 1. 重新安装依赖
cd ai-service
pip install --upgrade google-generativeai

# 2. 验证环境变量
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key exists:', bool(os.getenv('GEMINI_API_KEY')))"

# 3. 重启服务
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 验证修复
1. 刷新前端页面
2. 在AI助手中输入："你好"
3. 应该收到正常的回复

## 调试模式
如需更详细的错误信息，可以设置日志级别：
```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

## 备用方案
如果Gemini API持续出现问题，可以：
1. 检查Google AI Studio的服务状态
2. 尝试使用不同的模型（如 gemini-1.5-flash）
3. 暂时使用主后端的简单聊天功能（端口8000） 