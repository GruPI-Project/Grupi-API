# Usar Python 3.12 como base
FROM python:3.12-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_ENV=prod \
    UV_SYSTEM_PYTHON=1

# Criar diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema e uv
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv $HOME/.local/bin/uv /usr/local/bin/

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências usando uv (muito mais rápido que pip)
RUN uv sync --frozen --no-dev

# Instalar Gunicorn separadamente
RUN uv add gunicorn

# Copiar o projeto
COPY . .

# Coletar arquivos estáticos (WhiteNoise vai comprimir e adicionar hash)
RUN uv run manage.py collectstatic --noinput

# Criar diretório para o banco de dados SQLite (se usado)
RUN mkdir -p /app/data

# Expor a porta 8000
EXPOSE 8000

# Script de entrada
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
