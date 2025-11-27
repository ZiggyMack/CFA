@echo off
REM Launch Both Dashboards Simultaneously
REM Run from: dashboard/

echo Starting CFA Dashboard Suite...
echo.
echo [1/2] Launching Health Dashboard...
start "CFA Health Dashboard" cmd /k "cd HealthDashboard && streamlit run app.py"

timeout /t 2 /nobreak >nul

echo [2/2] Launching SMV Trinity...
start "SMV Trinity" cmd /k "cd SMV && npm run dev"

echo.
echo ========================================
echo  CFA Dashboard Suite Started!
echo ========================================
echo.
echo Health Dashboard: http://localhost:8504
echo SMV Trinity:      http://localhost:3001
echo.
echo Press any key to close this launcher...
pause >nul
