# IPS Visión Cárdenas - Chatbot de Recepción para Telegram

Chatbot inteligente de atención al cliente para la clínica oftalmológica IPS Visión Cárdenas, implementado con Telegram, LangChain, OpenAI y ChromaDB.

## 📋 Descripción

Este chatbot proporciona atención automatizada a pacientes de IPS Visión Cárdenas a través de Telegram, respondiendo consultas sobre:

- **Horarios de atención** 🕐
- **Información de doctores y especialidades** 👨‍⚕️👩‍⚕️
- **Servicios oftalmológicos disponibles** 🏥
- **Proceso para agendar citas** 📅
- **Preguntas frecuentes** ❓

### Características principales

✅ **Respuestas inteligentes** con LangChain y OpenAI  
✅ **Base de conocimiento vectorial** con ChromaDB para búsqueda semántica  
✅ **Memoria conversacional** que mantiene el contexto de la charla  
✅ **Tono amable y profesional** adaptado al sector salud  
✅ **Manejo robusto de errores** con logging detallado  
✅ **No inventa información** - solo responde con datos de la base de conocimiento  
✅ **No proporciona diagnósticos médicos** - redirige a consulta profesional

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- Cuenta de Telegram
- API Key de OpenAI
- Token de Bot de Telegram (obtener de [@BotFather](https://t.me/botfather))

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/yonydario20-cmd/APU-vision.git
   cd APU-vision
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   
   # En Linux/Mac
   source venv/bin/activate
   
   # En Windows
   venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   
   Editar el archivo `.env` con tus credenciales:
   ```env
   TELEGRAM_BOT_TOKEN=tu_token_de_telegram_aqui
   OPENAI_API_KEY=tu_api_key_de_openai_aqui
   OPENAI_MODEL=gpt-3.5-turbo
   OPENAI_TEMPERATURE=0.7
   ```

## 📱 Uso

### Iniciar el bot

```bash
python telegram_bot.py
```

El bot se iniciará y estará listo para recibir mensajes en Telegram.

### Comandos disponibles

- `/start` - Iniciar conversación con el bot
- `/help` - Mostrar ayuda y comandos disponibles
- `/limpiar` - Reiniciar la conversación (limpia el historial)

### Ejemplos de preguntas

- "¿Cuál es el horario de atención?"
- "¿Qué doctores están disponibles?"
- "¿Realizan cirugías de cataratas?"
- "¿Cómo puedo agendar una cita?"
- "¿Qué servicios oftalmológicos ofrecen?"

## 🏗️ Arquitectura del proyecto

```
APU-vision/
├── telegram_bot.py        # Bot de Telegram (punto de entrada)
├── chatbot.py            # Lógica del chatbot con LangChain
├── vector_store.py       # Gestión de ChromaDB
├── knowledge_base.py     # Base de conocimiento de la clínica
├── config.py             # Configuración y variables
├── requirements.txt      # Dependencias de Python
├── .env.example         # Plantilla de variables de entorno
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

### Componentes principales

1. **telegram_bot.py**: Interfaz de Telegram que maneja comandos y mensajes
2. **chatbot.py**: Gestiona la lógica conversacional con LangChain y OpenAI
3. **vector_store.py**: Administra ChromaDB para búsqueda semántica
4. **knowledge_base.py**: Contiene toda la información de la clínica
5. **config.py**: Centraliza configuración y prompts del sistema

## 🔧 Tecnologías utilizadas

- **[Python](https://www.python.org/)** - Lenguaje de programación
- **[python-telegram-bot](https://python-telegram-bot.org/)** - Integración con Telegram
- **[LangChain](https://www.langchain.com/)** - Framework para aplicaciones con LLM
- **[OpenAI](https://openai.com/)** - Modelo de lenguaje (GPT-3.5/4)
- **[ChromaDB](https://www.trychroma.com/)** - Base de datos vectorial
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Gestión de variables de entorno

## 🛡️ Seguridad y mejores prácticas

- ✅ **No almacena información sensible** en el código
- ✅ **Variables de entorno** para credenciales
- ✅ **Logging detallado** para debugging y monitoreo
- ✅ **Manejo de errores** en todos los componentes
- ✅ **Validación de entradas** del usuario
- ✅ **Límite de memoria conversacional** para optimizar recursos

## ⚠️ Limitaciones y consideraciones

- El bot **NO proporciona diagnósticos médicos**
- El bot **NO recomienda tratamientos**
- El bot solo responde basándose en su **base de conocimiento**
- Para emergencias, se debe acudir a servicios de urgencia
- La información proporcionada es general y orientativa

## 📝 Personalización

### Actualizar la base de conocimiento

Edita el archivo `knowledge_base.py` para agregar o modificar información:

```python
CLINIC_KNOWLEDGE = [
    {
        "category": "Nueva Categoría",
        "content": "Contenido de la nueva información..."
    }
]
```

Después de modificar, elimina la carpeta `chroma_db/` para recrear el índice vectorial.

### Ajustar el prompt del sistema

Modifica `SYSTEM_PROMPT` en `config.py` para cambiar el comportamiento del chatbot.

### Cambiar parámetros de OpenAI

Ajusta en `.env`:
- `OPENAI_MODEL`: Modelo a usar (gpt-3.5-turbo, gpt-4, etc.)
- `OPENAI_TEMPERATURE`: Creatividad (0.0 = determinista, 1.0 = creativo)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está desarrollado para IPS Visión Cárdenas.

## 👥 Autores

- Desarrollado para IPS Visión Cárdenas
- Hospital Cardenas Vision

## 📞 Soporte

Para problemas o preguntas sobre el chatbot, por favor contacta al administrador del sistema o abre un issue en GitHub.

---

**Nota**: Este chatbot es una herramienta de información general y no reemplaza la consulta médica profesional.
