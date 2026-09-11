@echo off
@chcp 65001 >nul
setlocal
title URY v0.9.6 - Legacy Pipeline Runner
cd /d "%~dp0"

echo =========================================================
echo  URY v0.9.6 Legacy Pipeline Runner
echo =========================================================
echo.
echo [NOTICE] Manual pipeline execution is no longer part of the URY UI.
echo Use Studio to select the course materials and generate a lecture note.
pause
exit /b 1
