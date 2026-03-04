FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencias
COPY pyproject.toml uv.lock ./

# Instalar uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Instalar dependencias (lockfile)
RUN uv sync --system --frozen

# Copiar código
COPY . .

EXPOSE 8501

# Render usa PORT; local cae a 8501
CMD streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-8501}