@echo off
setlocal

title URY Engine v0.7.9 - Windows EXE Builder

cd /d "%~dp0"

echo =========================================================
echo   URY Engine v0.7.9 Windows EXE Builder
echo =========================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python을 찾을 수 없습니다.
    echo Python 3.10 이상이 설치되어 있어야 합니다.
    pause
    exit /b 1
)

echo [1/2] Windows EXE 빌드를 시작합니다...
echo.

python "%~dp0system\code\build_exe_gui.py"

if errorlevel 1 (
    echo.
    echo [ERROR] EXE 빌드에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo [OK] Windows EXE 빌드가 완료되었습니다.
echo.
pause
