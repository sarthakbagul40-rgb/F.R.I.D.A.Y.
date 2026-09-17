@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title F.R.I.D.A.Y. OS 10.0 // Master System Diagnostic
color 0B
chcp 65001 >nul 2>&1

set "PYTHON_EXE=python"
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
)

"%PYTHON_EXE%" scripts/diagnose_all_systems.py
echo.
pause
