FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar archivos de dependencias primero (para cache)
COPY pyproject.toml uv.lock ./

# Instalar uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Instalar dependencias usando el lockfile (crea .venv)
RUN uv sync --frozen

# Copiar el resto del código
COPY . .

# Usar el entorno virtual creado por uv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8501

# Render suele definir PORT; si no existe, usa 8501
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]