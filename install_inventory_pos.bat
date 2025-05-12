@echo off
REM Batch script to install and run Inventory & POS System on Windows

echo Installing required Python packages...
pip install -r backend\requirements.txt

echo Initializing database by running backend server once...
start /B python backend\app.py
timeout /t 10

echo Creating admin user...
python backend\scripts\create_admin_user.py

echo Starting backend server...
start /B python backend\app.py

echo Starting frontend server...
start /B python -m http.server 8000

echo Installation and servers started.
echo Open your browser and go to http://localhost:8000/index.html
pause
