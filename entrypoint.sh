#!/bin/sh
set -e

# Папка для SQLite файла (в контейнере)
mkdir -p /app/data

# Автоматическая миграция структуры при старте
alembic upgrade head

# Запуск API
uvicorn app.main:app --host 0.0.0.0 --port 8000
