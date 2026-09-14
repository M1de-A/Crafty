@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo          CRAFTY 2.6 - START
echo ========================================

if not exist ".venv\Scripts\python.exe" (
    echo [1/4] Creating virtual environment...
    py -m venv .venv
    if errorlevel 1 goto :error
)

echo [2/4] Installing/updating dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo [3/4] Applying database migrations...
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto :error

.venv\Scripts\python.exe manage.py seed_crafty
if errorlevel 1 goto :error

.venv\Scripts\python.exe manage.py crafty_check
if errorlevel 1 goto :error

echo [4/4] Starting Crafty...
echo.
echo Open: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server.
echo.
.venv\Scripts\python.exe manage.py runserver
exit /b 0

:error
echo.
echo CRAFTY START ERROR. Read the message above.
pause
exit /b 1
