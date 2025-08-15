#!/bin/sh
set -e

# Postgres
echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.5
done
echo "Postgres is up."

# Миграции и запуск
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
