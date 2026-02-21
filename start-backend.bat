@echo off
echo Starting NumerAI Backend...
cd /d "%~dp0"
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
