@echo off
REM Script para compilar el ejecutable con PyInstaller (desde venv)

REM Activar venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Venv activado
) else (
    echo ✗ Error: No se encontro venv en venv\Scripts\activate.bat
    pause
    exit /b 1
)

echo.
echo Compilando ejecutable...
python -m PyInstaller --onefile --windowed --clean --collect-all PySide6 --icon="assets/icon.ico" --add-data "assets;assets" --add-data "gui;gui" --name "Generador_Calendario" main.py

if %errorlevel% equ 0 (
    echo.
    echo ✓ Compilacion completada exitosamente
    echo El ejecutable esta en: dist\Generador_Calendario.exe
) else (
    echo.
    echo ✗ Error durante la compilacion
    pause
)
