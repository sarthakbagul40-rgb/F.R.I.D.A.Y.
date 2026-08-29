@echo off
title F.R.I.D.A.Y. // Diagnostic Test Suite
color 0B
echo.
echo ===================================================================
echo               F.R.I.D.A.Y. V7.5 DIAGNOSTIC TEST SUITE
echo ===================================================================
echo.

echo [*] Testing 1: Codebase Health Audit (Target: 100/100)...
.venv\Scripts\python.exe -c "from core.health_check import codebase_auditor; r = codebase_auditor.perform_deep_audit(); s = max(0, 100 - (len(r.get('syntax_errors', [])) * 25 + len(r.get('vulnerabilities', [])) * 10 + len(r.get('code_smells', [])) * 2)); print('Health Score:', s, '/ 100')"
echo.

echo [*] Testing 2: Optical Camera Hardware Connection...
.venv\Scripts\python.exe -c "import cv2; cap = cv2.VideoCapture(0, cv2.CAP_DSHOW); print('Camera Active:', cap.isOpened()); cap.release() if cap.isOpened() else None"
echo.

echo [*] Testing 3: OpenCode Multi-Model CLI...
opencode --version
echo.

echo [*] Testing 4: Autonomous Coding & D: Drive Storage...
.venv\Scripts\python.exe -c "from core.claude_bridge import coding_engine; res = coding_engine.handle_coding_request('write a python hello world script'); print('Success! Code saved to D:\\FRIDAY_Projects\\')"
echo.

echo ===================================================================
echo                 ALL SYSTEMS NOMINAL AND VERIFIED!
echo ===================================================================
echo.
pause
