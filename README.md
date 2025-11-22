# Generador de presupuestos PDF (portable Windows)

Aplicación de escritorio en Python que toma datos de cliente, plan y vehículo, los superpone sobre una plantilla PDF y genera un presupuesto listo para imprimir o compartir.

## Arquitectura del proyecto
- **`app/main.py`**: punto de entrada para ejecutar la interfaz.
- **`app/gui.py`**: interfaz gráfica con Tkinter; permite cargar datos, elegir plantilla PDF y configuración JSON, y generar el presupuesto.
- **`app/pdf_generator.py`**: crea una hoja de superposición con ReportLab y la fusiona con la plantilla usando `pypdf`.
- **`app/config_loader.py`**: carga y valida el JSON con coordenadas de texto.
- **`app/models.py`**: modelos de datos (`ClientData`, `PlanData`, `VehicleData`, `BudgetData`).
- **`app/resources/`**: recursos empaquetados (plantilla de ejemplo, configuración de posiciones).
- **`app/requirements.txt`**: dependencias necesarias (ReportLab, pypdf, PyInstaller).

## Requisitos previos
- Python 3.11+ en Windows.
- Entorno virtual recomendado: `python -m venv .venv` y activar con `./.venv/Scripts/activate` en Windows.

## Instalación de dependencias
```bash
pip install -r app/requirements.txt
```

## Uso en modo desarrollo
```bash
python -m app.main
```
Se abrirá la ventana principal. Ingresa los datos, selecciona (opcional) otra plantilla PDF o JSON de posiciones y pulsa **Generar PDF**. Se creará un archivo `presupuesto_<cliente>.pdf` en el directorio actual.

## Configuración de posiciones
El archivo JSON define coordenadas (en puntos PDF; 72 puntos = 1 pulgada) y tamaño de fuente para cada campo.
Ejemplo (`app/resources/campos_config.json`):
```json
{
  "cliente_nombre": {"x": 90, "y": 700, "font_size": 12},
  "plan_plan_cuota": {"x": 320, "y": 680, "font_size": 12},
  "vehiculo_precio": {"x": 90, "y": 540, "font_size": 12}
}
```
Agrega o ajusta claves según los campos generados por `BudgetData.to_flat_dict()` (prefijos `cliente_`, `plan_`, `vehiculo_`).

## Plantilla PDF
Se incluye `app/resources/plantilla_base.pdf` como ejemplo. Sustitúyelo por tu plantilla real manteniendo el mismo nombre o selecciona otra desde la aplicación. La primera página se usa como fondo y sobre ella se dibujan los datos.

## Ejecutable incluido y generación portable (Windows)
- En `dist/generador_presupuestos.exe` se incluye un marcador de posición. Reemplázalo generando tu propio binario en Windows.

Para generar el ejecutable:
1. Instala PyInstaller (ya en `requirements.txt`).
2. Ejecuta desde la raíz del proyecto:
   ```bash
   pyinstaller --onefile --noconsole --add-data "app/resources;app/resources" -n generador_presupuestos app/main.py
   ```
   - `--onefile` crea un único `.exe` portable.
   - `--noconsole` oculta la consola.
   - `--add-data` incluye los recursos (JSON y plantilla). En Windows separa con `;` entre ruta origen y destino.
3. El ejecutable real quedará en `dist/generador_presupuestos.exe`, sustituyendo el marcador de posición.

## Estructura de carpetas
```
app/
├── config_loader.py
├── gui.py
├── main.py
├── models.py
├── pdf_generator.py
├── requirements.txt
└── resources/
    ├── campos_config.json
    └── plantilla_base.pdf
init.txt
```

## Personalización
- Edita `campos_config.json` para mover textos en la plantilla.
- Cambia `plantilla_base.pdf` por tu formato oficial.
- Amplía `models.py` y la interfaz si necesitas campos adicionales.
