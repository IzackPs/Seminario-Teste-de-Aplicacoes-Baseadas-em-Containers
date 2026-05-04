import os
from flask import Flask, Response

app = Flask(__name__)

# Definimos o caminho de um arquivo dentro do contêiner para sinalizar a falha.
# gunicorn pode não se comportar com o esperado se usar variavel global no codigo.
CRASH_FILE = "/tmp/api_crashed.flag"

@app.route('/')
def hello():
    return "API rodando perfeitamente! Preparada para o caos."

# O Kubernetes vai chamar essa rota a cada 5 segundos
@app.route('/health')
def health_check():
    # Verifica se o arquivo de falha existe dentro do contêiner
    if os.path.exists(CRASH_FILE):
        return Response("FALHA CRITICA", status=500)
    else:
        return Response("OK", status=200)

# Rota do Caos
@app.route('/crash')
def crash():
    # Cria o arquivo para "quebrar" a API para todas as threads do Gunicorn
    with open(CRASH_FILE, 'w') as f:
        f.write("crashed")
    return "Bug fatal acionado! A API vai parar de responder ao Health Check."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)