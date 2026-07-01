FROM python:3.13

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Actualizar pip
RUN pip install --upgrade pip

# Instalar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto de Django
EXPOSE 8000

# Servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]