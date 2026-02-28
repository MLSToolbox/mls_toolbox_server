FROM python:3.10-alpine

ARG ENVIRONMENT=local

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --no-cache-dir --timeout=120 --retries=5 -r requirements.txt

# Copiar app como fallback para builds standalone (sin docker compose).
# Cuando se usa docker compose, el bind mount ./app:/app lo sobreescribe.
COPY app /app

ENV EXECUTION_MODE="prod"
ENV ENVIRONMENT=${ENVIRONMENT}

ENTRYPOINT ["python3"]
CMD ["server.py"]
