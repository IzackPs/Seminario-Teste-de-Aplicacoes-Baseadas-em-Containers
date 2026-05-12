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
# ESTÁGIO 2: RUNTIME
# ==============================================================================
FROM python:3.14.4-slim

RUN addgroup --system --gid 10001 apiappgroup && \
    adduser --system --uid 10001 --gid 10001 --no-create-home apiapp

WORKDIR /app
RUN chown 10001:10001 /app

# Mudamos para o UID seguro numérico (O Kubernetes prefere UIDs para validar runAsNonRoot)
USER 10001

# A MÁGICA: Copiamos apenas o ambiente virtual pronto
COPY --from=builder --chown=10001:10001 /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY --chown=10001:10001 app.py /app/

EXPOSE 8080
CMD ["gunicorn", "-w", "1", "--threads", "2", "-b", "0.0.0.0:8080", "app:app"]