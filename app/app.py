import os
from flask import Flask, Response

app = Flask(__name__)

# Definimos o caminho de um arquivo dentro do contêiner para sinalizar a falha.
# gunicorn pode não se comportar com o esperado se usar variavel global no codigo.
CRASH_FILE = "/tmp/api_crashed.flag"

# GIFs Fixos
HAPPY_CAT = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTF0ZGh3ZXhicDRwYm5jbGNxcm1ydmprZDFkcThsaGdoOWdzY3FjZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/A0Zt7yuDULiy4ofmVD/giphy.gif"
SAD_CAT = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2JxMjN4bXNyeTQ0emdjYXI0ZXgxZTljYnlvODc4MnRqNzY1ZDIwdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dT7LBdAZP1Rh6/giphy.gif"

# CSS somente para melhorar a aparência da página.
CSS = """
<style>
    body { font-family: sans-serif; text-align: center; padding: 50px; transition: background 0.5s; }
    .container { max-width: 600px; margin: auto; padding: 20px; border-radius: 15px; background: white; border: 2px solid #ddd; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    img { max-width: 100%; border-radius: 10px; margin: 20px 0; }
    button { padding: 15px 25px; font-size: 18px; cursor: pointer; border: none; border-radius: 5px; background: #ff4d4d; color: white; font-weight: bold; }
    .status { font-weight: bold; padding: 5px 10px; border-radius: 5px; }
    .ok { color: #27ae60; background: #e8f5e9; }
    .fail { color: #c0392b; background: #f9ebea; }
</style>
"""

@app.route('/')
def hello():
    # Verifica se o arquivo de crash existe para mudar o visual da página e o status code.
    if os.path.exists(CRASH_FILE):
        return f"""
        <html>
            <head>{CSS}</head>
            <body style="background-color: #f9ebea;">
                <div class="container">
                    <h1 style="color: #c0392b;">⚠️ API Fora do Ar!</h1>
                    <img src="{SAD_CAT}" alt="Gatinho Triste">
                    <p>Status: <span class="status fail">FALHA CRÍTICA (500)</span></p>
                    <p>O Kubernetes detectou a falha e está reiniciando o pod...</p>
                </div>
                <script>setTimeout(function(){{ location.reload(); }}, 2000);</script>
            </body>
        </html>
        """, 500
    else:
        return f"""
        <html>
            <head>{CSS}</head>
            <body style="background-color: #e8f5e9;">
                <div class="container">
                    <h1 style="color: #27ae60;">✅ API Rodando Perfeitamente!</h1>
                    <img src="{HAPPY_CAT}" alt="Gatinho Feliz">
                    <p>Status: <span class="status ok">SAUDÁVEL (200)</span></p>
                    <p>Ambiente pronto para testes.</p>
                    <br>
                    <a href="/crash"><button>DERRUBAR API (CAOS)</button></a>
                </div>
            </body>
        </html>
        """, 200

# Endpoint de monitoramento para o Kubernetes
@app.route('/health')
def health_check():
    if os.path.exists(CRASH_FILE):
        return Response("FALHA CRITICA", status=500)
    else:
        return Response("OK", status=200)

# Rota para injeção de caos no health check.
@app.route('/crash')
def crash():
    with open(CRASH_FILE, 'w') as f:
        f.write("crashed")
    return """
    <script>
        window.location.href = '/';
    </script>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)