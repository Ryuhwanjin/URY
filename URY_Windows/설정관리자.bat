@echo off
@chcp 65001 >nul
setlocal
title URY v0.9.6 - Windows Academic Studio
cd /d "%~dp0"

echo =========================================================
echo  URY v0.9.6 (Windows Academic Studio)
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
echo [RUN] Starting URY GUI...
echo.
"%PY_CMD%" "%~dp0system\code\settings_gui.py"
set "RESULT=%errorlevel%"
echo.
if not "%RESULT%"=="0" echo [ERROR] URY exited with code %RESULT%.
if "%RESULT%"=="0" echo URY has exited.
pause
exit /b %RESULT%

:NO_PY
echo [ERROR] Python was not found on this PC.
echo Install Python 3.10 or later, enable "Add python.exe to PATH", and run again.
start "" https://www.python.org/downloads/
pause
exit /b 1
