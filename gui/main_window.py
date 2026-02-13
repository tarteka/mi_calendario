# gui/main_window.py
# Ventana principal: formulario de credenciales, controls, barra de progreso y log.
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QPushButton, QTextEdit, QProgressBar, QMessageBox
)
from .worker import Worker

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Calendario")
        self.worker = None
        self.setFixedSize(500, 300)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Fila: usuario / contraseña / año
        fila = QHBoxLayout()
        fila.addWidget(QLabel("Usuario:"))
        self.usuario = QLineEdit()
        fila.addWidget(self.usuario)

        fila.addWidget(QLabel("Contraseña:"))
        self.clave = QLineEdit()
        self.clave.setEchoMode(QLineEdit.Password)
        fila.addWidget(self.clave)

        fila.addWidget(QLabel("Año:"))
        self.anio = QSpinBox()
        self.anio.setRange(2026, 2050)
        # por defecto toma el año actual al arrancar (si quieres)
        from datetime import datetime
        self.anio.setValue(datetime.now().year)
        fila.addWidget(self.anio)

        layout.addLayout(fila)

        # Botones
        botones = QHBoxLayout()
        self.btn_generar = QPushButton("Generar")
        self.btn_generar.clicked.connect(self.on_generar)
        botones.addWidget(self.btn_generar)

        self.btn_salir = QPushButton("Salir")
        self.btn_salir.clicked.connect(self.close)
        botones.addWidget(self.btn_salir)

        layout.addLayout(botones)

        # Progreso y log
        self.progreso = QProgressBar()
        self.progreso.setRange(0, 100)
        self.progreso.setValue(0)
        layout.addWidget(self.progreso)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)
        self.resize(900, 480)

    @Slot()
    def on_generar(self):
        if self.worker is not None and self.worker.isRunning():
            self._append_log("Ya hay un proceso en ejecución.")
            return

        usuario = self.usuario.text().strip()
        clave = self.clave.text().strip()
        anio = int(self.anio.value())

        if not usuario or not clave:
            QMessageBox.warning(self, "Faltan datos", "Usuario y contraseña son obligatorios.")
            return

        # Configuración base (puedes extenderla)
        config = {
            "AMBU_URL": "https://ambulanciasgipuzkoa.ambu.app",
            "AMBU_PLAN_URL": "https://ambulanciasgipuzkoa.ambu.app/admin/planificaciones/",
            "PROVINCIA_VAL": "617",
            "DIA_DESDE": "01", "MES_DESDE": "01",
            "DIA_HASTA": "31", "MES_HASTA": "12",
            "OUTPUT": "calendario"
        }

        # Crear y arrancar worker (hilo)
        self.worker = Worker(config=config, year=anio, canal=None, usuario=usuario, clave=clave)
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

    @Slot()
    def _on_finished(self):
        self._append_log("Proceso finalizado correctamente.")
        self.btn_generar.setEnabled(True)
        self.progreso.setValue(100)

    @Slot(str)
    def _on_error(self, err):
        self._append_log(f"[ERROR] {err}")
        self.btn_generar.setEnabled(True)