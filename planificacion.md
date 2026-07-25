# 📋 Planificación - Challenge Alura Agente Inteligente

## 🎯 Objetivo del Proyecto
Diseñar y desarrollar un **agente inteligente** capaz de responder preguntas en lenguaje natural, 
utilizando una base de conocimiento construida a partir de documentos PDF/CSV, con despliegue en 
Render Cloud (Docker Web Service).

---

## 🏗️ Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                    │
│              Interfaz conversacional de chat               │
└─────────────────────┬────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────┐
│                  Agente Inteligente                        │
│             LangChain + Groq (openai/gpt-oss-20b) API                 │
│         (Orquestación, Memoria, Razonamiento)             │
└─────────────────────┬────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────┐
│              RAG (Retrieval-Augmented Generation)          │
│                                                           │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐  │
│  │  Documentos  │───▶│  Embeddings  │───▶│ ChromaDB    │  │
│  │  PDF / CSV   │    │ (FastEmbed)  │    │ VectorStore │  │
│  └─────────────┘    └──────────────┘    └─────────────┘  │
└──────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────┐
│                  Despliegue (Render Cloud)                 │
│              Docker Container Web Service                  │
└──────────────────────────────────────────────────────────┘
```

---

## 📦 Stack Tecnológico

| Componente       | Tecnología                          |
|------------------|-------------------------------------|
| Lenguaje         | Python 3.11+                        |
| LLM              | Groq (openai/gpt-oss-20b) (via API key)    |
| Embeddings       | FastEmbed (Local CPU)               |
| Orquestación     | LangChain                           |
| Vector Store     | ChromaDB (local/persistente)        |
| Interfaz (UI)    | Streamlit                            |
| Contenedorización| Docker                               |
| Despliegue       | Render Cloud (Web Service)         |
| Control versión  | Git + GitHub                         |

---

## 📁 Estructura del Proyecto

```
Challenge-ALURA-Agente/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada Streamlit
│   ├── agent.py              # Lógica del agente inteligente
│   ├── rag.py                # Pipeline RAG (ingesta + retrieval)
│   ├── config.py             # Configuración y constantes
│   └── utils.py              # Funciones utilitarias
├── data/
│   └── knowledge_base/       # Documentos PDF/CSV de la base de conocimiento
├── chroma_db/                 # Base de datos vectorial persistente (gitignored)
├── tests/
│   └── test_agent.py         # Tests del agente
├── .env.example               # Variables de entorno de ejemplo
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── planificacion.md
└── README.md
```

---

## 🗓️ Fases de Desarrollo

### Fase 1: Fundación del Proyecto ✅
- [x] Crear repositorio en GitHub
- [x] Definir planificación
- [x] Crear estructura de carpetas
- [x] Configurar entorno virtual y dependencias
- [x] Crear `.gitignore` y `.env.example`

### Fase 2: Base de Conocimiento y RAG ✅
- [x] Seleccionar/preparar documentos PDF y/o CSV para la base de conocimiento
- [x] Implementar carga de documentos (`rag.py`)
  - [x] Loader para PDF (PyPDFLoader)
  - [x] Loader para CSV (CSVLoader)
- [x] Implementar chunking (text splitting)
- [x] Generar embeddings locales con FastEmbed
- [x] Almacenar embeddings en ChromaDB
- [x] Implementar función de retrieval (búsqueda semántica)

### Fase 3: Agente Inteligente ✅
- [x] Configurar conexión con Groq API
- [x] Diseñar prompt del sistema (system prompt)
- [x] Implementar agente con LangChain
  - [x] Memoria conversacional
  - [x] Herramienta de búsqueda en base de conocimiento
  - [x] Cadena de razonamiento (ConversationalRetrievalChain)
- [ ] Probar respuestas con diferentes preguntas

### Fase 4: Interfaz de Usuario (Streamlit) ✅
- [x] Diseñar interfaz de chat conversacional
- [x] Implementar historial de mensajes
- [x] Agregar sidebar con información del proyecto
- [x] Agregar indicadores de carga/procesamiento
- [x] Estilizar la interfaz

### Fase 5: Contenedorización y Despliegue ✅
- [x] Crear Dockerfile
- [x] Crear docker-compose.yml
- [x] Crear render.yaml (Blueprint)
- [x] Probar localmente con Docker
- [x] Conectar repositorio a Render Web Service
- [x] Desplegar contenedor en Render
- [x] Verificar acceso público HTTPS

### Fase 6: Documentación y Entrega ✅ (parcial)
- [x] Elaborar README completo
  - [ ] Descripción del proyecto
  - [ ] Arquitectura del sistema
  - [ ] Instrucciones de instalación y uso
  - [ ] Capturas de pantalla / evidencias
  - [ ] Tecnologías utilizadas
- [ ] Revisar código y limpieza final
- [ ] Commit final y push a GitHub

---

## 🔑 Variables de Entorno Necesarias

```env
GROQ_API_KEY=tu_api_key_de_groq
CHROMA_PERSIST_DIR=./chroma_db_v2
COLLECTION_NAME=knowledge_base_v2
```

---

## 📝 Notas
- Se usa **Groq (openai/gpt-oss-20b)** como LLM por su velocidad sobresaliente y excelente rendimiento.
- Los embeddings se generan **localmente con FastEmbed**, lo que elimina llamadas externas y previene límites de API o cuota agotada.
- **ChromaDB** se elige como vector store por ser liviano, no requiere servidor externo, y persiste en disco.
- El despliegue se realiza en **Render** como un Web Service de Docker con certificado SSL gratuito.
