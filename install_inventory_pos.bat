@echo off
REM Batch script to clean, install and run Inventory & POS System on Windows

echo Deleting existing database file...
del /F /Q backend\pos_system.db

echo Installing required Python packages...
pip install -r backend\requirements.txt

echo Initializing database tables...
python backend\init_db.py

echo Creating admin user...
python create_admin_user.py admin canggara1@gmail.com admin123

echo Starting backend server...
start python backend\app.py

echo Starting frontend server...
start python -m http.server 8000

echo Installation and servers started.
echo Open your browser and go to http://localhost:8000/index.html
pause
