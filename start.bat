@echo off
echo Installing dependencies (CustomTkinter)...
python -m pip install -r requirements.txt

echo.
echo Starting Smart Task Manager...
python app.py

pause
