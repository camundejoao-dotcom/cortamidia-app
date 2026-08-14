import os
import subprocess
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite requisições vindas do WebView frontend

OUTPUT_FILE = "corte_output.mp4"

def update_ytdlp():
    """Garante que o yt-dlp esteja sempre atualizado na versão mais recente."""
    try:
        subprocess.run(["pip", "install", "--upgrade", "yt-dlp"], check=True)
    except Exception as e:
        print(f"Aviso ao atualizar yt-dlp: {e}")

@app.route("/cut", methods=["POST"])
def cut_media():
    # Atualiza o yt-dlp antes de processar qualquer requisição
    update_ytdlp()

    data = request.json
    url = data.get("url")
    start = data.get("start", "00:00:00")
    end = data.get("end", "00:00:10")

    if not url:
        return jsonify({"error": "URL não fornecida"}), 400

    # Remove arquivo residual antigo, se houver
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    # Comando otimizado com bypass de IP do YouTube (simulando cliente Android)
    cmd = [
        "yt-dlp",
        "--download-sections", f"*{start}-{end}",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--extractor-args", "youtube:player_client=android,web",
        "-o", OUTPUT_FILE,
        "--force-overwrites",
        url
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print("LOG DE ERRO DO YT-DLP:", result.stderr)
            return jsonify({"error": f"Erro no processamento: {result.stderr[-300:]}"}), 500

        return send_file(
            OUTPUT_FILE,
            mimetype="video/mp4",
            as_attachment=True,
            download_name="corte.mp4"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
