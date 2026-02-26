import requests
from packaging import version
from dataclasses import dataclass
import tempfile
import os
import sys
import subprocess
from PySide6.QtWidgets import QMessageBox, QApplication

from __version__ import __version__

GITHUB_API_URL = os.environ.get(
    "GITHUB_API_URL",
    "https://api.github.com/repos/tarteka/mi_calendario/releases/latest"
)

@dataclass
class UpdateInfo:
    version: str
    download_url: str
    mandatory: bool = False

def check_for_updates() -> UpdateInfo | None:
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        latest_version = data["tag_name"].lstrip("v")
        if version.parse(latest_version) <= version.parse(__version__):
            return None
        for asset in data.get("assets", []):
            if asset["name"].endswith(".exe"):
                return UpdateInfo(
                    version=latest_version,
                    download_url=asset["browser_download_url"],
                )
    except requests.RequestException:
        return None
    return None

def ask_and_update(parent=None):
    update = check_for_updates()
    if update:
        msg = f"Hay una nueva versión disponible: {update.version}.\n¿Deseas descargar e instalar la actualización ahora?"
        reply = QMessageBox.question(parent, "Actualización disponible", msg, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            download_and_install(update, parent)
    else:
        QMessageBox.information(parent, "Sin actualizaciones", "Ya tienes la última versión.")

def download_and_install(update: UpdateInfo, parent=None):
    try:
        temp_dir = tempfile.gettempdir()
        local_path = os.path.join(temp_dir, f"update_{update.version}.exe")
        with requests.get(update.download_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        QMessageBox.information(parent, "Descarga completa", "El instalador se descargó correctamente. Se iniciará la actualización.")
        subprocess.Popen([local_path])
        QApplication.instance().quit()
    except Exception as e:
        QMessageBox.warning(parent, "Error de actualización", f"No se pudo descargar o ejecutar el instalador:\n{e}")
