# 解决方案：环境变量加载时机问题

## 问题描述
- 单元测试成功（Gemini API正常工作）
- 服务运行时失败（60秒超时）

## 根本原因
1. **模块导入时机**：GeminiClient在模块导入时创建，此时环境变量可能未加载
2. **uvicorn进程**：uvicorn可能在子进程中运行，继承的环境变量不完整

## 解决方案

### 方案1：使用Python启动脚本（推荐）
```bash
cd ai-service
python start_service.py
```
优点：确保环境变量在启动uvicorn之前加载

### 方案2：使用批处理脚本
```bash
cd ai-service
start-service-fixed.bat
```
优点：自动从.env加载环境变量

### 方案3：手动设置环境变量
```bash
cd ai-service
# Windows CMD
set HTTP_PROXY=http://127.0.0.1:7897
set HTTPS_PROXY=http://127.0.0.1:7897
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 方案4：使用Python -m运行
```bash
cd ai-service
python -c "from dotenv import load_dotenv; load_dotenv(); import uvicorn; uvicorn.run('app.main:app', host='0.0.0.0', port=8001, reload=True)"
```

## 已实施的代码改进
1. **延迟初始化**：GeminiClient改为延迟创建，避免模块导入时的问题
2. **环境变量验证**：启动脚本会验证关键环境变量

## 验证步骤
1. 运行诊断测试：
   ```bash
   python test_env_timing.py
   ```

2. 使用新的启动方式启动服务

3. 测试AI助手功能

## 预期结果
- Gemini API通过代理正常工作
- 不再出现60秒超时错误
- AI助手可以正常对话和控制无人机 