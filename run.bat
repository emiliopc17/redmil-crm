@echo off
echo ==========================================
echo   REDMIL Quoter Pro - Launcher
echo ==========================================

REM Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python no fue detectado en el sistema.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo IMPORTANTE: Marca la casilla "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b
)

echo [INFO] Python detectado. Verificando dependencias...
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Hubo un problema instalando las librerias.
    pause
    exit /b
)

echo [INFO] Iniciando aplicacion...
python -m streamlit run app.py

pause
