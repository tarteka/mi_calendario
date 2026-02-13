# main.py
# Entry point principal: inicia la GUI (reemplaza el CLI)
import multiprocessing
from gui.app import run_app

if __name__ == "__main__":
    multiprocessing.freeze_support()  # útil si más tarde empaquetas en Windows
    run_app()