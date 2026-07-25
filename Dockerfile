FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Puerto de Streamlit (Render asigna la variable $PORT dinámicamente)
ENV PORT=8501
EXPOSE 8501

# Ejecutar Streamlit adaptándose al puerto de Render o local
CMD ["sh", "-c", "streamlit run app/main.py --server.port=${PORT} --server.address=0.0.0.0 --server.headless=true"]
