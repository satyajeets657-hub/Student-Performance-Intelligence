@echo off
title Push Project to GitHub
echo ========================================================
echo  PUSHING STUDENT PERFORMANCE INTELLIGENCE TO GITHUB
echo  Repository: https://github.com/satyajeets657-hub/Student-Performance-Intelligence
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo  SUCCESS: Project successfully pushed to GitHub!
    echo ========================================================
) else (
    echo ========================================================
    echo  Push was not completed. Please check your GitHub login.
    echo ========================================================
)
pause
