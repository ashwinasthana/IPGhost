@echo off
title IPGhost - Advanced Tor IP Changer

echo.
echo   ██▓ ██▓███    ▄████  ██░ ██  ▒█████   ██████ ▄▄▄█████▓
echo  ▓██▒▓██░  ██▒ ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
echo  ▒██▒▓██░ ██▓▒▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
echo  ░██░▒██▄█▓▒ ▒░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ 
echo  ░██░▒██▒ ░  ░░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ 
echo  ░▓  ▒▓▒░ ░  ░ ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   
echo   ▒ ░░▒ ░       ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    
echo   ▒ ░░░       ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░      
echo   ░                 ░  ░  ░  ░    ░ ░        ░           
echo.
echo IPGhost Launcher - by Ashwin Asthana
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if ipghost.py exists
if not exist "ipghost.py" (
    echo Error: ipghost.py not found in current directory
    pause
    exit /b 1
)

REM Check and install requirements
echo Checking dependencies...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing requirements...
    python -m pip install -r requirements.txt
)

echo Starting IPGhost...
echo.

REM Launch IPGhost
python ipghost.py

pause