@echo off
REM ================================================================
REM    SHADOWSCAN PRO - Offensive Security Framework
REM    Developed by ROHAIB TECHNICAL | +92 306 3844400
REM ================================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo    SHADOWSCAN PRO - Advanced Offensive Security
echo    Developed by ROHAIB TECHNICAL ^| +92 306 3844400
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [INFO] Virtual environment not found, creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

REM Run ShadowScan Pro
python -m shadowscan %*

endlocal