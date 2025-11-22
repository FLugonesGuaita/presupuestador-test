import json
from pathlib import Path
from typing import Dict, Any

from .paths import resource_path

DEFAULT_CONFIG_PATH = resource_path("resources/campos_config.json")


def load_positions(config_path: Path | str = DEFAULT_CONFIG_PATH) -> Dict[str, Dict[str, Any]]:
    path = resource_path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("El archivo de configuración debe ser un objeto JSON con las posiciones")
    return data
