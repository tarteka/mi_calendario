# gui/main_window.py
# Ventana principal: formulario de credenciales, controls, barra de progreso y log.
from PySide6.QtCore import Slot, Qt, QSize
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTextEdit, QProgressBar, QMessageBox,
    QFileDialog, QGroupBox, QCheckBox
)
from PySide6.QtGui import QIcon
from pathlib import Path
from .worker import Worker
from .about_dialog import AboutDialog
from PySide6.QtWidgets import QApplication
from datetime import datetime
from __version__ import __version__
from services.config_loader import load_config

class MainWindow(QMainWindow):

    ICON_PATH = Path(__file__).parent / "styles" / "icons"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Mi Calendario de Guardias - v{__version__}")

        # Si la QApplication tiene un icono establecido, úsalo también en la ventana
        try:
            app_icon = QApplication.instance().windowIcon()
            if not app_icon.isNull():
                self.setWindowIcon(app_icon)
        except Exception:
            pass

        self.setMinimumSize(700, 420)

        self.worker = None
        self._build_ui()
        
    def actualizar_texto(self, valor: int):
        """Muestra el % solo si el valor es mayor que 0"""
        self.progreso.setTextVisible(valor > 0)
        
    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(18)

        # Grupo de credenciales (alineado con FormLayout)
        cred_box = QGroupBox()
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)

        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario de Lotura (ambulanciasgipuzkoa.ambu.app)")
        form.addRow(QLabel("Usuario:"), self.usuario)

        self.clave = QLineEdit()
        self.clave.setPlaceholderText("Contraseña de Lotura")
        self.clave.setEchoMode(QLineEdit.Password)

        # Container for password + show checkbox
        pwd_container = QWidget()
        pwd_layout = QHBoxLayout(pwd_container)
        pwd_layout.setContentsMargins(0, 0, 0, 0)
        pwd_layout.setSpacing(6)
        pwd_layout.addWidget(self.clave)
        self.chk_show_pwd = QCheckBox("Mostrar contraseña")
        self.chk_show_pwd.toggled.connect(self._toggle_password_visibility)
        pwd_layout.addWidget(self.chk_show_pwd)

        form.addRow(QLabel("Contraseña:"), pwd_container)

        self.anio = QComboBox()
        years = [str(y) for y in range(2025, 2036)]
        self.anio.addItems(years)
        
        current_year = str(datetime.now().year)
        if current_year in years:
            self.anio.setCurrentText(current_year)
            
        form.addRow(QLabel("Año:"), self.anio)

        cred_box.setLayout(form)
        layout.addWidget(cred_box)

        # Fila: ruta de salida (editable mediante diálogo)
        outfila = QHBoxLayout()
        outfila.setSpacing(8)
        outfila.addWidget(QLabel("Guardar en:"))
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)
        # valor por defecto: 'calendario' dentro de la carpeta Descargas del usuario (si existe)
        downloads = Path.home() / "Downloads"
        if downloads.exists() and downloads.is_dir():
            self.output_base = str(downloads / "calendario")
        else:
            self.output_base = str(Path.home() / "calendario")
        self.output_path.setText(self.output_base)
        outfila.addWidget(self.output_path)

        self.btn_change_output = QPushButton("Cambiar...")
        self.btn_change_output.clicked.connect(self.choose_output)
        outfila.addWidget(self.btn_change_output)

        layout.addLayout(outfila)

        # Botones
        botones = QHBoxLayout()
        botones.setSpacing(12)

        # Crear botones primero
        self.btn_about = QPushButton("Acerca de")
        self.btn_generar = QPushButton("Generar")
        self.btn_salir = QPushButton("Salir")

        # ObjectName
        self.btn_about.setObjectName("btn_about")
        self.btn_generar.setObjectName("btn_generar")
        self.btn_salir.setObjectName("btn_salir")

        # Conectar señales
        self.btn_about.clicked.connect(self._show_about)
        self.btn_generar.clicked.connect(self.on_generar)
        self.btn_salir.clicked.connect(self.close)

        # Asignar iconos (usar self.ICON_PATH)
        self.btn_about.setIcon(QIcon(str(self.ICON_PATH / "info.svg")))
        self.btn_generar.setIcon(QIcon(str(self.ICON_PATH / "play.svg")))
        self.btn_salir.setIcon(QIcon(str(self.ICON_PATH / "exit.svg")))

        self.btn_about.setIconSize(QSize(16, 16))
        self.btn_generar.setIconSize(QSize(16, 16))
        self.btn_salir.setIconSize(QSize(16, 16))

        # Añadir al layout
        botones.addWidget(self.btn_about)
        botones.addStretch()
        botones.addWidget(self.btn_generar)
        botones.addWidget(self.btn_salir)

        layout.addLayout(botones)


        # Progreso y log
        self.progreso = QProgressBar()
        self.progreso.setRange(0, 100)
        self.progreso.setValue(0)
        self.progreso.setTextVisible(False)  # Ocultar texto inicialmente
        self.progreso.valueChanged.connect(self.actualizar_texto)  # Conectar para mostrar texto solo si valor > 0
        
        layout.addWidget(self.progreso)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(120)
        layout.addWidget(self.log)

        # Para QMainWindow usamos un widget central
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    @Slot()
    def on_generar(self):
        if self.worker is not None and self.worker.isRunning():
            self._append_log("Ya hay un proceso en ejecución.")
            return

        usuario = self.usuario.text().strip()
        clave = self.clave.text().strip()
        anio = int(self.anio.currentText())

        if not usuario or not clave:
            QMessageBox.warning(self, "Faltan datos", "Usuario y contraseña son obligatorios.")
            return

        # Configuración para el worker (puede ser ampliada con más opciones si es necesario)
        config = load_config()
        config["OUTPUT"] = self.output_base

        # Crear y arrancar worker (hilo)
        self.worker = Worker(config=config, year=anio, canal="chrome", usuario=usuario, clave=clave)
        self.worker.log.connect(self._append_log)
        self.worker.progress.connect(self.progreso.setValue)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.error.connect(self._on_error)

        self.btn_generar.setEnabled(False)
        self.progreso.setValue(0)
        self._append_log("Lanzando proceso en segundo plano...")
        self.worker.start()

    @Slot(str)
    def _append_log(self, text):
        self.log.append(text)

    @Slot(bool)
    def _toggle_password_visibility(self, visible: bool):
        if visible:
            self.clave.setEchoMode(QLineEdit.Normal)
        else:
            self.clave.setEchoMode(QLineEdit.Password)

    @Slot()
    def _show_about(self):
        """Muestra el diálogo de información de la aplicación."""
        dialog = AboutDialog(self)
        dialog.exec()

    @Slot()
    def _on_finished(self):
        self._append_log("Proceso finalizado correctamente.")
        self.btn_generar.setEnabled(True)
        self.progreso.setValue(100)

    @Slot()
    def choose_output(self):
        # Permite elegir un nombre base; si el usuario selecciona un archivo
        # con extensión .csv/.pdf/.ics se quitará la extensión para usarla como base.
        default = self.output_base
        fname, _ = QFileDialog.getSaveFileName(self, "Guardar como", default, "CSV Files (*.csv);;PDF Files (*.pdf);;ICS Files (*.ics);;All Files (*)")
        if not fname:
            return
        p = Path(fname)
        if p.suffix.lower() in ('.csv', '.pdf', '.ics'):
            base = str(p.with_suffix(''))
        else:
            base = str(p)
        self.output_base = base
        self.output_path.setText(self.output_base)

    @Slot(str)
    def _on_error(self, err):
        # Limpiar log y barra de progreso en caso de error
        self.log.clear()
        self.progreso.setValue(0)
        self.progreso.setTextVisible(False)
        
        # Mostrar mensaje de error al usuario
        QMessageBox.warning(
            self,
            "Error",
            "No se ha podido completar el proceso.\n\n"
            "Revisa tus credenciales o la configuración e inténtalo de nuevo."
        )
        
        # Reactivar Boton Generar para permitir reintentos
        self.btn_generar.setEnabled(True)