@echo off
REM Celery Worker Startup Script (Windows)
REM 
REM Usage:
REM   start_celery_worker.bat          - Interactive mode (choose foreground/background)
REM   start_celery_worker.bat fg       - Start worker (foreground)
REM   start_celery_worker.bat bg       - Start worker (background)
REM   start_celery_worker.bat stop     - Stop worker
REM   start_celery_worker.bat restart  - Restart worker

setlocal

if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="fg" goto foreground
if "%1"=="bg" goto start

:menu
echo ========================================
echo Celery Worker (Video Processing)
echo ========================================
echo.
echo Select startup mode:
echo   1. Foreground mode (real-time logs, press Ctrl+C to stop)
echo   2. Background mode (logs saved to file)
echo.
set /p choice="Enter choice (1/2) or press Enter for foreground [1]: "

if "%choice%"=="2" goto start
if "%choice%"=="bg" goto start
goto foreground

:foreground
echo.
echo ========================================
echo Starting in FOREGROUND mode
echo ========================================
echo.
echo Logs will be displayed in real-time
echo Press Ctrl+C to stop the worker
echo.
celery -A config.celery worker --concurrency=2 --prefetch-multiplier=2 --max-tasks-per-child=100 --loglevel=INFO -P solo
exit /b 0

:start
echo.
echo ========================================
echo Starting in BACKGROUND mode
echo ========================================
echo.

REM Create a VBScript to run Celery completely hidden
set TEMP_VBS=%TEMP%\celery_start.vbs

echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP_VBS%"
echo WshShell.Run "cmd /c celery -A config.celery worker --concurrency=2 --prefetch-multiplier=2 --max-tasks-per-child=100 --loglevel=INFO --logfile=logs/celery.log -P solo", 0, False >> "%TEMP_VBS%"

cscript //nologo "%TEMP_VBS%"
del "%TEMP_VBS%"

timeout /t 2 /nobreak >nul

echo Celery worker started in background (completely hidden)
echo Log file: logs\celery.log
echo.
echo To view log in real-time:
echo   Get-Content logs\celery.log -Tail 20 -Wait
echo.
echo To stop the worker:
echo   .\start_celery_worker.bat stop
echo.
pause
exit /b 0

:stop
echo Stopping Celery worker...
echo.

REM Kill all python processes running celery
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "celery"') do (
    taskkill /F /PID %%i >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo Celery worker stopped
pause
exit /b 0

:restart
call :stop
timeout /t 3 /nobreak >nul
call :start
exit /b 0