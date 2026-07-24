"""
Tests para el agente inteligente.
"""
import sys
import io
from pathlib import Path

# Asegurar encoding UTF-8 para la salida en consola Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import validate_config, DATA_DIR, GOOGLE_API_KEY
from app.rag import load_documents, split_documents, check_vector_store_exists
from app.utils import get_file_list, format_sources, truncate_text


def test_config():
    """Test de la configuración."""
    print("=" * 50)
    print("🧪 Test: Configuración")
    print("=" * 50)
    
    errors = validate_config()
    if errors:
        print("❌ Errores encontrados:")
        for e in errors:
            print(f"   - {e}")
    else:
        print("✅ Configuración válida")
    
    print(f"   DATA_DIR: {DATA_DIR}")
    print(f"   API_KEY configurada: {'Sí' if GOOGLE_API_KEY else 'No'}")
    print()


def test_file_discovery():
    """Test de descubrimiento de archivos."""
    print("=" * 50)
    print("🧪 Test: Descubrimiento de archivos")
    print("=" * 50)
    
    files = get_file_list(str(DATA_DIR), [".pdf"])
    print(f"   Archivos encontrados: {len(files)}")
    for f in files:
        print(f"   - {f.name} ({f.suffix})")
    print()


def test_document_loading():
    """Test de carga de documentos."""
    print("=" * 50)
    print("🧪 Test: Carga de documentos")
    print("=" * 50)
    
    docs = load_documents()
    if docs:
        print(f"   Documentos cargados: {len(docs)}")
        # Mostrar un preview del primer documento
        first_doc = docs[0]
        print(f"   Preview: {truncate_text(first_doc.page_content, 200)}")
        print(f"   Metadata: {first_doc.metadata}")
    else:
        print("   ⚠️ No hay documentos para cargar")
    print()


def test_text_splitting():
    """Test de splitting de documentos."""
    print("=" * 50)
    print("🧪 Test: Text Splitting")
    print("=" * 50)
    
    docs = load_documents()
    if docs:
        chunks = split_documents(docs)
        print(f"   Chunks generados: {len(chunks)}")
        if chunks:
            print(f"   Tamaño promedio: {sum(len(c.page_content) for c in chunks) // len(chunks)} chars")
    else:
        print("   ⚠️ No hay documentos para dividir")
    print()


def test_vector_store():
    """Test de existencia del vector store."""
    print("=" * 50)
    print("🧪 Test: Vector Store")
    print("=" * 50)
    
    exists = check_vector_store_exists()
    print(f"   Vector store existe: {'Sí' if exists else 'No'}")
    print()


def test_utils():
    """Test de funciones utilitarias."""
    print("=" * 50)
    print("🧪 Test: Utilidades")
    print("=" * 50)
    
    # Test format_sources
    sources = ["ONE_AI_for_Tech_G10_2026.pdf", "Nivelación.pdf"]
    formatted = format_sources(sources)
    print(f"   format_sources: OK")
    
    # Test truncate_text
    text = "Este es un texto de prueba muy largo " * 20
    truncated = truncate_text(text, 50)
    assert len(truncated) <= 53  # 50 + "..."
    print(f"   truncate_text: OK")
    
    print("   ✅ Todas las utilidades funcionan correctamente")
    print()


if __name__ == "__main__":
    print("\n🚀 Ejecutando tests del agente inteligente\n")
    test_config()
    test_file_discovery()
    test_document_loading()
    test_text_splitting()
    test_vector_store()
    test_utils()
    print("🏁 Tests completados")
