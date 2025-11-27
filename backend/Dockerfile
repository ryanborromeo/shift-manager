FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with increased timeout
ENV UV_HTTP_TIMEOUT=120
RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
