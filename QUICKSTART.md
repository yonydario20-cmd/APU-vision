# Guía Rápida - Chatbot IPS Visión Cárdenas

## 🚀 Inicio Rápido

### Instalación (3 pasos)

1. **Configurar entorno**
   ```bash
   # Linux/Mac
   ./setup.sh
   
   # Windows
   setup.bat
   ```

2. **Configurar credenciales**
   - Edita el archivo `.env`
   - Agrega tu `TELEGRAM_BOT_TOKEN` (de @BotFather)
   - Agrega tu `OPENAI_API_KEY` (de OpenAI)

3. **Iniciar bot**
   ```bash
   python telegram_bot.py
   ```

## 📱 Uso del Bot

### Comandos
- `/start` - Inicia la conversación
- `/help` - Muestra ayuda
- `/limpiar` - Reinicia la conversación

### Ejemplos de Consultas

**Horarios**
- "¿A qué hora abren?"
- "¿Atienden los sábados?"

**Doctores**
- "¿Qué doctores tienen?"
- "¿Quién hace cirugías de cataratas?"

**Servicios**
- "¿Hacen exámenes de la vista?"
- "¿Realizan cirugía LASIK?"

**Citas**
- "¿Cómo agendo una cita?"
- "¿Qué documentos necesito?"

## 🔧 Personalización

### Actualizar Información de la Clínica

Edita `knowledge_base.py`:
```python
CLINIC_KNOWLEDGE = [
    {
        "category": "Tu Categoría",
        "content": "Tu información..."
    }
]
```

Luego elimina `chroma_db/` para recrear el índice.

### Ajustar Comportamiento

Edita `.env`:
- `OPENAI_MODEL`: Cambia el modelo (gpt-3.5-turbo, gpt-4)
- `OPENAI_TEMPERATURE`: Ajusta creatividad (0.0 - 1.0)

## 🐛 Solución de Problemas

### Error: "TELEGRAM_BOT_TOKEN no configurado"
**Solución**: Edita `.env` y agrega tu token de Telegram

### Error: "OPENAI_API_KEY no configurado"
**Solución**: Edita `.env` y agrega tu API key de OpenAI

### Bot no responde
**Solución**: 
1. Verifica que el script esté ejecutándose
2. Revisa los logs en la consola
3. Verifica tu conexión a internet

### Respuestas incorrectas
**Solución**: 
1. Actualiza `knowledge_base.py`
2. Elimina carpeta `chroma_db/`
3. Reinicia el bot

## 📊 Monitoreo

Los logs se muestran en tiempo real:
```
2024-10-29 10:30:15 - INFO - Usuario 123456 inició conversación
2024-10-29 10:30:20 - INFO - Procesando mensaje de usuario 123456
2024-10-29 10:30:22 - INFO - Respuesta generada para usuario 123456
```

## 🔐 Seguridad

✅ **Nunca** compartas tu `.env` en repositorios públicos  
✅ **Nunca** compartas tus API keys  
✅ Usa `.gitignore` para excluir archivos sensibles  
✅ Rota tus tokens periódicamente

## 📞 Soporte

- Documentación completa: `README.md`
- Issues: GitHub Issues
- Logs: Revisa la consola donde ejecutas el bot

---

**💡 Tip**: Mantén el bot ejecutándose en un servidor para disponibilidad 24/7
