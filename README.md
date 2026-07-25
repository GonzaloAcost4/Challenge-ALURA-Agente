# 🤖 Agente Inteligente - Challenge Alura | Oracle ONE

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-GPT_OSS_20B-f55?style=for-the-badge&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-Live-46E3B7?style=for-the-badge&logo=render&logoColor=white)

**Agente conversacional inteligente con RAG (Retrieval-Augmented Generation) que responde preguntas en lenguaje natural basándose en una base de conocimiento personalizada.**

🌐 **[Acceder a la Aplicación en Vivo](https://challenge-alura-agente-ggi9.onrender.com)**

[Arquitectura](#arquitectura) • [Instalación](#instalacion) • [Uso](#uso) • [Ejemplos](#ejemplos) • [Despliegue y Evidencias](#despliegue)

</div>

---

## 📖 Descripción

Este proyecto es un **agente inteligente** desarrollado como parte del **Challenge Alura** del programa **Oracle Next Education (ONE) - AI for Tech**. 

El agente utiliza la técnica **RAG (Retrieval-Augmented Generation)** para responder preguntas de forma precisa basándose en la documentación oficial en formato PDF del curso **ONE AI FOR TECH (G10 2026)** y cada una de sus formaciones especializadas.

### ✨ Características principales

- 🧠 **Agente conversacional** con memoria de contexto
- 📚 **Base de conocimiento** especializada en los PDFs de ONE AI FOR TECH
- 🔍 **Búsqueda semántica** con embeddings vectoriales locales (`FastEmbed`)
- 💬 **Interfaz de chat** intuitiva, limpia y moderna (Streamlit)
- 🐳 **Contenedorizado** con Docker para fácil despliegue
- ☁️ **Desplegado** en la nube en **Render** (Docker Web Service) con HTTPS

---

<a id="arquitectura"></a>

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                    │
│              Interfaz conversacional de chat               │
└─────────────────────┬────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────┐
│                  Agente Inteligente                        │
│             LangChain + Groq (openai/gpt-oss-20b) API     │
│         (Orquestación, Memoria, Razonamiento)             │
└─────────────────────┬────────────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────────────┐
│              RAG (Retrieval-Augmented Generation)          │
│                                                           │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐  │
│  │  Documentos  │───▶│  Embeddings  │───▶│ ChromaDB    │  │
│  │  PDF (ONE)   │    │ (FastEmbed)  │    │ VectorStore │  │
│  └─────────────┘    └──────────────┘    └─────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### Flujo del sistema

1. **Ingesta**: Los documentos PDF del curso se cargan, dividen en fragmentos y se generan embeddings vectoriales de forma local.
2. **Indexación**: Los embeddings se almacenan en ChromaDB para búsqueda semántica eficiente.
3. **Consulta**: Cuando el usuario hace una pregunta sobre alguna formación, se buscan los fragmentos más relevantes.
4. **Generación**: El LLM (`openai/gpt-oss-20b` vía Groq) genera una respuesta contextualizada usando los fragmentos recuperados.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
|---|---|---|
| **Lenguaje** | Python 3.11+ | Desarrollo general |
| **LLM** | Groq (openai/gpt-oss-20b) | Generación de respuestas ultrarrápida |
| **Embeddings** | FastEmbed (Local CPU) | Representación vectorial sin APIs externas |
| **Orquestación** | LangChain | Framework para agentes IA |
| **Vector Store** | ChromaDB | Almacenamiento y búsqueda vectorial |
| **Interfaz** | Streamlit | UI web conversacional |
| **Contenedorización** | Docker | Empaquetado y despliegue |
| **Cloud** | Render | Infraestructura y hosting en la nube |

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
│   └── knowledge_base/      # Documentos PDF de las formaciones
├── despliegue/              # Capturas y evidencias del deploy en Render
│   ├── Aplicacion_deployeada.jpg
│   ├── Challenge_Alura_Deploy.jpg
│   └── Deploy_Render.jpg
├── tests/
│   └── test_agent.py        # Tests unitarios del proyecto
├── .env.example             # Template de variables de entorno
├── .gitignore
├── Dockerfile               # Configuración Docker optimizada
├── docker-compose.yml       # Orquestación Docker local
├── render.yaml              # Configuración Blueprint para Render
├── requirements.txt         # Dependencias Python
├── planificacion.md         # Planificación detallada del proyecto
└── README.md                # Documentación principal
```

---

<a id="instalacion"></a>

## 🚀 Instalación

### Prerrequisitos

- **Python 3.11+**
- **API Key de Groq** (gratuita en [Groq Console](https://console.groq.com/keys))

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
# Editar .env y agregar tu GROQ_API_KEY
```

### Paso 5: Indexar documentos de ONE AI FOR TECH

Los archivos PDF de las formaciones ya se encuentran en `data/knowledge_base/`. Para procesarlos e indexarlos ejecuta:

```bash
python create_sample_data.py
```

### Paso 6: Ejecutar la aplicación

```bash
streamlit run app/main.py
```

La aplicación estará disponible en `http://localhost:8501`.

---

<a id="uso"></a>

## 📖 Uso

1. **Cargar documentos**: Verifica los archivos PDF en `data/knowledge_base/`.
2. **Indexar**: Haz clic en **"⟳ Indexar documentos"** en el panel lateral (o ejecuta `python create_sample_data.py`).
3. **Preguntar**: Escribe tu pregunta sobre el programa ONE AI FOR TECH o sus formaciones en el chat.
4. **Explorar**: El agente responderá basándose en los PDFs oficiales, citando las fuentes correspondientes.
5. **Guardar**: Haz clic en **"💾 Guardar conversación"** para descargar el historial completo en formato Markdown.

---

<a id="ejemplos"></a>

## 💡 Ejemplos de Preguntas y Respuestas

El agente es capaz de responder consultas complejas sobre el programa y sus contenidos apoyándose en la base de conocimiento:

### ❓ Ejemplo 1: Estructura del Programa
**Pregunta:** ¿Cuáles son las formaciones que componen el programa ONE AI FOR TECH?  
**Respuesta del Agente:**
> El programa **ONE AI FOR TECH (G10 2026)** está compuesto por 5 formaciones principales:
> 1. **Nivelación**: Fundamentos de programación y control de versiones.
> 2. **Desarrollo y Orquestación con IA Generativa**: Integración de LLMs en flujos de desarrollo.
> 3. **Inteligencia de Datos y RAG Avanzado**: Embeddings, bases de datos vectoriales y arquitecturas RAG.
> 4. **Ingeniería de Agentes y Automatización**: Creación de agentes autónomos y multi-agente.
> 5. **Oracle Cloud Infrastructure (OCI)**: Despliegue y escalabilidad en la nube.
>
> 📎 **Fuentes consultadas:** `ONE_AI_for_Tech_G10_2026.pdf`, `Nivelación.pdf`

### ❓ Ejemplo 2: Conceptos Técnicos de RAG
**Pregunta:** ¿Qué es un Vector Store y por qué se utiliza en RAG?  
**Respuesta del Agente:**
> Un **Vector Store** (como ChromaDB) es una base de datos optimizada para almacenar y recuperar representaciones vectoriales (embeddings) de texto. En una arquitectura RAG, permite realizar búsquedas semánticas eficientes para encontrar los fragmentos de documentos más relevantes a la pregunta del usuario antes de enviar el contexto al LLM.
>
> 📎 **Fuentes consultadas:** `Inteligencia de Datos y RAG Avanzado.pdf`

---

<a id="despliegue"></a>

## ☁️ Evidencia del Despliegue en la Nube (Render)

La aplicación está completamente desplegada y funcionando públicamente en **Render** como un Web Service de Docker.

- 🌐 **Enlace público:** [https://challenge-alura-agente-ggi9.onrender.com](https://challenge-alura-agente-ggi9.onrender.com)
- 💻 **Plataforma:** Render Cloud (Docker Web Service)
- 🔒 **Protocolo:** HTTPS habilitado

### 📸 Evidencias de Despliegue

#### 1. Panel de Render (Servicio Activo)
![Panel de Render](despliegue/Deploy_Render.jpg)

#### 2. Aplicación Ejecutándose en la Nube
![Aplicación Web en Render](despliegue/Aplicacion_deployeada.jpg)

#### 3. Agente Inteligente Respondiendo en Producción
![Agente Inteligente en Producción](despliegue/Challenge_Alura_Deploy.jpg)

---

## 🧪 Tests

```bash
python tests/test_agent.py
```

---

## 👨‍💻 Autor

- **Gonzalo Acosta**
- Challenge Alura - Oracle Next Education (ONE) - AI for Tech

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos como parte del programa Oracle Next Education.
