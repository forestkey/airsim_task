# AI 聊天功能配置指南

## 系统架构

本系统采用双服务架构：
- **无人机控制服务**（Python 3.9）：端口 8000
- **AI 聊天服务**（Python 3.12）：端口 8001

两个服务通过 MCP (Model Context Protocol) 进行通信。

## 环境配置

### 1. 无人机控制服务（已有环境）

```bash
# 使用现有的 Python 3.9 环境
conda activate airsim  # 或您的环境名
cd backend
pip install -r requirements.txt
```

### 2. AI 聊天服务（新环境）

```bash
# 创建 Python 3.12 环境
conda create -n ai-chat python=3.12 -y
conda activate ai-chat

# 安装依赖
cd ai-service
pip install -r requirements.txt

# 配置环境变量
create_env.bat  # Windows
# 或
cp env_template.txt .env
# 编辑 .env 文件，配置必要的参数

# 测试配置
python test_gemini.py
```

### 3. 前端配置

```bash
cd frontend
npm install
```

## 启动服务

### 方式 1：分别启动每个服务

**1. 启动无人机控制服务**
```bash
# 终端 1
conda activate airsim
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**2. 启动 AI 聊天服务**
```bash
# 终端 2
conda activate ai-chat
cd ai-service
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**3. 启动前端**
```bash
# 终端 3
cd frontend
npm run dev
```

### 方式 2：使用启动脚本

创建 `start-all-services.bat`：
```batch
@echo off
echo Starting all services...

REM Start Drone Control Service
start "Drone Service" cmd /k "conda activate airsim && cd backend && uvicorn app.main:app --port 8000 --reload"

REM Start AI Chat Service
start "AI Service" cmd /k "conda activate ai-chat && cd ai-service && uvicorn app.main:app --port 8001 --reload"

REM Wait a bit for services to start
timeout /t 5 /nobreak > nul

REM Start Frontend
start "Frontend" cmd /k "cd frontend && npm run dev"

echo All services are starting...
echo Drone API: http://localhost:8000
echo AI API: http://localhost:8001
echo Frontend: http://localhost:3000
pause
```

## 服务验证

### 1. 检查服务健康状态
- 无人机服务：http://localhost:8000/health
- AI 服务：http://localhost:8001/health
- API 文档：
  - 无人机：http://localhost:8000/docs
  - AI：http://localhost:8001/docs

### 2. 前端访问
打开浏览器访问 http://localhost:3000，您应该能看到：
- 原有的无人机控制界面
- 右下角的 AI 助手对话框

## 使用说明

### AI 助手功能
1. **自然语言控制**
   - "让无人机起飞到20米"
   - "移动到坐标 (10, 20, -15)"
   - "降落"
   - "紧急停止"

2. **状态查询**
   - "查看无人机状态"
   - "当前位置是什么"
   - "电池电量多少"

3. **复杂任务**
   - "起飞到10米，然后向前飞行20米"
   - "在当前位置悬停30秒"

### MCP 工具说明
AI 可以调用以下工具：
- `takeoff`: 起飞到指定高度
- `land`: 降落
- `move_to_position`: 移动到指定位置
- `hover`: 悬停
- `get_drone_state`: 获取状态
- `emergency_stop`: 紧急停止

## 故障排除

### 1. AI 服务无法连接到无人机服务
- 检查两个服务是否都已启动
- 确认端口 8000 和 8001 没有被占用
- 检查 MCP_AUTH_TOKEN 配置是否一致

### 2. 前端无法连接到 AI 服务
- 检查 CORS 配置
- 确认 WebSocket 连接地址正确
- 查看浏览器控制台错误信息

### 3. Gemini API 错误
- 检查 API 密钥是否正确
- 确认网络可以访问 Google API
- 查看 AI 服务日志
- 如遇到 `AttributeError: module 'google.generativeai' has no attribute 'Tool'` 错误，参见 `ai-service/FIX_INSTRUCTIONS.md`

## 安全注意事项

1. **API 密钥管理**
   - 不要将 `.env` 文件提交到版本控制
   - 定期更换 MCP_AUTH_TOKEN

2. **服务隔离**
   - AI 服务只能通过 MCP 协议访问无人机
   - 实施适当的请求频率限制

3. **生产部署**
   - 使用 HTTPS
   - 配置防火墙规则
   - 实施用户认证

## 扩展开发

### 添加新的工具
1. 在 `backend/app/mcp/server.py` 中添加工具处理函数
2. 在 `ai-service/app/mcp/tools.py` 中添加工具定义
3. 更新系统提示词以包含新工具说明

### 切换 AI 模型
修改 `ai-service/.env` 中的 `GEMINI_MODEL` 参数，支持：
- gemini-1.5-pro
- gemini-1.5-flash
- 其他 Gemini 模型

## 性能优化

1. **缓存对话历史**
   - 当前实现在内存中
   - 可以添加 Redis 支持

2. **异步处理**
   - 工具调用已实现异步
   - 可以添加任务队列

3. **负载均衡**
   - 可以部署多个 AI 服务实例
   - 使用 Nginx 进行负载均衡 