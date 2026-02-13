import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import calendar
import os

class CalendarioAmbulancias(FPDF):
    def __init__(self, fecha_inicio, fecha_fin, **kwargs):
        super().__init__(**kwargs)
        self.rango_fechas = f"CALENDARIO DEL {fecha_inicio} AL {fecha_fin}"

    def header(self):
        if self.page_no() <= 2:
            self.set_font("helvetica", "B", 14)
            self.cell(0, 10, self.rango_fechas, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(2)

def generar_pdf(config):
    archivo_csv = config["OUTPUT"] + ".csv"
    if not os.path.exists(archivo_csv):
        print(f"Error: No se encuentra {archivo_csv}")
        return

    df = pd.read_csv(archivo_csv)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    f_min = df['Fecha'].min().strftime('%d/%m/%Y')
    f_max = df['Fecha'].max().strftime('%d/%m/%Y')

    pdf = CalendarioAmbulancias(fecha_inicio=f_min, fecha_fin=f_max, orientation='L', unit='mm', format='A4')
    pdf.set_margins(10, 8, 15) 
    
    meses_es = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", 
                "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    dias_letra = ["L", "M", "X", "J", "V", "S", "D"]
    resumen_datos = []

    for mes_idx, mes_nombre in enumerate(meses_es, 1):
        if (mes_idx - 1) % 6 == 0:
            pdf.add_page()
        
        d_count, n_count = 0, 0
        
        # --- CABECERA MES ---
        pdf.set_font("helvetica", "B", 9)
        pdf.set_fill_color(40, 40, 40)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(15 + (8.2 * 31), 6, mes_nombre, border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # --- FILAS DE DÍAS (MÁS FINAS: 4mm) ---
        for fila_tipo in ["letras", "numeros"]:
            pdf.set_font("helvetica", "B", 7)
            pdf.set_fill_color(245, 245, 245)
            pdf.set_text_color(0, 0, 0)
            
            # Celda vacía lateral
            pdf.cell(15, 4, "", border=1, fill=True) 
            
            ultimo_dia = calendar.monthrange(2026, mes_idx)[1]
            for d in range(1, 32):
                if d > ultimo_dia:
                    pdf.set_fill_color(220, 220, 220)
                    pdf.cell(8.2, 4, "", border=1, fill=True)
                else:
                    f_obj = pd.Timestamp(2026, mes_idx, d)
                    pdf.set_fill_color(245, 245, 245)
                    # Domingo en rojo
                    pdf.set_text_color(200, 0, 0) if f_obj.dayofweek == 6 else pdf.set_text_color(0, 0, 0)
                    
                    txt = dias_letra[f_obj.dayofweek] if fila_tipo == "letras" else str(d)
                    pdf.cell(8.2, 4, txt, border=1, align="C", fill=True)
            pdf.ln(4)

        # --- FILA DE TURNOS (ALTURA 10mm) ---
        pdf.set_font("helvetica", "B", 7)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(15, 10, "TURNO", border=1, align="C")
        
        for d in range(1, 32):
            if d > ultimo_dia:
                pdf.set_fill_color(220, 220, 220)
                pdf.cell(8.2, 10, "", border=1, fill=True)
            else:
                f_obj = pd.Timestamp(2026, mes_idx, d)
                dia_data = df[df['Fecha'] == f_obj]
                
                # Fondo rosa para domingos
                pdf.set_fill_color(255, 225, 225) if f_obj.dayofweek == 6 else pdf.set_fill_color(255, 255, 255)
                
                x, y = pdf.get_x(), pdf.get_y()
                pdf.rect(x, y, 8.2, 10, "DF")
                
                if not dia_data.empty:
                    turno = dia_data.iloc[0]['Turno']
                    nombre_base = str(dia_data.iloc[0]['Base_Nombre'])
                    
                    # Turno (D o N) arriba
                    pdf.set_font("helvetica", "B", 8)
                    pdf.set_text_color(0, 80, 180) if turno == "Día" else pdf.set_text_color(120, 0, 150)
                    pdf.set_xy(x, y + 1)
                    pdf.cell(8.2, 4, turno[0], align="C")
                    
                    # Nombre de base abajo
                    pdf.set_font("helvetica", "", 4.5)
                    pdf.set_text_color(50, 50, 50)
                    pdf.set_xy(x, y + 5.5)
                    
                    # Limpiamos nombre (Ej: ZARAUTZ-U3121 -> ZARAUTZ)
                    nombre_limpio = nombre_base.split('-')[0] if '-' in nombre_base else nombre_base
                    pdf.cell(8.2, 4, nombre_limpio, align="C")
                    
                    if turno == "Día": d_count += 1
                    else: n_count += 1
                
                pdf.set_xy(x + 8.2, y)
        
        resumen_datos.append({'Mes': mes_nombre, 'D': d_count, 'N': n_count})
        pdf.ln(12) # Espacio entre meses

    # --- PÁGINA DE RESUMEN ---
    pdf.add_page()
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 15, "RESUMEN ANUAL DE GUARDIAS", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(40, 40, 40); pdf.set_text_color(255, 255, 255)
    pdf.cell(50, 10, "MES", border=1, fill=True, align="C")
    pdf.cell(40, 10, "DÍAS (D)", border=1, fill=True, align="C")
    pdf.cell(40, 10, "NOCHES (N)", border=1, fill=True, align="C")
    pdf.cell(40, 10, "TOTAL MES", border=1, fill=True, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    total_d, total_n = 0, 0
    pdf.set_font("helvetica", "", 10); pdf.set_text_color(0, 0, 0)
    for r in resumen_datos:
        total_mes = r['D'] + r['N']
        if total_mes > 0:
            pdf.cell(50, 8, r['Mes'], border=1)
            pdf.cell(40, 8, str(r['D']), border=1, align="C")
            pdf.cell(40, 8, str(r['N']), border=1, align="C")
            pdf.cell(40, 8, str(total_mes), border=1, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            total_d += r['D']; total_n += r['N']
            
    pdf.set_font("helvetica", "B", 10); pdf.set_fill_color(230, 230, 230)
    pdf.cell(50, 10, "TOTAL ANUAL", border=1, fill=True)
    pdf.cell(40, 10, str(total_d), border=1, fill=True, align="C")
    pdf.cell(40, 10, str(total_n), border=1, fill=True, align="C")
    pdf.set_fill_color(180, 220, 180); pdf.cell(40, 10, str(total_d + total_n), border=1, fill=True, align="C")

    pdf.output(config["OUTPUT"]+".pdf")
    print("PDF generado con éxito.")
