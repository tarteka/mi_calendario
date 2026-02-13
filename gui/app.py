# gui/app.py
# Crea QApplication, carga estilos y muestra la ventana principal.
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .main_window import MainWindow

ROOT = Path(__file__).resolve().parents[1]

def _load_styles(app):
    qss_path = ROOT / "gui" / "styles.qss"
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception:
        pass  # no crítico si no existe

def run_app():
    """Arranca la aplicación Qt."""
    app = QApplication(sys.argv)
    _load_styles(app)
    # Si tienes calendario.ico en la raíz del repo:
    try:
        app.setWindowIcon(QIcon(str(ROOT / "calendario.ico")))
    except Exception:
        pass
    window = MainWindow()
    window.show()
    sys.exit(app.exec())