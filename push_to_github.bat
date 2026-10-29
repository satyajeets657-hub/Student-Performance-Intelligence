@echo off
title Auto-Sync to GitHub (Live Website Update)
echo ========================================================
echo  UPDATING LIVE WEBSITE VIA GITHUB
echo  Live URL: https://satyajeets657-hub.github.io/Student-Performance-Intelligence/
echo ========================================================
echo.
git add -A
git commit -m "Update project changes"
git push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo  SUCCESS: Code pushed! Your live website will update
    echo  automatically within 30-60 seconds!
    echo ========================================================
) else (
    echo ========================================================
    echo  Sync could not be completed. Please check your network.
    echo ========================================================
)
pause
