@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creando el entorno virtual, la primera vez tarda un poco...
    python -m venv .venv
)

".venv\Scripts\python.exe" -c "import django" 2>nul || (
    echo Instalando las dependencias...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)

echo.
echo  El blog sale en   http://127.0.0.1:8000/
echo  El portfolio en   http://127.0.0.1:8000/portfolio/
echo  El panel en       http://127.0.0.1:8000/admin/
echo.
echo  Para cortar el servidor aprieta Ctrl+C
echo.

timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8000/

".venv\Scripts\python.exe" manage.py runserver
pause
