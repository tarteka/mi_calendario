# Generador de Calendario Ambulancias Gipuzkoa

Este proyecto automatiza la extracción de turnos de trabajo desde la plataforma Ambu App y los convierte en formatos útiles: un **PDF listo para imprimir** y un archivo **ICS para integrar en Google Calendar o Apple Calendar (iPhone)**.

[![Download v2.3.0](https://img.shields.io/badge/descargar_exe-v2.3.0-orange.svg)](https://github.com/tarteka/mi_calendario/releases/download/v2.3.0/Generador_Calendario_v2.3.0.exe)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)

---

## Características

* **Opción de año:** El programa detecta el año actual y permite al usuario elegir cualquier año para generar el calendario.
* **Rascado Automático:** Accede a la web oficial y extrae los turnos del año completo.
* **Detección de Festivos:** Identifica automáticamente los días festivos (marcados en rojo en la web).
* **Generador PDF:** Crea un calendario visual organizado por meses.
* **Soporte ICS:** Genera un archivo compatible con dispositivos móviles.
* **Privacidad:** Las credenciales se introducen de forma interactiva y no se guardan en el código.

---

## Para Usuarios (Uso del .EXE)

Si no eres programador, simplemente descarga el archivo ejecutable:

1. Ve a la sección de **Releases** en este repositorio.
2. Descarga `Generador_Calendario.exe`.
3. Ejecútalo en tu ordenador.
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
```

### 2. Ejecución del Script en Python

```bash
python main.py
```

### 3. Generar el ejecutable (.EXE)

Para empaquetar el proyecto en un solo archivo independiente para otros usuarios:

```bash
build.bat
```

El archivo final aparecerá en la carpeta `/dist`.

---

## Cómo lanzar una nueva versión (Releases)

Usaremos **GitHub Actions** y los **tags**

### Pasos para publicar una actualización

1. **Prepara tus cambios:**
   Asegúrate de que el código funciona y de haber actualizado la variable `VERSION` en tu script principal si fuera necesario.

2. **Sube los cambios a la rama principal:**

   ```bash
   git add .
   git commit -m "Descripción de las mejoras"
   git push origin main
   ```

3. **Crea y sube el Tag de versión**

Elige el número de versión siguiendo el estándar (ej: `v1.1.0`).

```bash
# Crear el tag localmente
git tag -a v1.1.0 -m "Versión 1.1.0: Resumen de cambios"

# Subir el tag a GitHub
git push origin v1.1.0
```

GitHub detectará el tag, levantará un servidor con Windows, compilará el .exe ccreará una nueva entrada en la sección `Releases` automáticamente.

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
