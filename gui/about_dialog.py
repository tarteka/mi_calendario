# gui/about_dialog.py
# Diálogo "Acerca de" con diseño moderno y jerarquía visual clara

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt, QUrl
from __version__ import __version__
from pathlib import Path


class AboutDialog(QDialog):
    """Diálogo modal con información de la aplicación."""
    
    def _load_styes(self):
        """Carga la hoja de estilos desde un archivo externo."""
        style_path = Path(__file__).parent / "styles" /"about.qss"
        if style_path.exists():
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            pass  # No crítico si no se encuentra el archivo de estilos

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configuración base del diálogo
        self.setWindowTitle("Acerca de Mi Calendario")
        self.setFixedSize(520, 680)
        self.setModal(True)

        # Solo botón cerrar (sin minimizar ni maximizar)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        
        self._load_styes()

        self._build_ui()

    def _build_ui(self):
        """Construye la interfaz visual del diálogo."""

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(35, 30, 35, 30)
        main_layout.setSpacing(14)

        # ─────────────────────────────
        # TÍTULO
        # ─────────────────────────────
        title = QLabel("Mi Calendario de Guardias")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        version_label = QLabel(f"Versión {__version__}")
        version_label.setObjectName("subtitle")
        version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(version_label)

        # Separador
        separator = QLabel()
        separator.setStyleSheet("border-top: 1px solid #dcdde1;")
        separator.setFixedHeight(15)
        main_layout.addWidget(separator)

        # ─────────────────────────────
        # DESCRIPCIÓN
        # ─────────────────────────────
        description = QLabel(
            "Generador automático de calendarios de guardias desde Ambu App.\n"
            "Convierte turnos en formatos PDF e ICS para integrarlos en\n"
            "Google Calendar o Apple Calendar."
        )
        description.setObjectName("text")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # ─────────────────────────────
        # SEGURIDAD
        # ─────────────────────────────
        security_title = QLabel("Seguridad y Privacidad")
        security_title.setObjectName("section")
        main_layout.addWidget(security_title)

        security_text = QLabel(
            "• No guarda credenciales ni contraseñas\n"
            "• No recopila datos personales\n"
            "• Comunicación directa entre tu equipo y el servidor"
        )
        security_text.setObjectName("text")
        security_text.setWordWrap(True)
        main_layout.addWidget(security_text)

        # ─────────────────────────────
        # LICENCIA
        # ─────────────────────────────
        license_title = QLabel("Licencia")
        license_title.setObjectName("section")
        main_layout.addWidget(license_title)

        license_text = QLabel(
            "Software de uso libre y académico.\n"
            "Consulta el repositorio para más información."
        )
        license_text.setObjectName("text")
        license_text.setWordWrap(True)
        main_layout.addWidget(license_text)

        # ─────────────────────────────
        # DESCARGO
        # ─────────────────────────────
        disclaimer_title = QLabel("Descargo de Responsabilidad")
        disclaimer_title.setObjectName("section")
        main_layout.addWidget(disclaimer_title)

        disclaimer_text = QLabel(
            "Este software se proporciona \"tal cual\".\n"
            "El autor no se hace responsable de pérdidas de datos\n"
            "o uso indebido derivado de su utilización."
        )
        disclaimer_text.setObjectName("text")
        disclaimer_text.setWordWrap(True)
        main_layout.addWidget(disclaimer_text)

        main_layout.addStretch()

        # ─────────────────────────────
        # BOTONES
        # ─────────────────────────────
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        repo_btn = QPushButton("Ver en GitHub")
        repo_btn.setObjectName("primary")
        repo_btn.clicked.connect(self._open_repository)
        btn_layout.addWidget(repo_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    @staticmethod
    def _open_repository():
        """Abre el repositorio en el navegador predeterminado."""
        QDesktopServices.openUrl(
            QUrl("https://github.com/tarteka/mi_calendario")
        )
