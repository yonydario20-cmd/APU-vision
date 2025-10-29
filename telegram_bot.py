"""
Bot de Telegram para IPS Visión Cárdenas
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from config import TELEGRAM_BOT_TOKEN
from chatbot import ChatbotManager

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBot:
    """Bot de Telegram para la clínica oftalmológica"""
    
    def __init__(self):
        """Inicializa el bot de Telegram"""
        self.chatbot_manager = ChatbotManager()
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja el comando /start
        
        Args:
            update: Actualización de Telegram
            context: Contexto de la conversación
        """
        try:
            user = update.effective_user
            logger.info(f"Usuario {user.id} ({user.first_name}) inició conversación")
            
            welcome_message = (
                f"¡Hola {user.first_name}! 👋\n\n"
                "Bienvenido a *IPS Visión Cárdenas* 👁️\n\n"
                "Soy tu asistente virtual y estoy aquí para ayudarte con:\n"
                "• Horarios de atención 🕐\n"
                "• Información sobre nuestros doctores 👨‍⚕️👩‍⚕️\n"
                "• Servicios oftalmológicos disponibles 🏥\n"
                "• Proceso para agendar citas 📅\n\n"
                "Por favor, escríbeme tu pregunta y con gusto te atenderé.\n\n"
                "_Recuerda: No proporciono diagnósticos médicos. "
                "Para consultas sobre tu salud visual, agenda una cita con nuestros especialistas._"
            )
            
            await update.message.reply_text(welcome_message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error en comando /start: {str(e)}")
            await update.message.reply_text(
                "Disculpa, hubo un error al iniciar. Por favor, intenta nuevamente."
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja el comando /help
        
        Args:
            update: Actualización de Telegram
            context: Contexto de la conversación
        """
        try:
            help_message = (
                "*Comandos disponibles:* 📋\n\n"
                "/start - Iniciar conversación\n"
                "/help - Mostrar esta ayuda\n"
                "/limpiar - Iniciar nueva conversación\n\n"
                "*Puedes preguntarme sobre:*\n"
                "• ¿Cuál es el horario de atención?\n"
                "• ¿Qué doctores están disponibles?\n"
                "• ¿Qué servicios ofrecen?\n"
                "• ¿Cómo puedo agendar una cita?\n"
                "• ¿Realizan cirugías de cataratas?\n"
                "• Y mucho más...\n\n"
                "Simplemente escribe tu pregunta y te responderé de inmediato. 😊"
            )
            
            await update.message.reply_text(help_message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error en comando /help: {str(e)}")
            await update.message.reply_text(
                "Disculpa, hubo un error. Por favor, intenta nuevamente."
            )
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja el comando /limpiar para reiniciar la conversación
        
        Args:
            update: Actualización de Telegram
            context: Contexto de la conversación
        """
        try:
            user_id = str(update.effective_user.id)
            self.chatbot_manager.clear_conversation(user_id)
            
            logger.info(f"Conversación limpiada para usuario {user_id}")
            
            await update.message.reply_text(
                "✅ Conversación reiniciada.\n\n"
                "Puedes empezar a hacer tus preguntas nuevamente. "
                "¿En qué puedo ayudarte?"
            )
            
        except Exception as e:
            logger.error(f"Error en comando /limpiar: {str(e)}")
            await update.message.reply_text(
                "Disculpa, hubo un error al limpiar la conversación. "
                "Por favor, intenta nuevamente."
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja mensajes de texto del usuario
        
        Args:
            update: Actualización de Telegram
            context: Contexto de la conversación
        """
        try:
            user = update.effective_user
            user_id = str(user.id)
            message = update.message.text
            
            logger.info(f"Mensaje de {user.first_name} ({user_id}): {message[:50]}...")
            
            # Indicar que el bot está escribiendo
            await update.message.chat.send_action("typing")
            
            # Obtener respuesta del chatbot
            response = self.chatbot_manager.get_response(user_id, message)
            
            # Enviar respuesta
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error al manejar mensaje: {str(e)}")
            await update.message.reply_text(
                "Disculpa, he tenido un problema al procesar tu mensaje. 😔\n\n"
                "Por favor, intenta reformular tu pregunta o usa el comando /limpiar "
                "para iniciar una nueva conversación.\n\n"
                "Si el problema persiste, puedes contactar directamente con nuestra clínica."
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja errores del bot
        
        Args:
            update: Actualización de Telegram
            context: Contexto con información del error
        """
        logger.error(f"Error del bot: {context.error}", exc_info=context.error)
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Ha ocurrido un error inesperado. 😔\n\n"
                "Por favor, intenta nuevamente más tarde o contacta directamente con la clínica."
            )
    
    def run(self) -> None:
        """
        Inicia el bot de Telegram
        
        Raises:
            Exception: Si hay un error al iniciar el bot
        """
        try:
            logger.info("Inicializando bot de Telegram...")
            
            # Inicializar chatbot
            self.chatbot_manager.initialize()
            
            # Crear aplicación
            self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            
            # Registrar manejadores de comandos
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("limpiar", self.clear_command))
            
            # Registrar manejador de mensajes
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
            )
            
            # Registrar manejador de errores
            self.application.add_error_handler(self.error_handler)
            
            # Iniciar bot
            logger.info("Bot de Telegram iniciado. Presiona Ctrl+C para detener.")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"Error al iniciar bot: {str(e)}")
            raise


def main():
    """Función principal para ejecutar el bot"""
    try:
        bot = TelegramBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {str(e)}")
        raise


if __name__ == "__main__":
    main()
