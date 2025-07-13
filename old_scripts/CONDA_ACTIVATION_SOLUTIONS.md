# Conda Activation 问题解决方案

## 问题描述
在 PowerShell 中执行 `conda activate drone_308` 时出现错误：
```
CondaError: Run 'conda init' before 'conda activate'
```

即使运行了 `conda init`，问题仍然存在。

## 根本原因
- PowerShell 的执行策略限制
- Conda 的 PowerShell 集成未正确初始化
- PowerShell profile 未正确加载 conda 初始化脚本

## 解决方案

### 方案 1：使用 quick-start.bat（推荐）
最简单的解决方案，自动处理所有环境问题：
```batch
quick-start.bat
```

### 方案 2：使用 conda run
避免激活问题，直接在指定环境中运行命令：
```batch
# 启动后端服务
start-backend-conda-run.bat

# 或手动执行
conda run -n drone_308 uvicorn app.main:app --reload
```

### 方案 3：修复 PowerShell 配置
运行修复脚本：
```powershell
.\fix-conda-powershell.ps1
```

### 方案 4：使用 Anaconda Prompt
1. 打开 "Anaconda Prompt" (不是 PowerShell)
2. 运行：
   ```batch
   conda activate drone_308
   cd backend
   uvicorn app.main:app --reload
   ```

### 方案 5：使用 CMD 替代 PowerShell
在普通的命令提示符（cmd）中：
```batch
conda activate drone_308
cd backend
uvicorn app.main:app --reload
```

## 测试环境
运行测试脚本验证环境配置：
```batch
test-conda-env.bat
```

## 启动选项总结

| 方法 | 命令 | 说明 |
|------|------|------|
| 快速启动 | `quick-start.bat` | 一键启动，自动处理环境问题 |
| PowerShell | `.\start-all.ps1` | 智能检测并使用合适的方法 |
| Conda Run | `start-backend-conda-run.bat` | 使用 conda run 避免激活问题 |
| 标准启动 | `start-backend.bat` | 尝试激活，失败时自动切换到 conda run |

## 长期解决方案
1. 使用 Anaconda Prompt 而不是 PowerShell
2. 将 PowerShell 执行策略设置为 RemoteSigned：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. 确保 PowerShell profile 正确加载 conda：
   ```powershell
   notepad $PROFILE
   # 添加: & "C:\ProgramData\miniconda3\shell\condabin\conda-hook.ps1"
   ``` 