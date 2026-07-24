"""
Módulo RAG (Retrieval-Augmented Generation).
Maneja la ingesta de documentos, generación de embeddings y búsqueda semántica.
"""
import shutil
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import (
    CHROMA_PERSIST_DIR,
    COLLECTION_NAME,
    DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RETRIEVER_K,
)


def get_embeddings() -> FastEmbedEmbeddings:
    """Inicializa y retorna el modelo de embeddings local (FastEmbed)."""
    return FastEmbedEmbeddings()


def load_documents(data_dir: str = None) -> List[Document]:
    """
    Carga todos los documentos PDF del directorio de datos del programa ONE AI FOR TECH.

    Args:
        data_dir: Ruta al directorio de datos. Si es None, usa DATA_DIR.

    Returns:
        Lista de documentos cargados.
    """
    if data_dir is None:
        data_dir = str(DATA_DIR)

    documents = []
    data_path = Path(data_dir)

    if not data_path.exists():
        print(f"El directorio {data_path} no existe. Creandolo...")
        data_path.mkdir(parents=True, exist_ok=True)
        return documents

    # Cargar PDFs
    pdf_files = sorted(list(data_path.glob("*.pdf")))
    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_file"] = pdf_file.name
                doc.metadata["file_type"] = "PDF"
            documents.extend(docs)
            print(f"Cargado PDF: {pdf_file.name} ({len(docs)} paginas)")
        except Exception as e:
            print(f"Error cargando {pdf_file.name}: {e}")

    print(f"Total de paginas de documentos PDF cargadas: {len(documents)}")
    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Divide los documentos en chunks más pequeños para mejor retrieval.

    Args:
        documents: Lista de documentos a dividir.

    Returns:
        Lista de chunks (fragmentos de documentos).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Documentos divididos en {len(chunks)} chunks")
    return chunks


def create_vector_store(chunks: List[Document] = None) -> Chroma:
    """
    Crea o carga el vector store de ChromaDB.

    Si se pasan chunks, crea un nuevo vector store.
    Si no, intenta cargar uno existente.

    Args:
        chunks: Lista de chunks para indexar. Si es None, carga el existente.

    Returns:
        Instancia de ChromaDB.
    """
    embeddings = get_embeddings()

    if chunks is not None:
        # Si el directorio existia con embeddings de otra dimension, borrarlo
        persist_path = Path(CHROMA_PERSIST_DIR)
        if persist_path.exists():
            try:
                shutil.rmtree(CHROMA_PERSIST_DIR)
            except Exception:
                pass

        print("Creando vector store con nuevos documentos...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_PERSIST_DIR,
        )
        print(f"Vector store creado con {len(chunks)} chunks")
    else:
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIR,
        )
        count = vector_store._collection.count()
        print(f"Vector store cargado ({count} documentos indexados)")

    return vector_store


def get_retriever(vector_store: Chroma = None):
    """
    Obtiene el retriever para búsqueda semántica.

    Args:
        vector_store: Instancia de ChromaDB. Si es None, carga el existente.

    Returns:
        Retriever configurado.
    """
    if vector_store is None:
        vector_store = create_vector_store()

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVER_K},
    )


def ingest_documents():
    """
    Pipeline completo de ingesta: carga, divide e indexa documentos.

    Returns:
        Instancia de ChromaDB con los documentos indexados.
    """
    print("=" * 60)
    print("Iniciando ingesta de documentos")
    print("=" * 60)

    # 1. Cargar documentos
    documents = load_documents()
    if not documents:
        print("No se encontraron documentos para indexar.")
        print(f"   Coloca archivos PDF en: {DATA_DIR}")
        return None

    # 2. Dividir en chunks
    chunks = split_documents(documents)

    # 3. Crear vector store
    vector_store = create_vector_store(chunks)

    print("=" * 60)
    print("Ingesta completada exitosamente")
    print("=" * 60)

    return vector_store


def check_vector_store_exists() -> bool:
    """Verifica si ya existe un vector store persistido."""
    chroma_path = Path(CHROMA_PERSIST_DIR)
    return chroma_path.exists() and any(chroma_path.iterdir())


if __name__ == "__main__":
    ingest_documents()
