# gui/app.py
# Crea QApplication, carga estilos y muestra la ventana principal.
import sys
from platform import system
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .main_window import MainWindow


def _get_base_path():
    """Devuelve la ruta base correcta según si estamos empaquetados o no.
    Cuando PyInstaller empaqueta con --onefile, extrae archivos a _MEIPASS.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Ejecutándose como ejecutable empaquetado
        return Path(sys._MEIPASS)
    else:
        # Ejecutándose como script normal
        return Path(__file__).resolve().parents[1]


ROOT = _get_base_path()

def _load_styles(app):
    qss_path = ROOT / "gui" / "styles" / "main.qss"
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception:
        pass  # no crítico si no existe


def _select_icon_path():
    """Devuelve la mejor ruta de icono disponible.

    Preferencia por `.ico` en Windows y `.png` en otros sistemas.
    Busca en `assets/` dentro de la ruta base (que puede ser _MEIPASS si está empaquetado).
    """
    sys_name = system()
    candidates = []
    if sys_name == "Windows":
        candidates = [
            ROOT / "assets" / "icon.ico",
            ROOT / "assets" / "app.ico",
        ]
    else:
        candidates = [
            ROOT / "assets" / "icon.png",
            ROOT / "assets" / "icon.ico",
        ]

    for p in candidates:
        try:
            if p.exists():
                return str(p)
        except Exception:
            continue
    return None

def run_app():
    """Arranca la aplicación Qt."""
    # En Windows, fijar AppUserModelID mejora que el icono del exe se use en la barra de tareas
    if system() == "Windows":
        # Prefer QtWin API when available, fallback to ctypes shell32 call
        try:
            from PySide6.QtWinExtras import QtWin
            QtWin.setCurrentProcessExplicitAppUserModelID("com.tarteka.mi_calendario")
        except Exception:
            try:
                import ctypes
                from ctypes import c_wchar_p
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(c_wchar_p("com.tarteka.mi_calendario"))
            except Exception:
                pass

    app = QApplication(sys.argv)
    _load_styles(app)

    icon_path = _select_icon_path()
    if icon_path:
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()

    if icon_path:
        window.setWindowIcon(QIcon(icon_path))
    window.showMaximized()

    # Forzar icono de ventana después de mostrarla (algunas versiones de Windows/Qt lo requieren)
    try:
        if icon_path:
            window.setWindowIcon(QIcon(icon_path))
            QApplication.instance().setWindowIcon(QIcon(icon_path))
    except Exception:
        pass

    sys.exit(app.exec())