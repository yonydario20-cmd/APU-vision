# Arquitectura del Chatbot - IPS Visión Cárdenas

## 📐 Diseño de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                    Usuario de Telegram                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Mensajes
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  telegram_bot.py                             │
│  - Maneja comandos (/start, /help, /limpiar)               │
│  - Gestiona eventos de Telegram                             │
│  - Maneja errores de comunicación                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Mensajes procesados
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    chatbot.py                                │
│  - Gestiona conversaciones por usuario                      │
│  - Mantiene memoria conversacional                          │
│  - Coordina LangChain + OpenAI                             │
└──────┬──────────────────────────────────┬───────────────────┘
       │                                  │
       │ Consulta                         │ Respuesta
       ▼                                  │
┌─────────────────────┐                  │
│  vector_store.py    │                  │
│  - ChromaDB         │                  │
│  - Embeddings       │                  │
│  - Búsqueda         │                  │
│    semántica        │                  │
└──────┬──────────────┘                  │
       │                                  │
       │ Documentos                       │
       │ relevantes                       │
       │                                  │
       └──────────────────────────────────┘
                     │
                     │ Contexto
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              OpenAI (GPT-3.5-turbo/GPT-4)                   │
│  - Genera respuestas contextuales                          │
│  - Mantiene tono profesional                               │
└─────────────────────────────────────────────────────────────┘
```

## 🗂️ Componentes Principales

### 1. telegram_bot.py
**Responsabilidad**: Interfaz con Telegram

**Funcionalidades**:
- Manejo de comandos del bot
- Procesamiento de mensajes entrantes
- Gestión de errores de comunicación
- Logging de actividad

**Patrones utilizados**:
- Command Pattern (para comandos)
- Error Handler Pattern

### 2. chatbot.py
**Responsabilidad**: Lógica de negocio del chatbot

**Funcionalidades**:
- Gestión de conversaciones por usuario
- Integración LangChain + OpenAI
- Memoria conversacional (ventana deslizante)
- Orquestación de retrieval y generación

**Patrones utilizados**:
- Factory Pattern (creación de conversaciones)
- Strategy Pattern (diferentes tipos de respuestas)

### 3. vector_store.py
**Responsabilidad**: Gestión de base de conocimiento vectorial

**Funcionalidades**:
- Inicialización de ChromaDB
- Embeddings de documentos
- Búsqueda por similitud semántica
- Persistencia de datos

**Patrones utilizados**:
- Singleton Pattern (instancia única)
- Repository Pattern

### 4. knowledge_base.py
**Responsabilidad**: Almacenamiento de información de la clínica

**Estructura**:
```python
CLINIC_KNOWLEDGE = [
    {
        "category": "Nombre de categoría",
        "content": "Contenido detallado..."
    }
]
```

**Categorías incluidas**:
1. Información General
2. Horarios de Atención
3. Doctores y Especialidades
4. Servicios Oftalmológicos
5. Proceso de Citas
6. Preguntas Frecuentes
7. Consejos de Salud Visual

### 5. config.py
**Responsabilidad**: Configuración centralizada

**Contiene**:
- Variables de entorno
- Prompt del sistema
- Parámetros de OpenAI
- Configuración de ChromaDB

## 🔄 Flujo de Procesamiento

### Flujo de un Mensaje

1. **Usuario envía mensaje** → Telegram
2. **telegram_bot.py recibe** → Valida y logea
3. **chatbot.py procesa** → Identifica o crea conversación
4. **vector_store.py busca** → Encuentra documentos relevantes
5. **LangChain construye prompt** → Combina contexto + pregunta
6. **OpenAI genera respuesta** → Basándose en el prompt
7. **chatbot.py valida** → Verifica calidad de respuesta
8. **telegram_bot.py envía** → Devuelve al usuario

### Flujo de Memoria Conversacional

```python
# Ejemplo de memoria
Conversación Usuario A:
├─ Mensaje 1: "¿Cuál es el horario?"
├─ Respuesta 1: "Lunes a Viernes 8 AM - 6 PM..."
├─ Mensaje 2: "¿Y los sábados?"
└─ Respuesta 2: "Los sábados de 8 AM - 12 PM..."

# La memoria permite contexto ("¿Y los sábados?" hace referencia a horarios)
```

## 🎯 Decisiones de Diseño

### 1. ChromaDB para Vector Store
**Razón**: 
- Búsqueda semántica eficiente
- Fácil integración con LangChain
- Persistencia local sin dependencias externas

### 2. ConversationBufferWindowMemory
**Razón**:
- Mantiene contexto limitado (últimos N mensajes)
- Evita exceder límites de tokens
- Balance entre memoria y eficiencia

### 3. Separación de Concerns
**Razón**:
- Telegram Bot → Solo manejo de eventos
- Chatbot → Solo lógica conversacional
- Vector Store → Solo gestión de conocimiento
- Facilita testing y mantenimiento

### 4. Logging Exhaustivo
**Razón**:
- Debugging más fácil
- Monitoreo de actividad
- Auditoría de interacciones

### 5. Error Handling en Capas
**Razón**:
- Cada capa maneja sus propios errores
- Mensajes amigables para usuarios
- Logs técnicos para desarrolladores

## 🔐 Seguridad

### Medidas Implementadas

1. **Variables de entorno** para credenciales
2. **.gitignore** para archivos sensibles
3. **Validación de inputs** del usuario
4. **Límite de memoria** por conversación
5. **No almacenamiento** de datos sensibles

### Datos NO Almacenados

- ❌ Información personal de usuarios
- ❌ Datos médicos
- ❌ Credenciales en código
- ❌ API keys en repositorio

## 📊 Escalabilidad

### Actual (MVP)
- ✅ Múltiples usuarios simultáneos
- ✅ Memoria por usuario (en memoria)
- ✅ Vector store local

### Futuras Mejoras Posibles
- 🔄 Base de datos para persistir conversaciones
- 🔄 Redis para memoria distribuida
- 🔄 API REST para múltiples frontends
- 🔄 Analytics de conversaciones
- 🔄 A/B testing de prompts

## 🧪 Testing

### Niveles de Testing

1. **Unit Tests**: Funciones individuales
2. **Integration Tests**: Componentes juntos
3. **Manual Tests**: Interacción real con bot

### Áreas Críticas para Testing

- ✅ Vector store initialization
- ✅ Knowledge base structure
- ✅ Error handling
- ✅ Memory management
- ⚠️ Integration con Telegram (requiere token)
- ⚠️ Integration con OpenAI (requiere API key)

## 📈 Monitoreo y Observabilidad

### Logs Disponibles

```python
# Información general
logger.info("Usuario 123 inició conversación")

# Procesamiento
logger.info("Procesando mensaje de usuario 123")

# Errores
logger.error("Error al procesar: [detalle]")
```

### Métricas Importantes

1. **Número de conversaciones activas**
2. **Tiempo de respuesta**
3. **Errores por tipo**
4. **Consultas más frecuentes**

## 🔄 Mantenimiento

### Tareas Regulares

1. **Actualizar knowledge_base.py** con nueva información
2. **Revisar logs** para detectar problemas
3. **Actualizar dependencias** periódicamente
4. **Rotar API keys** por seguridad
5. **Backup de chroma_db/** si se personaliza

### Actualizaciones de Contenido

```bash
# 1. Editar knowledge_base.py
# 2. Eliminar índice antiguo
rm -rf chroma_db/
# 3. Reiniciar bot (recreará índice)
python telegram_bot.py
```

## 📚 Referencias

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [python-telegram-bot Docs](https://docs.python-telegram-bot.org/)

---

**Última actualización**: Octubre 2025  
**Versión**: 1.0.0
