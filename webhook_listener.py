from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/deploy_webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Здесь можно проверить секрет (если настроен на GitHub)
        # Для простоты запускаем deploy.sh без проверки
        subprocess.Popen([
            "/bin/bash", os.path.join(os.path.dirname(__file__), 'deploy.sh')
        ])
        return 'Deploy started', 200
    else:
        return 'Method not allowed', 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)