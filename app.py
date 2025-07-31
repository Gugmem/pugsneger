from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='static')
CORS(app)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1400164401402875955/T6XucHLxbq3SdQcSWZQ7yl3ESCuUFI_sOyOfrPqPihVO7JAE5TowjUf340vY38RK5AAS"

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/post', methods=['POST'])
def post_to_discord():
    data = request.json
    embeds = data.get("embeds", [])
    if not embeds:
        return jsonify({"status": "error", "details": "Нет embed-блоков"}), 400

    response = requests.post(DISCORD_WEBHOOK_URL, json={"embeds": embeds})
    if response.status_code == 204:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "details": response.text}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)