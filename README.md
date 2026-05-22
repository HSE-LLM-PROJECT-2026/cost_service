# Cost Service

## Описание

Сервис расчета стоимости inference, управления тарифами моделей и настройками стоимости электроэнергии.

## Основные возможности

- сводка и история затрат
- управление model rates
- запись usage cost events

## Структура проекта

- `app/` - код сервиса (FastAPI, config, domain handlers)
- `deploy/` - служебные файлы для роли сервиса в деплое
- `pyproject.toml` - зависимости и метаданные проекта
- `Dockerfile` - сборка контейнера
- `.env.example` - пример переменных окружения

## Быстрый старт (локально)

1. Установить зависимости:
   `uv sync --frozen --extra dev`
2. Запустить сервис:
   `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Проверить health:
   `curl http://127.0.0.1:8000/health`

## Переменные окружения

- `SERVICE_ROLE` - роль сервиса в control plane
- `SERVICE_NAME` - техническое имя сервиса
- `POSTGRES_DSN` - строка подключения к PostgreSQL
- `PROMETHEUS_BASE_URL` - адрес Prometheus
- `SERVICE_TO_SERVICE_URLS_JSON` - карта внутренних URL сервисов

## Docker

- Сборка: `docker build -t cost_service:local .`
- Запуск: `docker run --rm -p 8000:8000 --env-file .env cost_service:local`

## Деплой

Файлы для деплоя лежат в `deploy/`.

## Основные API ручки

- `GET /costs/summary`
- `GET /costs/history`
- `GET /costs/model-rates`
- `PUT /costs/model-rates/{model_name}`
- `GET /costs/electricity-price`
- `PUT /costs/electricity-price`
- `POST /costs/usage-events`
