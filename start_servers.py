#!/usr/bin/env python3
"""
Unified Server Startup Script for MindSpark AI
Starts both frontend (React) and backend (FastAPI) servers simultaneously
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.ENDC}")

def check_dependencies():
    """Check if required dependencies are available"""
    print_colored("🔍 Checking dependencies...", Colors.OKBLUE)
    
    # Check if Node.js is available
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_colored(f"✅ Node.js version: {result.stdout.strip()}", Colors.OKGREEN)
        else:
            raise subprocess.CalledProcessError(result.returncode, 'node')
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_colored("❌ Node.js not found. Please install Node.js", Colors.FAIL)
        return False
    
    # Check if Python virtual environment exists
    backend_path = Path("mindspark-ai/backend")
    venv_path = backend_path / "venv"
    
    if not venv_path.exists():
        print_colored("❌ Python virtual environment not found in backend/venv", Colors.FAIL)
        print_colored("Please run: cd mindspark-ai/backend && python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt", Colors.WARNING)
        return False
    
    print_colored("✅ Python virtual environment found", Colors.OKGREEN)
    
    # Check if package.json exists for frontend
    frontend_path = Path("mindspark-ai/frontend")
    package_json = frontend_path / "package.json"
    
    if not package_json.exists():
        print_colored("❌ Frontend package.json not found", Colors.FAIL)
        return False
    
    print_colored("✅ Frontend package.json found", Colors.OKGREEN)
    return True

def start_backend_server():
    """Start the FastAPI backend server"""
    print_colored("🚀 Starting Backend Server (FastAPI)...", Colors.HEADER)
    
    backend_path = Path("mindspark-ai/backend")
    
    # Change to backend directory
    os.chdir(backend_path)
    
    # Add current directory to Python path and start server
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_path.absolute())
    
    try:
        # Start FastAPI server using uvicorn
        backend_process = subprocess.Popen([
            "venv\\Scripts\\python.exe", 
            "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], env=env)
        
        print_colored("✅ Backend server starting on http://localhost:8000", Colors.OKGREEN)
        return backend_process
        
    except Exception as e:
        print_colored(f"❌ Failed to start backend server: {e}", Colors.FAIL)
        return None

def start_frontend_server():
    """Start the React frontend server"""
    print_colored("🚀 Starting Frontend Server (React)...", Colors.HEADER)
    
    frontend_path = Path("mindspark-ai/frontend")
    
    # Change to frontend directory
    os.chdir(frontend_path)
    
    try:
        # Start React development server
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], shell=True)
        
        print_colored("✅ Frontend server starting on http://localhost:3000", Colors.OKGREEN)
        return frontend_process
        
    except Exception as e:
        print_colored(f"❌ Failed to start frontend server: {e}", Colors.FAIL)
        return None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print_colored("\n🛑 Shutting down servers...", Colors.WARNING)
    if 'backend_process' in globals() and backend_process:
        backend_process.terminate()
    if 'frontend_process' in globals() and frontend_process:
        frontend_process.terminate()
    sys.exit(0)

def main():
    """Main function to start both servers"""
    print_colored("🌟 MindSpark AI Server Startup", Colors.HEADER)
    print_colored("=" * 50, Colors.HEADER)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Store original directory
    original_dir = os.getcwd()
    
    # Start backend server in a separate thread
    def start_backend():
        global backend_process
        os.chdir(original_dir)
        backend_process = start_backend_server()
    
    # Start frontend server in a separate thread
    def start_frontend():
        global frontend_process
        time.sleep(3)  # Wait a bit for backend to start
        os.chdir(original_dir)
        frontend_process = start_frontend_server()
    
    # Start both servers
    backend_thread = threading.Thread(target=start_backend)
    frontend_thread = threading.Thread(target=start_frontend)
    
    backend_thread.daemon = True
    frontend_thread.daemon = True
    
    backend_thread.start()
    frontend_thread.start()
    
    # Wait a moment for servers to start
    time.sleep(5)
    
    print_colored("\n🎉 Both servers are starting up!", Colors.OKGREEN)
    print_colored("Frontend: http://localhost:3000", Colors.OKCYAN)
    print_colored("Backend:  http://localhost:8000", Colors.OKCYAN)
    print_colored("API Docs: http://localhost:8000/docs", Colors.OKCYAN)
    print_colored("\nPress Ctrl+C to stop both servers", Colors.WARNING)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()