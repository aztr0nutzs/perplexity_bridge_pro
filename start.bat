@echo off
REM Perplexity Bridge - Windows Launcher
REM This script starts the Perplexity Bridge server and opens the browser

echo Starting Perplexity Bridge...

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please run install_windows.bat first
    pause
    exit /b 1
)

REM Start the server
python start.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Server stopped with an error.
    pause
)
