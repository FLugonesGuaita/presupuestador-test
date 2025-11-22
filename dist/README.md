# Ejecutable incluido

Este repositorio incluye `dist/generador_presupuestos.exe` como marcador de posición para el ejecutable portable. Para obtener un binario real en Windows recompila con PyInstaller:

```bash
pyinstaller --onefile --noconsole --add-data "app/resources;app/resources" -n generador_presupuestos app/main.py
```

El ejecutable generado aparecerá en `dist/` y reemplazará este marcador.
