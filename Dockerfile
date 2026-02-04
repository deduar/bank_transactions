FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --chown=appuser:appuser requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY --chown=appuser:appuser src /app/src
COPY --chown=appuser:appuser config /app/config

ENV PYTHONPATH=/app/src

USER appuser
