FROM python:3.12-slim

LABEL Name="Hello_Again" Version="1.0"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libpq-dev postgresql-client curl \
    && pip install --no-cache-dir --upgrade pip gunicorn pipenv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy

COPY . /app/

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/api || exit 1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
