import os
from flask import Flask, Response

app = Flask(__name__)
CRASH_FILE = "/tmp/api_crashed.flag"

@app.route('/')
def hello():
    if os.path.exists(CRASH_FILE):
        return "FALHA CRÍTICA (500)", 500
    else:
        return "SAUDÁVEL (200)", 200

@app.route('/health')
def health_check():
    if os.path.exists(CRASH_FILE):
        return Response("FALHA CRITICA", status=500)
    else:
        return Response("OK", status=200)

@app.route('/crash')
def crash():
    # Cria o arquivo para sinalizar a falha
    with open(CRASH_FILE, 'w') as f:
        f.write("crashed")
    return "Bug fatal acionado!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)