@echo off
cd /d "%~dp0"
echo Current directory is now: %CD%

cd frontend


npm i
npm start
