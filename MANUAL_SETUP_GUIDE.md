# 手动环境配置指南

## 环境要求
- Python 3.8 或 3.9
- Node.js 16+
- AirSim 仿真器

## 后端环境配置

### 方法 1：使用 Conda（推荐）
```bash
# 1. 创建 conda 环境
conda create -n drone python=3.9 -y

# 2. 激活环境
conda activate drone

# 3. 安装依赖包
cd backend
pip install -r requirements.txt
```

### 方法 2：使用 venv
```bash
# 1. 创建虚拟环境
cd backend
python -m venv venv

# 2. 激活环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖包
pip install -r requirements.txt
```

### 方法 3：使用 Anaconda Prompt（如果 PowerShell 有问题）
1. 打开 "Anaconda Prompt"（不是 PowerShell）
2. 执行上述 conda 命令

## 前端环境配置
```bash
cd frontend
npm install
```

## 验证环境
```bash
# 后端验证
python backend/test_env.py

# 前端验证
cd frontend
npm list
```

## 启动服务

### 后端启动
```bash
# 确保在激活的环境中
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端启动
```bash
cd frontend
npm run dev
```

## 常见问题

### 如果 conda activate 在 PowerShell 失败
使用以下任一方法：
- 使用 Anaconda Prompt
- 使用 cmd 而不是 PowerShell
- 使用 `conda run -n drone python -m uvicorn app.main:app --reload`

### 端口冲突
- 后端改端口：添加 `--port 8001`
- 前端改端口：`PORT=3001 npm run dev` 