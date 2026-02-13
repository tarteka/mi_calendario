import sys
import subprocess
import getpass
import rascador as scraper
import calendarioPDF
import calendarioICS
import multiprocessing
from playwright.sync_api import sync_playwright
from datetime import datetime

# --- CONFIGURACIÓN ---
CONFIG = {
    "AMBU_URL": "https://ambulanciasgipuzkoa.ambu.app",
    "AMBU_PLAN_URL": "https://ambulanciasgipuzkoa.ambu.app/admin/planificaciones/",
    "PROVINCIA_VAL": "617",
    "DIA_DESDE": "01", "MES_DESDE": "01",
    "DIA_HASTA": "31", "MES_HASTA": "12",
    "OUTPUT": "calendario"
}

def preparar_navegador():
    """
    Intenta detectar Chrome/Edge en el sistema.
    Si no se encuentra, se descargará el motor de Playwright automáticamente.
    """
    print("Comprobando motor de navegación...")

    with sync_playwright() as p:
        # 1. Intentamos con Chrome del sistema
        try:
            browser = p.chromium.launch(channel="chrome", headless=True)
            browser.close()
            print("Utilizando Google Chrome del sistema.")
            return "chrome"
        except:
            pass

        # 2. Intentamos con Edge del sistema
        try:
            browser = p.chromium.launch(channel="msedge", headless=True)
            browser.close()
            print("Utilizando Microsoft Edge del sistema.")
            return "msedge"
        except:
            pass

        # 3. Si llegamos aquí, no hay navegador compatible. Intentamos usar el de Playwright.
        try:
            # Intentamos lanzarlo para ver si ya se descargó antes
            browser = p.chromium.launch(headless=True)
            browser.close()
            print("Utilizando motor Chromium propio.")
            return None # None significa que usará el default de Playwright
        except:
            print("No se encontró ningún navegador. Descargando componentes necesarios...")
            # Aquí es donde el freeze_support es vital para evitar el bucle
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
            print("Instalación completada.")
            return None

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Necesario para PyInstaller en Windows   
    try:
        print("==========================================")
        print("   GENERADOR DE CALENDARIO AMBULANCIAS")
        print("==========================================\n")
        
        # Guardamos qué canal vamos a usar
        canal_navegador = preparar_navegador()

        # Obtener el año actual automáticamente
        current_year = datetime.now().year
        
        # --- ENTRADA DE USUARIO ---
        print("Por favor, introduce tus credenciales de la web:")
        user_input = input("Usuario: ")
        # getpass oculta la escritura por seguridad
        pass_input = getpass.getpass("Contraseña: ")
        # Año del calendario (opcional, por defecto es el actual)
        print("Año del calendario:")
        year_input = input(f"Año (por defecto {current_year}): ")
        
        if not user_input or not pass_input:
            print("\n[ERROR]: El usuario y la contraseña son obligatorios.")
            sys.exit()

        # Ejecutamos el rascado pasando las variables directamente
        year = int(year_input) if year_input.isdigit() else current_year
        scraper.ejecutar_scraper(CONFIG, year, canal_navegador, user_input, pass_input)
        
        print("\nGenerando PDF...")
        calendarioPDF.generar_pdf(CONFIG)
        
        print("Generando archivo ICS para el móvil...")
        calendarioICS.crear_ics(CONFIG)
        
        print("\n==========================================")
        print("   ¡TODO LISTO CON ÉXITO!")
        print("==========================================")
        
    except Exception as e:
        print(f"\n[ERROR]: Ha ocurrido un fallo: {e}")
    
    input("\nPresiona ENTER para salir...")