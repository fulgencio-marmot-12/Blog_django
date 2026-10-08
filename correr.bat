@echo off
cd /d "%~dp0"
set "PY=python"

python -c "import django" >nul 2>&1
if errorlevel 1 goto convenv

echo Usando el Python de la computadora.
goto ejecutar

:convenv
if not exist ".venv\Scripts\python.exe" (
    echo Creando el entorno virtual, la primera vez tarda un poco...
    python -m venv .venv
)
set "PY=.venv\Scripts\python.exe"
"%PY%" -c "import django" >nul 2>&1
if errorlevel 1 (
    echo Instalando las dependencias...
    "%PY%" -m pip install -r requirements.txt
)
echo Usando el entorno virtual del proyecto.

:ejecutar
echo.
echo  El blog sale en   http://127.0.0.1:8000/
echo  El portfolio en   http://127.0.0.1:8000/portfolio/
echo  El panel en       http://127.0.0.1:8000/admin/
echo.
echo  Para cortar el servidor aprieta Ctrl+C
echo.

timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8000/

"%PY%" manage.py runserver
pause
