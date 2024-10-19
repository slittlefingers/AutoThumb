@echo off
echo Starting backend...
echo Changing to script directory...
cd /d %~dp0
cd autoThumb
start cmd /k "python main.py"

echo Starting frontend...
echo Changing to script directory...
cd /d %~dp0
cd frontSide\forensic
start cmd /k "npm start"

echo Both frontend and backend have been started.
