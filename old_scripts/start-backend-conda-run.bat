@echo off
echo Starting AirSim Drone Control Backend (Using conda run)...
cd backend

echo Using conda run to execute in drone_308 environment...
conda run -n drone_308 uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause 