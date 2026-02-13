import os
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def ejecutar_scraper(config, year, usuario=None, clave=None):

    with sync_playwright() as p:

        year_str = str(year)

        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Bloqueamos imágenes para velocidad (excepto las necesarias para el filtro)
        context.route("**/*.{png,jpg,jpeg,gif}", lambda route: route.abort())
        page = context.new_page()

        try:
            print("--- INICIANDO PROCESO DE RASPADO ---")
            
            # 1. LOGIN
            print("1. Logueando en el sistema...")
            page.goto(config["AMBU_URL"])
            page.fill("#Tusuario", usuario or "")
            page.fill("#Tclave", clave or "")
            page.click("#button1")
            page.wait_for_load_state("networkidle")

            # 2. NAVEGACIÓN
            print("2. Accediendo a planificaciones...")
            page.goto(config["AMBU_PLAN_URL"])

            # 3. FILTROS
            print("3. Aplicando rango de fechas completo...")
            page.select_option("#Nprovinc", value=config["PROVINCIA_VAL"] or "617")
            
            # --- FECHA DESDE ---
            page.select_option("#dFplanifiD", value=config["DIA_DESDE"] or "01")
            page.select_option("#mFplanifiD", value=config["MES_DESDE"] or "01")
            page.select_option("#aFplanifiD", value=year_str)
            
            # --- FECHA HASTA ---
            page.select_option("#dFplanifiH", value=config["DIA_HASTA"] or "31")
            page.select_option("#mFplanifiH", value=config["MES_HASTA"] or "12")
            page.select_option("#aFplanifiH", value=year_str)

            # 4. GENERAR TABLA
            print("4. Solicitando calendario...")
            page.click('input[name="boton_calendario"]')
            
            # Esperamos a que la tabla se genere
            page.wait_for_selector("table.fila_fija", timeout=60000)
            
            # 5. ANÁLISIS
            print("5. Analizando datos...")
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            # A. DETECCIÓN DE FESTIVOS
            celdas_rojas = soup.find_all("td", bgcolor="#CC0033")
            festivos_map = set()
            for celda in celdas_rojas:
                dia_txt = celda.get_text(strip=True)
                if dia_txt.isdigit():
                    tabla = celda.find_parent("table")
                    if tabla:
                        festivos_map.add(f"{tabla.get('id')}_{dia_txt}")

            # B. EXTRACCIÓN DE TURNOS
            datos = []
            dict_nombres_bases = {}
            inputs = soup.find_all("input", value=["D", "N"])
            
            print(f"   -> Procesando {len(inputs)} registros encontrados...")

            for inp in inputs:
                # --- FILTRO VACACIONES ---
                celda_td = inp.find_parent("td")
                estilo = celda_td.get('style', '').lower() if celda_td else ""
                if "vacacionescubierta.gif" in estilo:
                    continue 

                # Extracción de datos
                anno = inp.get('data-anno')
                mes = inp.get('data-mes')
                dia = inp.get('data-dia')
                base_id = inp.get('data-situado')
                turno_val = inp.get('value').upper()

                if anno and mes and dia:
                    fecha = f"{anno}-{mes.zfill(2)}-{dia.zfill(2)}"
                    id_tabla = f"tabla_{base_id}_{anno}_{mes.zfill(2)}"
                    
                    # Nombre de la Base (Caching)
                    if base_id not in dict_nombres_bases:
                        tabla_obj = soup.find("table", id=id_tabla)
                        nombre_encontrado = "Desconocido"
                        if tabla_obj:
                            thead = tabla_obj.find("thead")
                            if thead:
                                primer_td = thead.find("td")
                                if primer_td:
                                    nombre_encontrado = primer_td.get_text(strip=True)
                        dict_nombres_bases[base_id] = nombre_encontrado
                    
                    base_nombre = dict_nombres_bases[base_id]
                    es_festivo = f"{id_tabla}_{int(dia)}" in festivos_map

                    datos.append({
                        "Fecha": fecha,
                        "Turno": turno_val,
                        "Base_Nombre": base_nombre,
                        "Base_ID": base_id,
                        "Festivo": es_festivo
                    })

            # 6. GUARDAR CSV
            if datos:
                df = pd.DataFrame(datos)
                df = df.sort_values(by=["Fecha"])
                
                # Columnas solicitadas
                df = df[["Fecha", "Turno", "Base_Nombre", "Base_ID", "Festivo"]]
                
                df.to_csv(config["OUTPUT"]+".csv", index=False, encoding="utf-8-sig")
                print(f"\n¡ÉXITO! '{config['OUTPUT']}.csv' generado correctamente.")
                print(f"Rango de fechas detectado: {df['Fecha'].min()} a {df['Fecha'].max()}")
                print(f"Total registros: {len(df)}")
            else:
                print("\nAVISO: No se encontraron datos (verifique filtros de fechas).")

        except Exception as e:
            print(f"\nERROR: {e}")
            page.screenshot(path="error_debug.png")
        finally:
            browser.close()
