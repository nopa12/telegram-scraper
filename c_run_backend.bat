@echo off
cd /d "%~dp0"
echo Current directory is now: %CD%

set VENV_DIR=venv

call "%VENV_DIR%\Scripts\activate"

python ./src/c_backend.py