# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
ENV PORT=8000

# Keep it light: 1 worker + threads
CMD gunicorn -w 1 -k gthread --threads 8 -b 0.0.0.0:$PORT yahtzee:app

