# AirSim Drone Control System Startup Script

Write-Host "Starting AirSim Drone Control System..." -ForegroundColor Green

# Check if backend environment exists
$backendEnvExists = $false

# Check for conda environment drone_308
$condaEnvs = & conda info --envs 2>$null
if ($condaEnvs -match "drone_308") {
    $backendEnvExists = $true
    Write-Host "Found conda environment: drone_308" -ForegroundColor Green
} elseif (Test-Path "backend\.venv") {
    $backendEnvExists = $true
    Write-Host "Found virtual environment: backend\.venv" -ForegroundColor Green
} elseif (Test-Path "backend\venv") {
    $backendEnvExists = $true
    Write-Host "Found virtual environment: backend\venv" -ForegroundColor Green
}

if (-not $backendEnvExists) {
    Write-Host "Conda environment 'drone_308' not found!" -ForegroundColor Red
    Write-Host "Please make sure you have created and configured the 'drone_308' conda environment." -ForegroundColor Yellow
    Write-Host "The environment should have all packages from backend\requirements.txt installed." -ForegroundColor Yellow
    exit
}

# Start backend in new terminal using conda run
Write-Host "Starting Backend Service..." -ForegroundColor Yellow
if ($condaEnvs -match "drone_308") {
    # Use conda run to avoid activation issues
    Start-Process cmd -ArgumentList "/k", "cd backend && conda run -n drone_308 uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
} elseif (Test-Path "backend\.venv") {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; & .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; & .\venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend in new terminal
Write-Host "Starting Frontend Service..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "cd frontend && npm install && npm run dev"

Write-Host "`nServices are starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n提示: 如果看到 conda activate 错误，请忽略，服务仍会正常启动。" -ForegroundColor Yellow
Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 