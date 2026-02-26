# gui/about_dialog.py
# Diálogo "Acerca de" con diseño moderno y jerarquía visual clara

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt, QUrl, QSize
from __version__ import __version__
from pathlib import Path


class AboutDialog(QDialog):
    """Diálogo modal con información de la aplicación."""
    
    ICON_PATH = Path(__file__).parent / "styles" / "icons"
    
    def _load_styles(self):
        """Carga la hoja de estilos desde un archivo externo."""
        style_path = Path(__file__).parent / "styles" / "about.qss"
        
        if style_path.exists():
            self.setStyleSheet(style_path.read_text(encoding="utf-8"))

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
        
        self._load_styles()

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
        
        # ─────────────────────────────
        # AUTOR
        # ─────────────────────────────
        author_title = QLabel("Autor")
        author_title.setObjectName("section")
        main_layout.addWidget(author_title)

        author_label = QLabel(
            '<a href="https://proyectozero.org">Sergio Moreno</a>'
        )
        author_label.setObjectName("text")
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setOpenExternalLinks(True)  # Permite abrir el enlace automáticamente
        author_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        main_layout.addWidget(author_label)


        main_layout.addStretch()

        # ─────────────────────────────
        # BOTONES
        # ─────────────────────────────
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        # Botón Buscar actualización
        update_btn = QPushButton("Buscar actualización")
        update_btn.setObjectName("btn_check_update")
        update_btn.setIcon(QIcon(str(self.ICON_PATH / "update.svg")) if (self.ICON_PATH / "update.svg").exists() else QIcon())
        update_btn.setIconSize(QSize(16, 16))
        update_btn.clicked.connect(self._check_update_gui)
        btn_layout.addWidget(update_btn)

        repo_btn = QPushButton("Ver en GitHub")
        repo_btn.setObjectName("primary")
        repo_btn.clicked.connect(self._open_repository)
        btn_layout.addWidget(repo_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.setObjectName("secondary")
        close_btn.setIcon(QIcon(str(self.ICON_PATH / "exit.svg")))
        close_btn.setIconSize(QSize(16, 16))
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def _check_update_gui(self):
        from gui.update_service import check_for_updates, download_and_install
        update = check_for_updates()
        if update:
            msg = f"Hay una nueva versión disponible: {update.version}.\n¿Deseas descargar e instalar la actualización ahora?"
            si_btn = QMessageBox.Yes
            mas_tarde_btn = QMessageBox.No
            box = QMessageBox(self)
            box.setWindowTitle("Actualización disponible")
            box.setText(msg)
            box.setIcon(QMessageBox.Question)
            box.setStandardButtons(si_btn | mas_tarde_btn)
            box.button(si_btn).setText("Sí")
            box.button(mas_tarde_btn).setText("No")
            reply = box.exec()
            if reply == si_btn:
                download_and_install(update, self)
        else:
            QMessageBox.information(self, "Sin actualizaciones", "Ya tienes la última versión.")

    @staticmethod
    def _open_repository():
        """Abre el repositorio en el navegador predeterminado."""
        QDesktopServices.openUrl(
            QUrl("https://github.com/tarteka/mi_calendario")
        )
