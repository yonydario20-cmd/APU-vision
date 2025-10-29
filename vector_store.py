"""
Gestor de la base de datos vectorial Chroma para IPS Visión Cárdenas
"""
import logging
from typing import List, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from config import (
    CHROMA_PERSIST_DIRECTORY,
    COLLECTION_NAME,
    OPENAI_API_KEY
)
from knowledge_base import CLINIC_KNOWLEDGE

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Gestiona el almacenamiento y recuperación de información en Chroma"""
    
    def __init__(self):
        """Inicializa el gestor de vector store"""
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_store: Optional[Chroma] = None
        
    def initialize_vector_store(self) -> None:
        """
        Inicializa o carga el vector store de Chroma
        
        Raises:
            Exception: Si hay un error al inicializar el vector store
        """
        try:
            logger.info("Inicializando vector store...")
            
            # Intentar cargar vector store existente
            try:
                self.vector_store = Chroma(
                    persist_directory=CHROMA_PERSIST_DIRECTORY,
                    embedding_function=self.embeddings,
                    collection_name=COLLECTION_NAME
                )
                
                # Verificar si tiene documentos
                collection = self.vector_store._collection
                if collection.count() > 0:
                    logger.info(f"Vector store cargado con {collection.count()} documentos")
                    return
                else:
                    logger.info("Vector store vacío, creando nueva base de conocimiento...")
                    
            except Exception as e:
                logger.info(f"Creando nuevo vector store: {str(e)}")
            
            # Crear y popular nuevo vector store
            self._populate_vector_store()
            logger.info("Vector store inicializado correctamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar vector store: {str(e)}")
            raise
    
    def _populate_vector_store(self) -> None:
        """
        Puebla el vector store con la base de conocimiento de la clínica
        
        Raises:
            Exception: Si hay un error al popular el vector store
        """
        try:
            # Convertir conocimiento a documentos
            documents = []
            for item in CLINIC_KNOWLEDGE:
                doc = Document(
                    page_content=item["content"],
                    metadata={"category": item["category"]}
                )
                documents.append(doc)
            
            # Dividir documentos en chunks más pequeños para mejor recuperación
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            split_docs = text_splitter.split_documents(documents)
            
            logger.info(f"Creando vector store con {len(split_docs)} chunks de documentos...")
            
            # Crear vector store
            self.vector_store = Chroma.from_documents(
                documents=split_docs,
                embedding=self.embeddings,
                persist_directory=CHROMA_PERSIST_DIRECTORY,
                collection_name=COLLECTION_NAME
            )
            
            # Persistir datos
            self.vector_store.persist()
            logger.info("Base de conocimiento guardada en disco")
            
        except Exception as e:
            logger.error(f"Error al popular vector store: {str(e)}")
            raise
    
    def search_relevant_info(self, query: str, k: int = 3) -> List[Document]:
        """
        Busca información relevante en el vector store
        
        Args:
            query: Consulta del usuario
            k: Número de documentos relevantes a recuperar
            
        Returns:
            Lista de documentos relevantes
            
        Raises:
            ValueError: Si el vector store no está inicializado
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado. Llame a initialize_vector_store() primero.")
        
        try:
            # Buscar documentos similares
            docs = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Encontrados {len(docs)} documentos relevantes para: '{query[:50]}...'")
            return docs
            
        except Exception as e:
            logger.error(f"Error al buscar información: {str(e)}")
            return []
    
    def get_retriever(self, k: int = 3):
        """
        Obtiene un retriever de LangChain para el vector store
        
        Args:
            k: Número de documentos a recuperar
            
        Returns:
            Retriever de LangChain
            
        Raises:
            ValueError: Si el vector store no está inicializado
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado. Llame a initialize_vector_store() primero.")
        
        return self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )
