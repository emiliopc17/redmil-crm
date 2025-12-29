@echo off
echo 🎵 Iniciando Invoice Manager Pro - REDMIL Honduras...

:: Verificar si Docker está corriendo
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no parece estar iniciado. 
    echo Por favor, abre 'Docker Desktop' y espera a que el icono este en verde.
    pause
    exit /b
)

echo [INFO] Docker detectado. Levantando servicios...
docker compose up -d --build

echo [OK] Servicios levantados correctamente.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Presiona cualquier tecla para ver los logs...
pause
docker compose logs -f
