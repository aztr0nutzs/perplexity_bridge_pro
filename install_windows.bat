@echo off
REM Perplexity Bridge - Windows Installation Script
REM This script installs dependencies and sets up the application

echo ================================================
echo Perplexity Bridge - Windows Installation
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version
echo.

REM Check Python version (must be 3.8+)
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>nul
if errorlevel 1 (
    echo [ERROR] Python 3.8 or higher is required
    echo Current version does not meet requirements
    pause
    exit /b 1
)

echo [2/4] Creating virtual environment (recommended)...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [WARNING] Failed to create virtual environment, continuing with system Python
        set USE_VENV=0
    ) else (
        echo Virtual environment created successfully
        set USE_VENV=1
    )
)

if "%USE_VENV%"=="1" (
    echo [3/4] Activating virtual environment...
    call venv\Scripts\activate.bat
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=python
)

echo.
echo [4/4] Installing dependencies...
%PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1
%PYTHON_CMD% -m pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo [5/5] Setting up environment...
if not exist .env (
    copy env.example .env >nul 2>&1
    echo Created .env file - please edit it with your API key
) else (
    echo .env file already exists
)

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your PERPLEXITY_API_KEY
echo 2. Double-click "Launch Perplexity Bridge.lnk" or run start.bat
echo.
echo Or run manually:
echo   start.bat
echo.
pause
