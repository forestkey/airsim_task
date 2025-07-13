# AirSim Drone Control System

基于 AirSim 的无人机控制系统，提供完整的后端控制服务和前端操作界面。

## 功能特性

### 后端功能
- **飞行控制**: 起飞、降落、移动、悬停、紧急停止
- **状态监控**: 实时位置、姿态、电池状态
- **WebSocket**: 实时遥测数据推送（10Hz）
- **安全限制**: 高度限制（100m）、速度限制（20m/s）、地理围栏（500m）
- **RESTful API**: 完整的 API 文档（OpenAPI/Swagger）

### 前端功能
- **实时状态显示**: 位置、高度、速度、电池等信息
- **飞行控制面板**: 直观的控制按钮和滑块
- **数据可视化**: 实时遥测数据图表
- **3D视图**: 无人机位置可视化
- **响应式设计**: 支持不同屏幕尺寸

## 快速开始

### 1. 系统要求
- Python 3.8 或 3.9
- Node.js 16+
- AirSim 仿真器

### 2. 环境配置

详细配置步骤请参考：[MANUAL_SETUP_GUIDE.md](MANUAL_SETUP_GUIDE.md)

**快速配置示例（使用 Conda）**：
```bash
# 后端
conda create -n airsim python=3.9 -y
conda activate airsim
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 3. 启动服务

**简单启动（需先激活 Python 环境）**：
```bash
start-simple.bat
```

**或手动启动**：
```bash
# 后端（在激活的环境中）
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 前端（新终端）
cd frontend
npm run dev
```

### 4. 访问系统
- 前端界面：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

## 使用说明

1. 启动 AirSim 仿真器
2. 启动后端和前端服务
3. 打开浏览器访问 http://localhost:3000
4. 使用界面控制无人机

## 项目结构

```
airsim_task/
├── backend/
│   ├── app/
│   │   ├── api/        # API 路由
│   │   ├── core/       # 核心功能
│   │   └── models/     # 数据模型
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/ # React 组件
│   │   ├── hooks/      # 自定义 Hooks
│   │   └── types/      # TypeScript 类型
│   └── package.json
├── MANUAL_SETUP_GUIDE.md  # 详细环境配置指南
└── README.md
```

## 技术栈

- **后端**: FastAPI, AirSim Python Client, WebSocket
- **前端**: Next.js, TypeScript, Tailwind CSS, Recharts

## 许可证

MIT License