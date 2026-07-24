# 🤖 Agente Inteligente - Challenge Alura | Oracle ONE

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![OCI](https://img.shields.io/badge/Oracle_Cloud-Deployed-F80000?style=for-the-badge&logo=oracle&logoColor=white)

**Agente conversacional inteligente con RAG (Retrieval-Augmented Generation) que responde preguntas en lenguaje natural basándose en una base de conocimiento personalizada.**

[Demostración](#-demostración) • [Instalación](#-instalación) • [Uso](#-uso) • [Arquitectura](#-arquitectura) • [Despliegue](#-despliegue-en-oci)

</div>

---

## 📖 Descripción

Este proyecto es un **agente inteligente** desarrollado como parte del **Challenge Alura** del programa **Oracle Next Education (ONE) - AI for Tech**. 

El agente utiliza la técnica **RAG (Retrieval-Augmented Generation)** para responder preguntas de forma precisa basándose en la documentación oficial en formato PDF del curso **ONE AI FOR TECH (G10 2026)** y cada una de sus formaciones especializadas.

### ✨ Características principales

- 🧠 **Agente conversacional** con memoria de contexto
- 📚 **Base de conocimiento** especializada en los PDFs de ONE AI FOR TECH
- 🔍 **Búsqueda semántica** con embeddings vectoriales
- 💬 **Interfaz de chat** intuitiva y moderna
- 🐳 **Contenedorizado** con Docker para fácil despliegue
- ☁️ **Desplegado** en Oracle Cloud Infrastructure (OCI)

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                    │
│              Interfaz conversacional de chat               │
└─────────────────────┬────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────┐
│                  Agente Inteligente                        │
│            LangChain + Google Gemini API                   │
│         (Orquestación, Memoria, Razonamiento)             │
└─────────────────────┬────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────┐
│              RAG (Retrieval-Augmented Generation)          │
│                                                           │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐  │
│  │  Documentos  │───▶│  Embeddings  │───▶│ ChromaDB    │  │
│  │  PDF (ONE)   │    │  (Gemini)    │    │ VectorStore │  │
│  └─────────────┘    └──────────────┘    └─────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Flujo del sistema

1. **Ingesta**: Los documentos PDF del curso se cargan, dividen en fragmentos y se generan embeddings vectoriales.
2. **Indexación**: Los embeddings se almacenan en ChromaDB para búsqueda semántica eficiente.
3. **Consulta**: Cuando el usuario hace una pregunta sobre alguna formación, se buscan los fragmentos más relevantes.
4. **Generación**: El LLM (Gemini) genera una respuesta contextualizada usando los fragmentos recuperados.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
|---|---|---|
| **Lenguaje** | Python 3.11+ | Desarrollo general |
| **LLM** | Google Gemini 2.0 Flash | Generación de respuestas |
| **Embeddings** | Google Gemini Embedding | Representación vectorial |
| **Orquestación** | LangChain | Framework para agentes IA |
| **Vector Store** | ChromaDB | Almacenamiento y búsqueda vectorial |
| **Interfaz** | Streamlit | UI web conversacional |
| **Contenedorización** | Docker | Empaquetado y despliegue |
| **Cloud** | Oracle Cloud (OCI) | Infraestructura en la nube |

---

## 📁 Estructura del Proyecto

```
Challenge-ALURA-Agente/
├── app/
│   ├── __init__.py          # Inicializador del paquete
│   ├── main.py              # Interfaz Streamlit (punto de entrada)
│   ├── agent.py             # Lógica del agente inteligente
│   ├── rag.py               # Pipeline RAG (ingesta + retrieval)
│   ├── config.py            # Configuración y constantes
│   └── utils.py             # Funciones utilitarias
├── data/
│   └── knowledge_base/      # Documentos PDF/CSV
├── tests/
│   └── test_agent.py        # Tests del proyecto
├── .env.example             # Template de variables de entorno
├── .gitignore
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Orquestación Docker
├── requirements.txt         # Dependencias Python
├── planificacion.md         # Planificación del proyecto
└── README.md                # Este archivo
```

---

## 🚀 Instalación

### Prerrequisitos

- **Python 3.11+**
- **API Key de Google Gemini** (gratuita en [Google AI Studio](https://aistudio.google.com/apikey))

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/GonzaloAcost4/Challenge-ALURA-Agente.git
cd Challenge-ALURA-Agente
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env y agregar tu GOOGLE_API_KEY
```

### Paso 5: Indexar documentos de ONE AI FOR TECH

Los archivos PDF de las formaciones ya se encuentran en `data/knowledge_base/`. Para procesarlos e indexarlos ejecute:

```bash
python create_sample_data.py
```

### Paso 6: Ejecutar la aplicación

```bash
streamlit run app/main.py
```

La aplicación estará disponible en `http://localhost:8501`.

---

## 📖 Uso

1. **Cargar documentos**: Verifica los archivos PDF en `data/knowledge_base/`
2. **Indexar**: Haz clic en "🔄 Indexar Documentos" en el panel lateral (o ejecuta `python create_sample_data.py`)
3. **Preguntar**: Escribe tu pregunta sobre el programa ONE AI FOR TECH o sus formaciones en el chat
4. **Explorar**: El agente responderá basándose en los PDFs oficiales, citando las fuentes correspondientes

---

## 🐳 Despliegue con Docker

### Local

```bash
# Construir y ejecutar
docker compose up --build

# La app estará en http://localhost:8501
```

### En OCI (Oracle Cloud Infrastructure)

1. **Crear instancia de cómputo** (Always Free Tier - ARM Ampere A1)
2. **Instalar Docker** en la instancia
3. **Clonar el repositorio** y configurar `.env`
4. **Ejecutar** con Docker Compose
5. **Configurar Security List** para abrir el puerto 8501

```bash
# En la instancia OCI
git clone https://github.com/GonzaloAcost4/Challenge-ALURA-Agente.git
cd Challenge-ALURA-Agente
cp .env.example .env
# Editar .env con tu API key
docker compose up -d --build
```

---

## 🧪 Tests

```bash
python tests/test_agent.py
```

---

## 📸 Demostración

> _Capturas de pantalla y evidencias se agregarán aquí._

---

## 👨‍💻 Autor

- **Gonzalo Acosta**
- Challenge Alura - Oracle Next Education (ONE) - AI for Tech

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos como parte del programa Oracle Next Education.
