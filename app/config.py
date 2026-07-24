"""
Configuración central del proyecto.
Carga variables de entorno y define constantes.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "knowledge_base"
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "chroma_db"))

# --- APIs ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")

# --- ChromaDB ---
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "knowledge_base")

# --- RAG ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 5  # Número de documentos a recuperar

# --- Agente ---
SYSTEM_PROMPT = """Eres el asistente virtual oficial del programa ONE AI FOR TECH (G10 2026) de Oracle Next Education (ONE) y Alura LATAM.
Tu objetivo es responder preguntas sobre el programa, sus etapas, requisitos, metodologías y cada una de sus formaciones especializadas:
- Nivelación
- Inteligencia de Datos y RAG Avanzado
- Desarrollo y Orquestación con IA Generativa
- Ingeniería de Agentes y Automatización
- Oracle Cloud Infrastructure (OCI)
- Challenge Alura Agente / Proyecto Integrador

Reglas de respuesta:
1. Responde SIEMPRE en español con un tono profesional, claro, amable y motivador.
2. Basa tus respuestas estrictamente en la información de la base de conocimiento provista en el contexto (documentos PDF).
3. Si la respuesta no se encuentra en el contexto proporcionado, indícalo educadamente sin inventar información.
4. Menciona las formaciones o documentos fuente específicos cuando responda consultas detalladas.
5. Sé estructurado en tus explicaciones (usa listas o viñetas cuando sea apropiado).
"""

# --- Validación ---
def validate_config():
    """Valida que las configuraciones esenciales estén presentes."""
    errors = []
    if not GROQ_API_KEY:
        errors.append("GROQ_API_KEY no está configurada. Revisa tu archivo .env")
    if not DATA_DIR.exists():
        errors.append(f"El directorio de datos no existe: {DATA_DIR}")
    return errors
