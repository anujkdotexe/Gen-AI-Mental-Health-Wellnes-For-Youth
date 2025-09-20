# PowerShell script to start both MindSpark AI servers
# This is optimized for PowerShell and provides better error handling

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   MindSpark AI Server Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "[INFO] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Please install Python first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Node.js not found"
    }
    Write-Host "[INFO] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found. Please install Node.js first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[INFO] Starting MindSpark AI servers..." -ForegroundColor Yellow
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $scriptDir "backend"
$frontendDir = Join-Path $scriptDir "frontend"

# Check if directories exist
if (-not (Test-Path $backendDir)) {
    Write-Host "[ERROR] Backend directory not found: $backendDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path $frontendDir)) {
    Write-Host "[ERROR] Frontend directory not found: $frontendDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start backend server in a new PowerShell window
Write-Host "[INFO] Starting Backend Server (FastAPI)..." -ForegroundColor Yellow
$backendScript = @"
Set-Location '$backendDir'
if (Test-Path '.\venv\Scripts\Activate.ps1') {
    & '.\venv\Scripts\Activate.ps1'
    Write-Host 'Virtual environment activated' -ForegroundColor Green
} else {
    Write-Host 'Virtual environment not found, using system Python' -ForegroundColor Yellow
}
Write-Host 'Starting FastAPI server...' -ForegroundColor Green
if (Test-Path '.\start_server.py') {
    python start_server.py
} else {
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend server in a new PowerShell window
Write-Host "[INFO] Starting Frontend Server (React)..." -ForegroundColor Yellow
$frontendScript = @"
Set-Location '$frontendDir'
Write-Host 'Starting React development server...' -ForegroundColor Green
npm start
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript -WindowStyle Normal

Write-Host ""
Write-Host "[SUCCESS] Both servers are starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close the server windows to stop the servers." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"