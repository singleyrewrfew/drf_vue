@echo off
REM ========================================
REM 清空 Redis 缓存脚本
REM 
REM 用途：清除所有或指定模式的 Redis 缓存
REM 使用场景：代码更新后清除旧缓存，避免数据不一致
REM ========================================

cd /d "%~dp0"

echo.
echo ========================================
echo   Redis 缓存清理工具
echo ========================================
echo.

:menu
echo 请选择操作：
echo.
echo 1. 清空所有缓存（谨慎使用）
echo 2. 清空内容相关缓存（contents:*）
echo 3. 清空分类相关缓存（categories:*）
echo 4. 清空标签相关缓存（tags:*）
echo 5. 清空角色权限缓存（roles:* permissions:*）
echo 6. 自定义模式
echo 0. 退出
echo.

set /p choice="请输入选项 (0-6): "

if "%choice%"=="1" goto clear_all
if "%choice%"=="2" goto clear_contents
if "%choice%"=="3" goto clear_categories
if "%choice%"=="4" goto clear_tags
if "%choice%"=="5" goto clear_roles
if "%choice%"=="6" goto clear_custom
if "%choice%"=="0" goto end

echo 无效选项，请重新选择
echo.
goto menu

:clear_all
call venv\Scripts\python.exe backend\manage.py clear_cache --pattern "*"
goto end

:clear_contents
call venv\Scripts\python.exe backend\manage.py clear_cache --pattern "contents:*"
goto end

:clear_categories
call venv\Scripts\python.exe backend\manage.py clear_cache --pattern "categories:*"
goto end

:clear_tags
call venv\Scripts\python.exe backend\manage.py clear_cache --pattern "tags:*"
goto end

:clear_roles
call venv\Scripts\python.exe backend\manage.py clear_cache --pattern "roles:*"
call venv\Scripts\python.exe backend\manage.py clear_cache --pattern "permissions:*"
goto end

:clear_custom
echo.
set /p pattern="请输入缓存模式（如 contents:*）: "
call venv\Scripts\python.exe backend\manage.py clear_cache --pattern "%pattern%"
goto end

:end
echo.
echo 按任意键退出...
pause >nul
