@echo off
echo Starting AirSim Drone Control Backend...
echo.
echo NOTE: Please ensure your Python environment is activated!
echo.
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause 