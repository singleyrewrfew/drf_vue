@echo off
REM Celery Beat Startup Script (Windows)
REM 
REM Usage:
REM   start_celery_beat.bat          - Interactive mode (choose foreground/background)
REM   start_celery_beat.bat fg       - Start beat (foreground)
REM   start_celery_beat.bat bg       - Start beat (background)
REM   start_celery_beat.bat stop     - Stop beat
REM   start_celery_beat.bat restart  - Restart beat

setlocal

if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="fg" goto foreground
if "%1"=="bg" goto start

:menu
echo ========================================
echo Celery Beat (Scheduled Tasks)
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
echo Press Ctrl+C to stop
echo.
celery -A config.celery beat --loglevel=INFO
exit /b 0

:start
echo.
echo ========================================
echo Starting in BACKGROUND mode
echo ========================================
echo.

REM Create a VBScript to run Celery Beat completely hidden
set TEMP_VBS=%TEMP%\celery_beat_start.vbs

echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP_VBS%"
echo WshShell.Run "cmd /c celery -A config.celery beat --loglevel=INFO --logfile=logs/celery_beat.log", 0, False >> "%TEMP_VBS%"

cscript //nologo "%TEMP_VBS%"
del "%TEMP_VBS%"

timeout /t 2 /nobreak >nul

echo Celery Beat started in background (completely hidden)
echo Log file: logs\celery_beat.log
echo.
echo To view log in real-time:
echo   Get-Content logs\celery_beat.log -Tail 20 -Wait
echo.
echo To stop the beat:
echo   .\start_celery_beat.bat stop
echo.
pause
exit /b 0

:stop
echo Stopping Celery Beat...
echo.

REM Kill all python processes running celery beat
for /f "tokens=2" %%i in ('tasklist ^| findstr /i "celery.*beat"') do (
    taskkill /F /PID %%i >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo Celery Beat stopped
pause
exit /b 0

:restart
call :stop
timeout /t 3 /nobreak >nul
call :start
exit /b 0
