# 1. Usamos un sistema operativo Linux muy ligero con Python 3.12 preinstalado
FROM python:3.12-slim

# 2. Instalamos la librería del sistema 'ffmpeg' (Obligatoria para que Whisper escuche MP3)
RUN apt-get update && apt-get install -y ffmpeg

# 3. Creamos la carpeta /app dentro del contenedor y nos movemos ahí
WORKDIR /app

# 4. Copiamos nuestro archivo de requerimientos e instalamos las librerías de IA y QA
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto de nuestro framework (código, audios, features)
COPY . .

# 6. El comando maestro que se ejecutará cuando el contenedor se encienda
CMD ["pytest", "tests/test_bdd_voz.py", "--alluredir=allure-results"]