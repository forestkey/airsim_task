# AirSim 无人机控制服务后端

基于 FastAPI 和 AirSim 的无人机控制服务后端。

## 功能特性

- 基本飞行控制（起飞、降落、移动、悬停）
- 实时状态监控（位置、姿态、速度）
- WebSocket 实时数据推送
- 安全限制（高度限制、速度限制、地理围栏）
- RESTful API 接口

## 安装要求

- Python 3.9+ (推荐使用 conda 或 uv 管理)
- AirSim 仿真器

## 环境设置

### 方法 1: 使用 Conda (推荐)

```bash
# Windows
.\setup-env.ps1 conda

# Linux/Mac
./setup-env.sh conda
```

### 方法 2: 使用 uv (更快的包管理器)

```bash
# Windows
.\setup-env.ps1 uv

# Linux/Mac
./setup-env.sh uv
```

### 方法 3: 传统 venv

```bash
# Windows
.\setup-env.ps1 venv

# Linux/Mac
./setup-env.sh venv
```

## 快速开始

1. 设置环境（首次运行）：
```bash
# 选择一种方法设置环境
.\setup-env.ps1 conda  # Windows
./setup-env.sh conda   # Linux/Mac
```

2. 激活环境：
```bash
# Conda
conda activate airsim-drone-control

# uv 或 venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/Mac
```

2. 启动 AirSim 仿真器

3. 运行服务：
```bash
python -m app.main
# 或使用 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API 文档

服务启动后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要接口

### 控制接口
- `POST /api/v1/control/arm` - 解锁无人机
- `POST /api/v1/control/takeoff` - 起飞
- `POST /api/v1/control/land` - 降落
- `POST /api/v1/control/move` - 移动控制
- `POST /api/v1/control/hover` - 悬停
- `POST /api/v1/control/emergency` - 紧急停止

### 状态接口
- `GET /api/v1/status/position` - 获取位置
- `GET /api/v1/status/attitude` - 获取姿态
- `GET /api/v1/status/state` - 获取完整状态
- `WebSocket /api/v1/status/ws` - 实时状态流

## 配置说明

主要配置项在 `app/core/config.py` 中：
- `MAX_ALTITUDE`: 最大飞行高度（默认100米）
- `MAX_SPEED`: 最大飞行速度（默认20米/秒）
- `GEOFENCE_RADIUS`: 地理围栏半径（默认500米）
- `WS_MESSAGE_INTERVAL`: WebSocket 消息间隔（默认0.1秒） 