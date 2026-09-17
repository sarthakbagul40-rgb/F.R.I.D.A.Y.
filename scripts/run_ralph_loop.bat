@echo off
title F.R.I.D.A.Y. OS 10.0 // Ralph Flow Autonomous Execution Loop
color 0A
echo.
echo ===================================================================
echo     F.R.I.D.A.Y. OS 10.0 -- RALPH FLOW AUTONOMOUS CODING LOOP
echo ===================================================================
echo [*] Initializing autonomous execution monitor...
python -c "from core.ralph_engine import ralph_engine; q = ralph_engine.load_queue(); print(f'Active Queue: {q[\"project_name\"] if q else \"No active queue.\" Status: {q[\"status\"] if q else \"Idle\"}')"
echo.
echo [*] Press any key to trigger next step or review status...
pause
