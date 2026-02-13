# gui/dialogs.py
# Pequeñas utilidades basadas en QMessageBox para mostrar errores/confirmaciones.
from PySide6.QtWidgets import QMessageBox

def show_error(parent, title, message):
    QMessageBox.critical(parent, title, message)

def show_info(parent, title, message):
    QMessageBox.information(parent, title, message)

def show_confirm(parent, title, message):
    reply = QMessageBox.question(parent, title, message, QMessageBox.Yes | QMessageBox.No)
    return reply == QMessageBox.Yes