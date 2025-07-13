# AirSim 无人机控制系统部署指南

## 环境要求

### 系统要求
- Windows 10/11 或 Linux
- Python 3.9+
- Node.js 16+
- AirSim 仿真器

### 硬件要求
- CPU: 4核心以上
- RAM: 8GB以上
- GPU: 支持DirectX 11（用于AirSim）

## 快速部署

### Windows 用户

1. **一键启动（推荐）**
   ```powershell
   # 使用PowerShell运行
   .\start-all.ps1
   ```

2. **分别启动**
   - 后端：双击 `start-backend.bat`
   - 前端：双击 `start-frontend.bat`

### Linux/Mac 用户

1. **启动后端**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **启动前端**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 详细配置

### 1. AirSim 配置

确保 AirSim 的 `settings.json` 配置如下：

```json
{
  "SettingsVersion": 1.2,
  "SimMode": "Multirotor",
  "Vehicles": {
    "SimpleFlight": {
      "VehicleType": "SimpleFlight",
      "DefaultVehicleState": "Armed"
    }
  }
}
```

### 2. 后端配置

创建 `backend/.env` 文件：

```env
# AirSim连接配置
AIRSIM_IP=127.0.0.1
AIRSIM_PORT=41451

# 安全限制
MAX_ALTITUDE=100.0
MAX_SPEED=20.0
GEOFENCE_RADIUS=500.0
```

### 3. 前端配置

创建 `frontend/.env.local` 文件：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 部署步骤

### 1. 启动 AirSim

1. 启动 AirSim 仿真器
2. 等待场景加载完成
3. 确认无人机已出现在场景中

### 2. 启动后端服务

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

验证后端是否正常：
- 访问 http://localhost:8000/docs 查看API文档
- 检查终端是否显示 "Successfully connected to AirSim"

### 3. 启动前端服务

```bash
cd frontend
npm run dev
```

访问 http://localhost:3000 即可使用控制界面

## 常见问题

### 1. 无法连接到 AirSim

**问题**：后端显示 "Failed to connect to AirSim"

**解决方案**：
- 确认 AirSim 已启动
- 检查防火墙设置
- 验证端口 41451 未被占用

### 2. WebSocket 连接失败

**问题**：前端显示 "未连接"

**解决方案**：
- 确认后端服务正在运行
- 检查浏览器控制台错误信息
- 确认 CORS 设置正确

### 3. 无人机无响应

**问题**：点击控制按钮无反应

**解决方案**：
- 确认无人机已解锁（ARM）
- 检查是否超出安全限制
- 查看后端日志错误信息

## 性能优化

### 1. 降低 WebSocket 频率

如果网络延迟较高，可以调整 `backend/app/core/config.py`：

```python
WS_MESSAGE_INTERVAL: float = 0.2  # 改为200ms
```

### 2. 限制遥测数据点

修改 `frontend/components/drone/TelemetryChart.tsx`：

```typescript
maxDataPoints = 30  // 减少数据点数量
```

## 生产环境部署

### 1. 后端部署

使用 Gunicorn + Nginx：

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. 前端部署

构建生产版本：

```bash
npm run build
npm start
```

### 3. 使用 Docker

```dockerfile
# 后端 Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 安全建议

1. **生产环境**：启用 HTTPS
2. **访问控制**：添加身份验证
3. **限流**：实施 API 速率限制
4. **监控**：部署日志和性能监控

## 技术支持

如遇到问题，请检查：
1. 系统日志：`backend/logs/`
2. API 文档：http://localhost:8000/docs
3. 浏览器控制台错误信息 