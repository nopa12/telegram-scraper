@echo off
cd /d "%~dp0"
echo Current directory is now: %CD%

set VENV_DIR=venv

if not exist "%VENV_DIR%" (
    echo Creating virtual environment directory...
    python -m venv "%VENV_DIR%"
)

echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate"

pip install -r requirements.txt