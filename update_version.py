#!/usr/bin/env python
"""Script para actualizar la versión en todos los archivos."""

import re
from pathlib import Path

# Leer versión actual
from __version__ import __version__

def update_readme():
    """Actualiza la versión en README.md"""
    readme = Path("README.md")
    content = readme.read_text(encoding="utf-8")

    # Actualizar badge de descarga
    content = re.sub(
        r'!\[Download v[\d.]+\]\(https://img\.shields\.io/badge/descargar_exe-v[\d.]+-orange\.svg\)',
        f'![Download v{__version__}](https://img.shields.io/badge/descargar_exe-v{__version__}-orange.svg)',
        content
    )

    # Actualizar URL de descarga
    content = re.sub(
        r'\]\(https://github\.com/tarteka/mi_calendario/releases/download/v[\d.]+/Generador_Calendario_v[\d.]+\.exe\)',
        f'](https://github.com/tarteka/mi_calendario/releases/download/v{__version__}/Generador_Calendario_v{__version__}.exe)',
        content
    )

    readme.write_text(content, encoding="utf-8")
    print(f"✓ README.md actualizado a v{__version__}")

if __name__ == "__main__":
    update_readme()
    print(f"Versión actual: {__version__}")
