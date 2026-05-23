# Cost Service

## Описание

Этот репозиторий содержит FinOps-сервис платформы. Он хранит тарифы, цену электроэнергии и события стоимости инференса, а frontend получает из него сводки и детализацию затрат.

## Основные возможности
- сводка затрат за период
- история стоимости инференса и электроэнергии
- ручные тарифы моделей
- настройка цены электроэнергии
- запись cost usage events из inference gateway
- служебные health/livez/service-info ручки

## Структура проекта

- `app/` — основной код приложения
  - `main.py` — FastAPI-приложение и HTTP-ручки
  - `config.py` — настройки сервиса

- `deploy/` — файлы и переменные для развертывания
- `.env.example` — пример переменных окружения
- `Dockerfile` — сборка Docker-образа
- `pyproject.toml` — зависимости и настройки Python-проекта
- `requirements.txt` — список зависимостей для совместимого запуска без uv

## Быстрый старт локально

1. Установите зависимости:
   ```bash
   uv sync
   ```

2. Создайте `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Запустите сервис:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

Если `uv` не используется, можно запустить через обычный virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Переменные окружения
- `DATABASE_URL`
- `PROMETHEUS_URL`
- `SECURITY_SERVICE_URL`
- `SERVICE_TOKEN`
- `DEFAULT_ELECTRICITY_PRICE_RUB`
- `LOG_LEVEL`

Пример `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/llm_platform
SERVICE_TOKEN=change-me
LOG_LEVEL=INFO
```

## Основные API-ручки
- `GET /health`
- `GET /livez`
- `GET /service-info`
- `GET /cost/summary`
- `GET /cost/history`
- `GET /cost/rates`
- `PUT /cost/rates/{model_name}`
- `GET /cost/settings`
- `PUT /cost/settings`
- `POST /cost/events`

## Сборка и запуск в Docker

```bash
docker build -t hse-llm-project-2026/cost_service:local .
docker run --env-file .env -p 8000:8000 hse-llm-project-2026/cost_service:local
```

## Деплой в Kubernetes

Файлы развертывания лежат в папке `deploy/`. Для сервисов, которые уже подключены к стенду, используются Helm values и deploy-скрипты из соответствующего репозитория или общего инфраструктурного пайплайна.

## Метрики и документация

- Swagger UI: `/docs`
- OpenAPI: `/openapi.json`
- Health check: `/health`
- Liveness check: `/livez`

## Автор

Igor Malysh
