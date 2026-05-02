@echo off
echo Starting Celery Worker for Windows...
echo.
echo Make sure Redis and MySQL are running
echo.
cd /d %~dp0
set DJANGO_ENV=development
celery -A config.celery worker -l info -P solo
pause