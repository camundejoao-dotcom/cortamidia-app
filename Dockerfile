# Usa uma imagem oficial do Python leve
FROM python:3.10-slim

# Instala o FFmpeg no sistema do servidor
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Cria a pasta de trabalho no servidor
WORKDIR /app

# Copia os arquivos do seu projeto para o servidor
COPY . .

# Instala as bibliotecas de Python (Flask, yt-dlp, flask-cors)
RUN pip install --no-cache-dir flask flask-cors yt-dlp

# Expõe a porta que a API vai rodar
EXPOSE 5000

# Executa o seu backend
CMD ["python", "app.py"]
