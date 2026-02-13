# gui/worker.py
# QThread que ejecuta la lógica de rascado y generación de archivos sin bloquear la UI.
from PySide6.QtCore import QThread, Signal
import traceback

# importamos las funciones existentes del repo (mantener ficheros rascador.py, calendarioPDF.py, calendarioICS.py)
import services.rascador as rascador
import services.calendarioPDF as calendarioPDF
import services.calendarioICS as calendarioICS

class Worker(QThread):
    log = Signal(str)
    progress = Signal(int)
    finished_signal = Signal()
    error = Signal(str)

    def __init__(self, config, year, canal=None, usuario=None, clave=None):
        super().__init__()
        self.config = config
        self.year = year
        self.canal = canal
        self.usuario = usuario
        self.clave = clave

    def run(self):
        try:
            self.log.emit("Iniciando scraping...")
            self.progress.emit(5)

            # Ejecuta el rascador (usa sync_playwright internamente)
            rascador.ejecutar_scraper(self.config, self.year, self.canal, usuario=self.usuario, clave=self.clave)
            self.log.emit("Scraping completado.")
            self.progress.emit(60)

            # Generar PDF (usa calendarioPDF.generar_pdf)
            self.log.emit("Generando PDF...")
            calendarioPDF.generar_pdf(self.config)
            self.log.emit("PDF generado.")
            self.progress.emit(85)

            # Generar ICS (usa calendarioICS.crear_ics)
            self.log.emit("Generando ICS...")
            calendarioICS.crear_ics(self.config)
            self.log.emit("ICS generado.")
            self.progress.emit(95)

            self.finished_signal.emit()
            self.progress.emit(100)
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(str(e))
            self.log.emit("Trazado de la excepción:\n" + tb)