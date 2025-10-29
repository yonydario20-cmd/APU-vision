@echo off
REM Script de configuración para el chatbot de IPS Visión Cárdenas (Windows)

echo ==========================================
echo IPS Vision Cardenas - Chatbot Setup
echo ==========================================
echo.

REM Verificar Python
echo 1. Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo    X Python no esta instalado
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo    √ Python encontrado: %PYTHON_VERSION%
echo.

REM Crear entorno virtual si no existe
echo 2. Configurando entorno virtual...
if not exist "venv" (
    echo    Creando entorno virtual...
    python -m venv venv
    echo    √ Entorno virtual creado
) else (
    echo    √ Entorno virtual ya existe
)
echo.

REM Activar entorno virtual
echo 3. Activando entorno virtual...
call venv\Scripts\activate.bat
echo    √ Entorno virtual activado
echo.

REM Actualizar pip
echo 4. Actualizando pip...
python -m pip install --upgrade pip --quiet
echo    √ pip actualizado
echo.

REM Instalar dependencias
echo 5. Instalando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo    X Error al instalar dependencias
    pause
    exit /b 1
)
echo    √ Dependencias instaladas correctamente
echo.

REM Verificar archivo .env
echo 6. Verificando configuracion...
if not exist ".env" (
    echo    ⚠ Archivo .env no encontrado
    echo    Creando .env desde .env.example...
    copy .env.example .env >nul
    echo    √ Archivo .env creado
    echo.
    echo    ⚠ IMPORTANTE: Edita el archivo .env con tus credenciales:
    echo      - TELEGRAM_BOT_TOKEN (obten de @BotFather en Telegram^)
    echo      - OPENAI_API_KEY (obten de https://platform.openai.com^)
) else (
    echo    √ Archivo .env encontrado
)
echo.

echo ==========================================
echo √ Instalacion completada
echo ==========================================
echo.
echo Proximos pasos:
echo 1. Edita el archivo .env con tus credenciales
echo 2. Ejecuta: python telegram_bot.py
echo.
echo Para mas informacion, consulta README.md
echo.
pause
