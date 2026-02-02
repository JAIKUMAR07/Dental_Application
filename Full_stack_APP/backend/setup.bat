@echo off
REM Quick Setup Script for Dental AI System (Windows)

echo ====================================
echo Dental AI System - Quick Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo.
    echo [2/4] Virtual environment already exists, skipping...
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo [4/4] Installing dependencies...
echo This may take a few minutes, please wait...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Make sure your model files are in app\models\ directory:
echo    - DENTAL_MODEL_BEST.keras
echo    - GINGIVITIS_MODEL_AUGMENTED.keras
echo.
echo 2. Run the application:
echo    python run.py
echo.
echo 3. Access at: http://localhost:8000
echo.
pause
