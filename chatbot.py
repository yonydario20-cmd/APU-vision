"""
Chatbot con LangChain y OpenAI para IPS Visión Cárdenas
"""
import logging
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    SYSTEM_PROMPT,
    MAX_MEMORY_MESSAGES
)
from vector_store import VectorStoreManager

logger = logging.getLogger(__name__)


class ChatbotManager:
    """Gestiona el chatbot con LangChain y OpenAI"""
    
    def __init__(self):
        """Inicializa el gestor del chatbot"""
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
            openai_api_key=OPENAI_API_KEY
        )
        self.vector_store_manager = VectorStoreManager()
        self.conversations: Dict[str, Any] = {}
        
    def initialize(self) -> None:
        """
        Inicializa el chatbot y sus componentes
        
        Raises:
            Exception: Si hay un error al inicializar
        """
        try:
            logger.info("Inicializando chatbot...")
            self.vector_store_manager.initialize_vector_store()
            logger.info("Chatbot inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar chatbot: {str(e)}")
            raise
    
    def _get_or_create_conversation(self, user_id: str) -> ConversationalRetrievalChain:
        """
        Obtiene o crea una cadena de conversación para un usuario
        
        Args:
            user_id: ID único del usuario
            
        Returns:
            Cadena de conversación configurada
        """
        if user_id not in self.conversations:
            logger.info(f"Creando nueva conversación para usuario {user_id}")
            
            # Crear memoria conversacional
            memory = ConversationBufferWindowMemory(
                k=MAX_MEMORY_MESSAGES,
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
            # Template personalizado para el prompt
            qa_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template=f"""{SYSTEM_PROMPT}

Contexto de la base de conocimiento:
{{context}}

Pregunta del paciente: {{question}}

Respuesta (amable y profesional):"""
            )
            
            # Crear cadena de conversación con retrieval
            conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store_manager.get_retriever(k=3),
                memory=memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": qa_prompt},
                verbose=False
            )
            
            self.conversations[user_id] = conversation_chain
        
        return self.conversations[user_id]
    
    def get_response(self, user_id: str, message: str) -> str:
        """
        Procesa un mensaje del usuario y genera una respuesta
        
        Args:
            user_id: ID único del usuario
            message: Mensaje del usuario
            
        Returns:
            Respuesta del chatbot
        """
        try:
            # Validar entrada
            if not message or not message.strip():
                return "Por favor, escriba su pregunta o consulta."
            
            logger.info(f"Procesando mensaje de usuario {user_id}: {message[:50]}...")
            
            # Obtener cadena de conversación
            conversation = self._get_or_create_conversation(user_id)
            
            # Generar respuesta
            result = conversation({"question": message})
            answer = result["answer"]
            
            logger.info(f"Respuesta generada para usuario {user_id}")
            return answer.strip()
            
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {str(e)}")
            return self._get_error_message()
    
    def clear_conversation(self, user_id: str) -> None:
        """
        Limpia la memoria conversacional de un usuario
        
        Args:
            user_id: ID único del usuario
        """
        if user_id in self.conversations:
            logger.info(f"Limpiando conversación para usuario {user_id}")
            del self.conversations[user_id]
    
    def _get_error_message(self) -> str:
        """
        Retorna un mensaje de error amigable
        
        Returns:
            Mensaje de error para el usuario
        """
        return (
            "Disculpe, he tenido un problema al procesar su mensaje. "
            "Por favor, intente nuevamente o reformule su pregunta. "
            "Si el problema persiste, puede contactar directamente con nuestra clínica. "
            "¿En qué más puedo ayudarle?"
        )
    
    def get_active_conversations_count(self) -> int:
        """
        Obtiene el número de conversaciones activas
        
        Returns:
            Número de conversaciones activas
        """
        return len(self.conversations)
