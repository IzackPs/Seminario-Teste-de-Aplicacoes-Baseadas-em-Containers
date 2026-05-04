# ==============================================================================
# ESTÁGIO 1: BUILDER (Preparação e instalação de dependências)
# ==============================================================================
FROM python:3.14.4-slim AS builder

WORKDIR /app

# Cria o ambiente virtual
ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV

# Colocamos o ambiente virtual no PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# BOAS PRÁTICAS: Copiamos APENAS o requirements primeiro para usar o cache do Docker!
COPY requirements.txt .

# Instalamos as dependências de forma limpa
RUN pip install --no-cache-dir -r requirements.txt


# ==============================================================================
# ESTÁGIO 2: RUNTIME (A imagem final, limpa, leve e segura)
# ==============================================================================
FROM python:3.14.4-slim

# Segurança DevSecOps: Usuário sem privilégios
RUN adduser --disabled-password --gecos '' apiapp

WORKDIR /app
RUN chown apiapp:apiapp /app

# Mudamos para o usuário seguro
USER apiapp

# A MÁGICA: Copiamos apenas o ambiente virtual pronto do estágio builder
COPY --from=builder --chown=apiapp:apiapp /app/venv /app/venv

# Garantimos que o sistema use o nosso venv
ENV PATH="/app/venv/bin:$PATH"

# Agora copiamos APENAS o código da aplicação
COPY --chown=apiapp:apiapp app.py /app/

EXPOSE 8080

# Servidor de Produção (Gunicorn)
CMD ["gunicorn", "-w", "1", "--threads", "2", "-b", "0.0.0.0:8080", "app:app"]