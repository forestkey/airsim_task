@echo off
echo === AirSim Drone Control - Simple Start ===
echo.
echo NOTE: Please ensure your Python environment is activated before running this script!
echo.

REM Start backend in new window
echo Starting Backend...
start "Backend" cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a bit
timeout /t 3 /nobreak > nul

REM Start frontend in new window  
echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Services starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
pause 