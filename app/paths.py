"""Utilidades de rutas compatibles con ejecutables empaquetados."""
from pathlib import Path
import sys


def base_path() -> Path:
    """Devuelve la ruta base tanto en modo fuente como empaquetado."""
    frozen_root = getattr(sys, "_MEIPASS", None)
    if frozen_root:
        return Path(frozen_root)
    return Path(__file__).resolve().parent


def resource_path(relative: str | Path) -> Path:
    """Obtiene la ruta a un recurso dentro del paquete o al lado del .exe."""
    rel_path = Path(relative)
    if rel_path.is_absolute():
        return rel_path
    return base_path() / rel_path
