@echo off
@chcp 65001 >nul
setlocal
title URY v0.9.6 - Windows Standalone EXE Builder
cd /d "%~dp0"

echo =========================================================
echo  URY v0.9.6 Windows Standalone EXE Builder
echo =========================================================
echo.

set "PY_CMD="
if exist "%~dp0python\python.exe" set "PY_CMD=%~dp0python\python.exe"
for %%P in ("%LocalAppData%\Programs\Python\Python312\python.exe" "%LocalAppData%\Programs\Python\Python311\python.exe" "%LocalAppData%\Programs\Python\Python310\python.exe" "C:\Program Files\Python312\python.exe" "C:\Program Files\Python311\python.exe" "C:\Program Files\Python310\python.exe") do if not defined PY_CMD if exist "%%~P" set "PY_CMD=%%~P"
if not defined PY_CMD for /f "delims=" %%i in ('where python 2^>nul') do (
    echo %%i | findstr /i "WindowsApps" >nul || if not defined PY_CMD set "PY_CMD=%%i"
)
if not defined PY_CMD goto NO_PY

echo [OK] Python: "%PY_CMD%"
echo [RUN] Starting the EXE builder...
echo.
"%PY_CMD%" "%~dp0system\code\build_exe_gui.py"
set "RESULT=%errorlevel%"
echo.
if not "%RESULT%"=="0" echo [ERROR] EXE build failed with code %RESULT%.
if "%RESULT%"=="0" echo EXE build process finished.
pause
exit /b %RESULT%

:NO_PY
echo [ERROR] Python was not found on this PC.
pause
exit /b 1
