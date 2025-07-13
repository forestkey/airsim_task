# 如何运行 AirSim 无人机控制系统

## 步骤 1：配置 Python 环境

### 选项 A - Conda（推荐）
```bash
conda create -n airsim python=3.9 -y
conda activate airsim
cd backend
pip install -r requirements.txt
```

### 选项 B - Python venv
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

## 步骤 2：安装前端依赖
```bash
cd frontend
npm install
```

## 步骤 3：启动 AirSim
运行 AirSim 仿真器，选择多旋翼无人机模式

## 步骤 4：启动服务

### 最简单方式
在激活 Python 环境后：
```bash
start-simple.bat
```

### 手动启动
**后端**（在激活的 Python 环境中）：
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**前端**（新终端窗口）：
```bash
cd frontend
npm run dev
```

## 步骤 5：使用系统
打开浏览器访问 http://localhost:3000

## 常见问题

### conda activate 失败
- 使用 Anaconda Prompt 而不是 PowerShell
- 或使用 `conda run -n airsim uvicorn app.main:app --reload`

### 端口被占用
- 后端改端口：`--port 8001`
- 前端改端口：`PORT=3001 npm run dev`

### 更多帮助
参考 [MANUAL_SETUP_GUIDE.md](MANUAL_SETUP_GUIDE.md) 