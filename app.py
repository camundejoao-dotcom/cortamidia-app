from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app) # Permite requisições vindas do APK

@app.route('/cut', methods=['POST'])
def cut_video():
    data = request.json
    video_url = data.get('url')
    start_time = data.get('start', '00:00:00')
    end_time = data.get('end')

    # Comando usando yt-dlp + ffmpeg para baixar apenas o trecho selecionado
    output_filename = "corte_output.mp4"
    
    # Exemplo de comando otimizado com download direto do trecho
    cmd = [
        "yt-dlp",
        "--download-sections", f"*{start_time}-{end_time}",
        "-f", "mp4",
        "-o", output_filename,
        video_url,
        "--force-overwrites"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        # Aqui você pode retornar o link direto para download do arquivo gerado
        return jsonify({"download_url": f"{request.host_url}download/{output_filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
