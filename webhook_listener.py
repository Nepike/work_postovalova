import hmac
import hashlib
import yaml
from flask import Flask, request, abort
import subprocess
import os

# Загружаем конфиг
config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
with open(config_path) as f:
    config = yaml.safe_load(f)

WEBHOOK_SECRET = config.get('deploy_secret', '')

app = Flask(__name__)

def verify_signature(payload, signature):
    if not WEBHOOK_SECRET:
        return False
    mac = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256)
    return hmac.compare_digest(f"sha256={mac.hexdigest()}", signature)

@app.route("/deploy_webhook", methods=["POST"])
def deploy():
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        abort(403)

    subprocess.Popen([
        "/bin/bash", os.path.join(os.path.dirname(__file__), 'deploy.sh')
    ])
    return "Deploy started", 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
