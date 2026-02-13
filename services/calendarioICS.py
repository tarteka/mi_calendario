import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import os

def crear_ics(config):
    archivo_csv = config["OUTPUT"] + ".csv"
    if not os.path.exists(archivo_csv):
        print(f"Error: No se encuentra {archivo_csv}")
        return

    df = pd.read_csv(archivo_csv)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    cal = Calendar()
    cal.add('prodid', '-//Calendario de Turnos Ambulancias Gipuzkoa//mx//')
    cal.add('version', '2.0')

    print(f"Generando eventos desde {archivo_csv}...")

    for _, fila in df.iterrows():
        evento = Event()
        base = fila['Base_Nombre']
        turno = fila['Turno']
        fecha = fila['Fecha']

        # Configuración de horarios
        if turno == "D": # Día
            inicio = fecha.replace(hour=8, minute=0)
            fin = fecha.replace(hour=20, minute=0)
            resumen = f"☀️ Día - {base}"
        else: # Noche
            inicio = fecha.replace(hour=20, minute=0)
            fin = inicio + timedelta(hours=12) # Termina a las 08:00 del día siguiente
            resumen = f"🌙 Noche - {base}"

        evento.add('summary', resumen)
        evento.add('dtstart', inicio)
        evento.add('dtend', fin)
        evento.add('description', f"Turno de {turno} en la base {base}. Festivo: {fila['Festivo']}")
        
        cal.add_component(evento)

    nombre_archivo = config["OUTPUT"]+".ics"
    with open(nombre_archivo, 'wb') as f:
        f.write(cal.to_ical())
    
    print(f"¡HECHO! Archivo '{nombre_archivo}' generado listo para importar.")
