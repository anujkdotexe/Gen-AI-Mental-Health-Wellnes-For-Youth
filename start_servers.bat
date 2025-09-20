@echo off
REM Windows batch script to start both MindSpark AI servers
REM This provides an alternative to the Python script for Windows users

echo.
echo ========================================
echo    MindSpark AI Server Startup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js first.
    pause
    exit /b 1
)

echo [INFO] Starting MindSpark AI servers...
echo.

REM Start backend server in a new window
echo [INFO] Starting Backend Server (FastAPI)...
start "MindSpark AI Backend" cmd /k "cd /d \"%~dp0backend\" && .\\venv\\Scripts\\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 >nul

REM Start frontend server in a new window
echo [INFO] Starting Frontend Server (React)...
start "MindSpark AI Frontend" cmd /k "cd /d \"%~dp0frontend\" && npm start"

echo.
echo [SUCCESS] Both servers are starting up!
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the server windows to stop the servers.
echo.
pause