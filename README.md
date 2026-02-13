# Generador de Calendario Ambulancias Gipuzkoa

Este proyecto automatiza la extracción de turnos de trabajo desde la plataforma Ambu App y los convierte en formatos útiles: un **PDF listo para imprimir** y un archivo **ICS para integrar en Google Calendar o Apple Calendar (iPhone)**.

![Versión](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)

---

## Características

* **Soporte Multianual:** El programa detecta el año actual y permite al usuario elegir cualquier año para generar el calendario.
* **Rascado Automático:** Accede a la web oficial y extrae los turnos del año completo.
* **Detección de Festivos:** Identifica automáticamente los días festivos (marcados en rojo en la web).
* **Generador PDF:** Crea un calendario visual organizado por meses.
* **Soporte ICS:** Genera un archivo compatible con dispositivos móviles.
* **Privacidad:** Las credenciales se introducen de forma interactiva y no se guardan en el código.

---

## Para Usuarios (Uso del .EXE)

Si no eres programador, simplemente descarga el archivo ejecutable:

1. Ve a la sección de **Releases** en este repositorio.
2. Descarga `Generador_Calendario_Ambu.exe`.
3. Ejecútalo en tu ordenador.
    * *Nota: La primera vez descargará el motor de navegación (Chromium), espera a que finalice.*
4. Introduce tu **usuario**, **contraseña** y el **año** deseado (o pulsa Enter para el año actual).
5. ¡Listo! Encontrarás `calendario.pdf` y `calendario.ics` en la misma carpeta.

---

## Para Desarrolladores

### 1. Preparación del Entorno Virtual

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd <nombre-de-la-carpeta>

# 2. Crear el entorno virtual
python -m venv venv

# 3. Activar el entorno
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Instalar navegadores de Playwright (solo la primera vez)
playwright install chromium
```

### 2. Ejecución del Script en Python

```bash
python main.py
```

### 3. Generar el ejecutable (.EXE)

Para empaquetar el proyecto en un solo archivo independiente para otros usuarios:

```bash
python -m PyInstaller --onefile --console --clean --icon="calendario.ico" --name "Generador_Calendario" main.py
```

El archivo final aparecerá en la carpeta `/dist`.

---

## Estructura del Código

El sistema es modular y centralizado:

* **`main.py`**: Puerta de entrada. Gestiona la entrada del usuario (incluyendo el año dinámico) y coordina el flujo.
* **`rascador.py`**: Motor de Playwright y BeautifulSoup.
* **`calendarioPDF.py`**: Generación de informes visuales.
* **`calendarioICS.py`**: Formateo de eventos para calendarios digitales.

---

## Notas Importantes

* **Privacidad:** Este script es una herramienta de automatización local. El inicio de sesión ocurre exclusivamente entre tu equipo y la web de destino.
* **Falsos Positivos:** Algunos antivirus pueden marcar el `.exe` como sospechoso porque realiza descargas (del motor Chromium). Es seguro ignorar el aviso.

---

## Licencia

Este proyecto es de uso personal y educativo.
