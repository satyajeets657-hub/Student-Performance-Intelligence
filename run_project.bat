@echo off
title Student Performance Intelligence System
echo ===================================================
echo Starting Student Performance Intelligence System...
echo ===================================================
echo Opening http://127.0.0.1:5000 in your browser...
start http://127.0.0.1:5000
python wsgi.py
pause
