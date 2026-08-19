FROM python:3.11-slim

WORKDIR /app

# Install serving-only dependencies first for better layer caching
COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt

# Bring in the app code and the bundled model artifacts
COPY src/ ./src/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "src.app.main:app"]
