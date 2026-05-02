@echo off
echo Starting Celery Beat...
echo.
cd /d %~dp0
celery -A config.celery beat -l info
pause
