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
python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --clean ^
  --icon="assets/icon.ico" ^
  --add-data "assets;assets" ^
  --add-data "gui;gui" ^
  --add-data "config.json;." ^
  --exclude-module PySide6.Qt3DAnimation ^
  --exclude-module PySide6.Qt3DCore ^
  --exclude-module PySide6.Qt3DExtras ^
  --exclude-module PySide6.Qt3DInput ^
  --exclude-module PySide6.Qt3DLogic ^
  --exclude-module PySide6.Qt3DRender ^
  --exclude-module PySide6.QtCharts ^
  --exclude-module PySide6.QtDataVisualization ^
  --exclude-module PySide6.QtMultimedia ^
  --exclude-module PySide6.QtMultimediaWidgets ^
  --exclude-module PySide6.QtQml ^
  --exclude-module PySide6.QtQuick ^
  --exclude-module PySide6.QtQuick3D ^
  --exclude-module PySide6.QtQuickControls2 ^
  --exclude-module PySide6.QtQuickWidgets ^
  --exclude-module PySide6.QtWebChannel ^
  --exclude-module PySide6.QtWebEngineCore ^
  --exclude-module PySide6.QtWebEngineWidgets ^
  --exclude-module PySide6.QtWebSockets ^
  --exclude-module PySide6.QtSpatialAudio ^
  --exclude-module PySide6.QtTextToSpeech ^
  --exclude-module PySide6.QtSensors ^
  --exclude-module PySide6.QtSerialPort ^
  --exclude-module PySide6.QtRemoteObjects ^
  --exclude-module PySide6.QtStateMachine ^
  --exclude-module PySide6.QtScxml ^
  --exclude-module tkinter ^
  --exclude-module tzdata ^
  --exclude-module lib2to3 ^
  --exclude-module unittest ^
  --name "Generador_Calendario" ^
  main.py

if %errorlevel% equ 0 (
    echo.
    echo ✓ Compilacion completada exitosamente
    echo El ejecutable esta en: dist\Generador_Calendario.exe
) else (
    echo.
    echo ✗ Error durante la compilacion
    pause
)
