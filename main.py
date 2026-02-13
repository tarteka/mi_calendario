import sys
import subprocess
import getpass
import rascador as scraper
import calendarioPDF
import calendarioICS
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

def instalar_playwright_si_falta():
    print("Comprobando motor de navegación...")
    try:
        with sync_playwright() as p:
            p.chromium.launch()
        print("Motor de navegación listo.")
    except Exception:
        print("Motor no encontrado. Descargando componentes...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("Instalación completada.\n")

if __name__ == "__main__":
    try:
        print("==========================================")
        print("   GENERADOR DE CALENDARIO AMBULANCIAS")
        print("==========================================\n")
        
        instalar_playwright_si_falta()

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
        scraper.ejecutar_scraper(CONFIG, year, user_input, pass_input)
        
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