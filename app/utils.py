"""
Funciones utilitarias del proyecto.
"""
from pathlib import Path
from typing import List


def get_file_list(directory: str, extensions: List[str] = None) -> List[Path]:
    """
    Obtiene la lista de archivos en un directorio.
    
    Args:
        directory: Ruta al directorio.
        extensions: Lista de extensiones a filtrar (ej: ['.pdf', '.csv']).
    
    Returns:
        Lista de Paths de los archivos encontrados.
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    
    if extensions:
        files = []
        for ext in extensions:
            files.extend(dir_path.glob(f"*{ext}"))
        return sorted(files)
    
    return sorted(dir_path.iterdir())


def format_sources(sources: List[str]) -> str:
    """
    Formatea la lista de fuentes para mostrar al usuario.
    
    Args:
        sources: Lista de nombres de archivos fuente.
    
    Returns:
        String formateado con las fuentes.
    """
    if not sources:
        return ""
    
    formatted = "📎 **Fuentes consultadas:**\n"
    for source in sorted(sources):
        formatted += f"  - {source}\n"
    return formatted


def truncate_text(text: str, max_length: int = 500) -> str:
    """Trunca un texto a una longitud máxima, agregando '...' si es necesario."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."
