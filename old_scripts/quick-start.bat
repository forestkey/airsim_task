@echo off
echo === AirSim Drone Control Quick Start ===
echo.

REM Start backend using conda run in new window
echo Starting Backend Service (using conda run)...
start "AirSim Backend" cmd /k "cd backend && conda run -n drone_308 uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend in new window
echo Starting Frontend Service...
start "AirSim Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo Services are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul 