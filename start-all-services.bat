@echo off
echo === Starting AirSim Drone Control System with AI Chat ===
echo.
echo This script will start:
echo - Drone Control Service (Port 8000)
echo - AI Chat Service (Port 8001)
echo - Frontend (Port 3000)
echo.
echo NOTE: Please ensure you have activated the appropriate Python environments!
echo.
pause

REM Start Drone Control Service
echo Starting Drone Control Service...
start "Drone Service" cmd /k "cd backend && echo Please activate your Python environment (e.g., conda activate airsim) && echo Then run: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Start AI Chat Service
echo Starting AI Chat Service...
start "AI Service" cmd /k "cd ai-service && echo Please activate your Python 3.12 environment (e.g., conda activate ai-chat) && echo Then run: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"

REM Wait a bit
timeout /t 3 /nobreak > nul

REM Start Frontend
echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo All service windows have been opened!
echo.
echo Please manually activate the Python environments in each window and run the commands shown.
echo.
echo Service URLs:
echo - Drone API: http://localhost:8000
echo - AI API: http://localhost:8001
echo - Frontend: http://localhost:3000
echo.
echo API Documentation:
echo - Drone API Docs: http://localhost:8000/docs
echo - AI API Docs: http://localhost:8001/docs
echo.
pause 