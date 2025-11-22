@echo off
setlocal
REM Construye el ejecutable portable para Windows
python -m pip install --upgrade pip
python -m pip install -r app\requirements.txt
pyinstaller --noconsole --onefile --name generador_presupuestos ^
    --add-data "app/resources;resources" ^
    app/main.py
