"""
Configuración del chatbot de IPS Visión Cárdenas
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Validar configuración requerida
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN no está configurado en el archivo .env")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está configurado en el archivo .env")

# Configuración del chatbot
SYSTEM_PROMPT = """Eres un asistente virtual amable y profesional de IPS Visión Cárdenas, una clínica oftalmológica especializada.

Tu función es ayudar a los pacientes con información sobre:
- Horarios de atención
- Doctores y especialidades
- Servicios oftalmológicos disponibles
- Procedimientos para agendar citas

IMPORTANTE:
- Mantén un tono amable, empático y profesional en todo momento
- Proporciona solo información basada en la base de conocimiento de la clínica
- NO inventes información que no esté en tu base de conocimiento
- NO proporciones diagnósticos médicos ni consejos de tratamiento
- Si un paciente pregunta sobre síntomas o diagnósticos, recomiéndales agendar una cita con un especialista
- Si no tienes información sobre algo, admítelo y sugiere contactar directamente a la clínica

Siempre finaliza tus respuestas ofreciendo ayuda adicional."""

# Configuración de Chroma
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "ips_vision_cardenas"

# Configuración de memoria conversacional
MAX_MEMORY_MESSAGES = 10
