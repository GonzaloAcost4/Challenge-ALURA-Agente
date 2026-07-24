"""
Módulo del Agente Inteligente.
Implementa el agente conversacional con memoria y RAG.
"""
import time

from langchain_groq import ChatGroq

try:
    from langchain.chains import ConversationalRetrievalChain
except (ImportError, ModuleNotFoundError):
    from langchain_classic.chains import ConversationalRetrievalChain

try:
    from langchain.memory import ConversationBufferWindowMemory
except (ImportError, ModuleNotFoundError):
    from langchain_classic.memory import ConversationBufferWindowMemory

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from app.config import GROQ_API_KEY, LLM_MODEL, SYSTEM_PROMPT
from app.rag import get_retriever, check_vector_store_exists


def get_llm() -> ChatGroq:
    """Inicializa y retorna el modelo LLM de Groq."""
    return ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.3,
    )


def get_memory() -> ConversationBufferWindowMemory:
    """
    Crea memoria conversacional con ventana deslizante.
    Mantiene los últimos k intercambios para contexto.
    """
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=10,
    )


def create_agent(memory: ConversationBufferWindowMemory = None):
    """
    Crea el agente conversacional con RAG.

    Args:
        memory: Memoria conversacional. Si es None, crea una nueva.

    Returns:
        Cadena conversacional configurada.
    """
    if not check_vector_store_exists():
        raise ValueError(
            "No se encontró una base de conocimiento indexada. "
            "Por favor, coloca documentos en data/knowledge_base/ y ejecuta la ingesta."
        )

    llm = get_llm()
    retriever = get_retriever()

    if memory is None:
        memory = get_memory()

    qa_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            SYSTEM_PROMPT + "\n\nContexto de la base de conocimiento:\n{context}"
        ),
        HumanMessagePromptTemplate.from_template("{question}"),
    ])

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        return_source_documents=True,
        verbose=False,
    )

    return chain


def ask_agent(chain, question: str, max_retries: int = 3) -> dict:
    """
    Realiza una pregunta al agente con reintentos automáticos
    para manejar errores transitorios de la API.

    Args:
        chain: Cadena conversacional.
        question: Pregunta del usuario.
        max_retries: Cantidad máxima de reintentos ante errores transitorios.

    Returns:
        Diccionario con 'answer' y 'source_documents'.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            result = chain.invoke({"question": question})

            sources = set()
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    source_file = doc.metadata.get("source_file", "Desconocido")
                    sources.add(source_file)

            return {
                "answer": result.get("answer", "No pude generar una respuesta."),
                "sources": list(sources),
                "source_documents": result.get("source_documents", []),
            }
        except Exception as e:
            error_str = str(e)
            retryable = (
                "RESOURCE_EXHAUSTED" in error_str
                or "429" in error_str
                or "500 INTERNAL" in error_str
                or "503" in error_str
                or "UNAVAILABLE" in error_str
            )
            if retryable:
                last_error = e
                wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s
                print(
                    f"Error transitorio (intento {attempt + 1}/{max_retries}). "
                    f"Reintentando en {wait_time}s..."
                )
                time.sleep(wait_time)
            else:
                raise

    raise last_error
