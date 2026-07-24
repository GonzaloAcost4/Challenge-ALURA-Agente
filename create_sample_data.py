"""
Script para ejecutar la ingesta de documentos en la base de conocimiento.
Procesa los archivos PDF del programa ONE AI FOR TECH ubicados en data/knowledge_base/.
"""
import sys
import io
from pathlib import Path

# Asegurar encoding UTF-8 en consola de Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.config import DATA_DIR
from app.rag import ingest_documents, check_vector_store_exists


def run_ingestion():
    """Ejecuta la ingesta de los PDFs de la base de conocimiento."""
    print(f"📚 Buscando documentos PDF en: {DATA_DIR}")
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("⚠️ No se encontraron archivos PDF en data/knowledge_base/")
        return
    
    print(f"📄 Se encontraron {len(pdf_files)} archivo(s) PDF:")
    for pdf in pdf_files:
        print(f"   - {pdf.name}")
    
    print("\n🔄 Iniciando proceso de indexación...")
    vector_store = ingest_documents()
    
    if vector_store:
        print("\n✅ Ingesta completada con éxito. Base de conocimiento lista para el Agente.")
    else:
        print("\n❌ Error durante la ingesta de documentos.")


if __name__ == "__main__":
    run_ingestion()
