# Usamos una imagen base de Python optimizada y ligera
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y habilita logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar algunas librerías
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalar las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto predeterminado de Streamlit
EXPOSE 8501

# Chequeo de salud para que la nube sepa si la app sigue viva
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para iniciar la aplicación optimizada
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
