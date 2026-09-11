@echo off
@chcp 65001 >nul
setlocal
title URY v0.9.6 - URY Uninstaller
cd /d "%~dp0"

echo =========================================================
echo  URY v0.9.6 Complete Program Uninstaller
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
echo [RUN] Starting the URY uninstaller GUI...
echo.
"%PY_CMD%" "%~dp0system\code\uninstall_gui.py"
set "RESULT=%errorlevel%"
echo.
if not "%RESULT%"=="0" echo [ERROR] Uninstaller failed with code %RESULT%.
if "%RESULT%"=="0" echo Uninstaller finished.
pause
exit /b %RESULT%

:NO_PY
echo [ERROR] Python was not found. No user data was deleted.
echo Use Windows Apps and Features to remove the installed URY program.
echo The user workspace folders are intentionally preserved.
pause
exit /b 1
