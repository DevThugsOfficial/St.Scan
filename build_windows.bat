@echo off
REM Activate venv and build one-file windowed executable using PyInstaller
REM Adjust venv activation path if your venv has different structure

IF EXIST "venv\\Scripts\\activate.bat" (
    call venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment activation script not found at venv\Scripts\activate.bat
    echo Ensure you run this from project root where 'venv' exists.
)

REM Use the provided stc.ico in assets as application icon
pyinstaller --onefile --windowed --name RecordSync --icon "assets/stc.ico" --add-data "assets;assets" --add-data "database;database" main.py
echo Build finished. See dist\RecordSync.exe
pause