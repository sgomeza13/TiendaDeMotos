# Utiliza una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt a /app/
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Copia todo el contenido de tu proyecto al directorio de trabajo
COPY . /app/

# Configura las variables de entorno
ENV DJANGO_SETTINGS_MODULE=TiendaDeMotos.settings
ENV DEBUG=True

# Abre el puerto en el contenedor que escuchará tu aplicación
EXPOSE 8000

# Ejecuta el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
