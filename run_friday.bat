@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title F.R.I.D.A.Y. OS // NEURAL TACTICAL CORE
color 0B
chcp 65001 >nul 2>&1

echo.
echo ===================================================================
echo          F.R.I.D.A.Y. SYSTEM INITIALIZATION SEQUENCE
echo              Your Personal AI Companion ^& Tactical OS
echo ===================================================================
echo.

:: 1. Determine Python Executable
set "PYTHON_EXE=python"
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
)

:: 2. Check & Launch Gemini-Web2API Pro Bridge (Port 8081) Silently in Background
netstat -ano | findstr :8081 >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Starting Gemini-Web2API neural gateway in background...
    powershell -NoProfile -WindowStyle Hidden -Command "Start-Process '%PYTHON_EXE%' -ArgumentList '\"%~dp0core\gemini_web2api\gemini_web2api.py\"', '--port', '8081' -WorkingDirectory '%~dp0core\gemini_web2api' -WindowStyle Hidden" >nul 2>&1
) else (
    echo [✓] Gemini-Web2API Bridge is active on port 8081.
)

echo [*] Starting F.R.I.D.A.Y. Master Terminal HUD ^& Neural Voice Engine...
echo.
"%PYTHON_EXE%" main.py

if %errorlevel% neq 0 (
    echo.
    echo [!] F.R.I.D.A.Y. halted with error code %errorlevel%.
    echo Press any key to close this terminal...
    pause >nul
)
