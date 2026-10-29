@echo off
title Student Performance Intelligence - Phone Live Link
echo ===================================================================
echo Starting Flask App and Cloudflare Public Tunnel for Phone Access...
echo ===================================================================
start /B python wsgi.py
timeout /t 2 >nul
echo Generating your live HTTPS public link...
echo (Open the https://....trycloudflare.com link on your phone)
echo ===================================================================
cloudflared.exe tunnel --url http://127.0.0.1:5000
pause
