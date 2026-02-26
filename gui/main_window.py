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

        # Chequeo de actualización en segundo plano
        self._start_update_check_thread()

    def _start_update_check_thread(self):
        from PySide6.QtCore import QThread, Signal, QObject
        from gui.update_service import check_for_updates

        class UpdateWorker(QObject):
            finished = Signal(object)
            def run(self):
                update = check_for_updates()
                self.finished.emit(update)

        self._update_thread = QThread()
        self._update_worker = UpdateWorker()
        self._update_worker.moveToThread(self._update_thread)
        self._update_thread.started.connect(self._update_worker.run)
        self._update_worker.finished.connect(self._on_update_check_finished)
        self._update_worker.finished.connect(self._update_thread.quit)
        self._update_worker.finished.connect(self._update_worker.deleteLater)
        self._update_thread.finished.connect(self._update_thread.deleteLater)
        self._update_thread.start()

    def _on_update_check_finished(self, update):
        if update:
            msg = f"Hay una nueva versión disponible: {update.version}.\n¿Deseas descargar e instalar la actualización ahora?"
            # Botones personalizados: Sí y Más tarde
            si_btn = QMessageBox.Yes
            mas_tarde_btn = QMessageBox.No
            box = QMessageBox(self)
            box.setWindowTitle("Actualización disponible")
            box.setText(msg)
            box.setIcon(QMessageBox.Question)
            box.setStandardButtons(si_btn | mas_tarde_btn)
            box.button(si_btn).setText("Sí")
            box.button(mas_tarde_btn).setText("Más tarde")
            reply = box.exec()
            if reply == si_btn:
                from gui.update_service import download_and_install
                download_and_install(update, self)
        
    def actualizar_texto(self, valor: int):
        """Muestra el % solo si el valor es mayor que 0"""
        self.progreso.setTextVisible(valor > 0)
        
    def _build_ui(self):
        # ...existing code...
        # (todo el resto del layout...)

        # --- Aquí va la construcción del layout principal y widgets ---
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
        self.usuario.textChanged.connect(self._update_output_path)

        self.clave = QLineEdit()
        self.clave.setPlaceholderText("Contraseña de Lotura")
        self.clave.setEchoMode(QLineEdit.Password)
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
        self.anio.currentTextChanged.connect(self._update_output_path)
        form.addRow(QLabel("Año:"), self.anio)

        cred_box.setLayout(form)
        layout.addWidget(cred_box)

        # Fila: ruta de salida (editable mediante diálogo)
        outfila = QHBoxLayout()
        outfila.setSpacing(8)
        outfila.addWidget(QLabel("Guardar en:"))
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)
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

        # Selección de tipos de archivo a generar (checkbox + descripción a la derecha)
        tipo_archivo_box = QGroupBox("Archivos a crear:")
        tipo_archivo_vlayout = QVBoxLayout()
        tipo_archivo_vlayout.setSpacing(6)
        pdf_layout = QHBoxLayout()
        self.chk_pdf = QCheckBox("Generar PDF")
        self.chk_pdf.setChecked(True)
        pdf_layout.addWidget(self.chk_pdf)
        pdf_desc = QLabel("<span style='color:#555;font-size:10pt;'>Calendario visual para imprimir o compartir.</span>")
        pdf_desc.setWordWrap(False)
        pdf_layout.addWidget(pdf_desc)
        pdf_layout.addStretch()
        tipo_archivo_vlayout.addLayout(pdf_layout)
        ics_layout = QHBoxLayout()
        self.chk_ics = QCheckBox("Generar ICS")
        self.chk_ics.setChecked(True)
        ics_layout.addWidget(self.chk_ics)
        ics_desc = QLabel("<span style='color:#555;font-size:10pt;'>Archivo compatible con Google/Apple Calendar.</span>")
        ics_desc.setWordWrap(False)
        ics_layout.addWidget(ics_desc)
        ics_layout.addStretch()
        tipo_archivo_vlayout.addLayout(ics_layout)
        tipo_archivo_box.setLayout(tipo_archivo_vlayout)
        layout.addWidget(tipo_archivo_box)

        # Botones
        botones = QHBoxLayout()
        botones.setSpacing(12)
        self.btn_about = QPushButton("Acerca de")
        self.btn_generar = QPushButton("Generar")
        self.btn_salir = QPushButton("Salir")
        self.btn_about.setObjectName("btn_about")
        self.btn_generar.setObjectName("btn_generar")
        self.btn_salir.setObjectName("btn_salir")
        self.btn_about.clicked.connect(self._show_about)
        self.btn_generar.clicked.connect(self.on_generar)
        self.btn_salir.clicked.connect(self.close)
        self.btn_about.setIcon(QIcon(str(self.ICON_PATH / "info.svg")))
        self.btn_generar.setIcon(QIcon(str(self.ICON_PATH / "play.svg")))
        self.btn_salir.setIcon(QIcon(str(self.ICON_PATH / "exit.svg")))
        self.btn_about.setIconSize(QSize(16, 16))
        self.btn_generar.setIconSize(QSize(16, 16))
        self.btn_salir.setIconSize(QSize(16, 16))
        botones.addWidget(self.btn_about)
        botones.addStretch()
        botones.addWidget(self.btn_generar)
        botones.addWidget(self.btn_salir)
        layout.addLayout(botones)

        # Progreso y log
        self.progreso = QProgressBar()
        self.progreso.setRange(0, 100)
        self.progreso.setValue(0)
        self.progreso.setTextVisible(False)
        self.progreso.valueChanged.connect(self.actualizar_texto)
        layout.addWidget(self.progreso)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(120)
        layout.addWidget(self.log)

        # El botón de actualización se moverá al diálogo Acerca de

        # Para QMainWindow usamos un widget central
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def _check_update_gui(self):
        from gui.update_service import ask_and_update
        ask_and_update(self)

    def _update_output_path(self):
        """Actualiza el campo de ruta de salida según usuario y año."""
        usuario = self.usuario.text().strip().replace(" ", "_")
        anio = self.anio.currentText()
        if usuario and anio:
            base_path = Path(self.output_base).parent if hasattr(self, 'output_base') else Path.home()
            nombre_archivo = f"calendario-{usuario}-{anio}"
            nueva_ruta = str(base_path / nombre_archivo)
            self.output_path.setText(nueva_ruta)
        else:
            # Si falta usuario o año, mostrar solo la carpeta base
            self.output_path.setText(self.output_base)

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

        # Validar que al menos uno de los tipos de archivo esté seleccionado
        if not (self.chk_pdf.isChecked() or self.chk_ics.isChecked()):
            QMessageBox.warning(self, "Faltan opciones", "Debes seleccionar al menos un tipo de archivo (PDF y/o ICS) a generar.")
            return


        # Modificar el nombre base del archivo de salida: calendario-usuario-año
        nombre_usuario = usuario.replace(" ", "_")
        nombre_archivo = f"calendario-{nombre_usuario}-{anio}"
        # Mantener la ruta base elegida por el usuario, pero cambiar el nombre
        base_path = Path(self.output_base).parent
        self.output_base = str(base_path / nombre_archivo)
        self.output_path.setText(self.output_base)

        # Limpiar los campos de usuario y contraseña
        self.usuario.clear()
        self.clave.clear()

        # Configuración para el worker (puede ser ampliada con más opciones si es necesario)
        config = load_config()
        config["OUTPUT"] = self.output_base
        config["GENERAR_PDF"] = self.chk_pdf.isChecked()
        config["GENERAR_ICS"] = self.chk_ics.isChecked()

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

        # Intentar abrir el PDF generado automáticamente
        pdf_path = Path(self.output_base).with_suffix('.pdf')
        if pdf_path.exists():
            try:
                import subprocess
                subprocess.Popen(["xdg-open", str(pdf_path)])
                self._append_log(f"Abriendo PDF: {pdf_path}")
            except Exception as e:
                self._append_log(f"No se pudo abrir el PDF automáticamente: {e}")

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