#!/bin/bash
# Script de configuración para el chatbot de IPS Visión Cárdenas

echo "=========================================="
echo "IPS Visión Cárdenas - Chatbot Setup"
echo "=========================================="
echo ""

# Verificar Python
echo "1. Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "   ✗ Python 3 no está instalado"
    exit 1
fi
echo "   ✓ Python 3 encontrado: $(python3 --version)"
echo ""

# Crear entorno virtual si no existe
echo "2. Configurando entorno virtual..."
if [ ! -d "venv" ]; then
    echo "   Creando entorno virtual..."
    python3 -m venv venv
    echo "   ✓ Entorno virtual creado"
else
    echo "   ✓ Entorno virtual ya existe"
fi
echo ""

# Activar entorno virtual
echo "3. Activando entorno virtual..."
source venv/bin/activate
echo "   ✓ Entorno virtual activado"
echo ""

# Actualizar pip
echo "4. Actualizando pip..."
pip install --upgrade pip --quiet
echo "   ✓ pip actualizado"
echo ""

# Instalar dependencias
echo "5. Instalando dependencias..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "   ✓ Dependencias instaladas correctamente"
else
    echo "   ✗ Error al instalar dependencias"
    exit 1
fi
echo ""

# Verificar archivo .env
echo "6. Verificando configuración..."
if [ ! -f ".env" ]; then
    echo "   ⚠ Archivo .env no encontrado"
    echo "   Creando .env desde .env.example..."
    cp .env.example .env
    echo "   ✓ Archivo .env creado"
    echo ""
    echo "   ⚠ IMPORTANTE: Edita el archivo .env con tus credenciales:"
    echo "     - TELEGRAM_BOT_TOKEN (obtén de @BotFather en Telegram)"
    echo "     - OPENAI_API_KEY (obtén de https://platform.openai.com)"
else
    echo "   ✓ Archivo .env encontrado"
fi
echo ""

echo "=========================================="
echo "✓ Instalación completada"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "1. Edita el archivo .env con tus credenciales"
echo "2. Ejecuta: python telegram_bot.py"
echo ""
echo "Para más información, consulta README.md"
echo ""
