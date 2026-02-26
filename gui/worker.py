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
            self.log.emit("Obteniendo todas las planificaciones de turnos...")
            self.progress.emit(5)

            # Ejecuta el rascador (usa sync_playwright internamente)
            rascador.ejecutar_scraper(self.config, self.year, self.canal, usuario=self.usuario, clave=self.clave)
            self.log.emit("Planificaciones obtenidas.")
            self.progress.emit(60)

            # Generar PDF si corresponde
            if self.config.get("GENERAR_PDF", False):
                self.log.emit("Generando PDF...")
                calendarioPDF.generar_pdf(self.config)
                self.log.emit("PDF generado.")
                self.progress.emit(85)

            # Generar ICS si corresponde
            if self.config.get("GENERAR_ICS", False):
                self.log.emit("Generando archivo ICS...")
                calendarioICS.crear_ics(self.config)
                self.log.emit("Archivo ICS generado.")
                self.progress.emit(95)

            # Borrar el archivo CSV tras generar los archivos seleccionados
            import os
            out_base = self.config.get("OUTPUT", "calendario")
            csv_path = out_base + ".csv"
            try:
                if os.path.exists(csv_path):
                    os.remove(csv_path)
                    self.log.emit(f"Archivo temporal CSV eliminado: {csv_path}")
            except Exception as e:
                self.log.emit(f"No se pudo eliminar el CSV: {e}")

            self.progress.emit(100)
            self.finished_signal.emit()

        except Exception as e:
            self.error.emit(str(e))