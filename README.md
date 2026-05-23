# Cost Service

## Описание

FastAPI-сервис для FinOps-части платформы. Он хранит тарифы, цену электроэнергии и события стоимости инференса, после чего отдает сводки для frontend.

## Основные возможности

- сводка затрат за период
- история стоимости инференса и электроэнергии
- ручные тарифы моделей
- настройка цены электроэнергии
- запись cost usage events из inference gateway

## Основные API-ручки

- `/costs/summary`
- `/costs/history`
- `/costs/model-rates`
- `/costs/electricity-price`
- `/costs/usage-events`

## Структура проекта

- `app/` — код FastAPI-сервиса
- `app/main.py` — HTTP API и базовая service runtime логика
- `app/config.py` — настройки сервиса через переменные окружения
- `deploy/` — файлы для раскатки сервиса
- `Dockerfile` — сборка контейнера
- `pyproject.toml`, `uv.lock` — зависимости Python
- `.env.example` — пример конфигурации

## Быстрый старт локально

1. Установить зависимости:
   ```bash
   uv sync --frozen
   ```

2. Запустить сервис:
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Проверить, что сервис живой:
   ```bash
   curl http://localhost:8000/health
   ```

## Переменные окружения

- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — подключение к PostgreSQL
- `K8S_NAMESPACE` — namespace платформы в Kubernetes
- `SECURITY_AUDIT_BASE_URL` — адрес security/audit service
- `SECURITY_AUDIT_SERVICE_TOKEN` — service-to-service токен
- `STATUS_PROMETHEUS_BASE_URL` — адрес Prometheus для сервисов, которым нужны метрики
- `IMAGE_REPOSITORY`, `IMAGE_TAG`, `RELEASE_NAME`, `KUBECONFIG_PATH` — параметры deploy-скриптов

Полный пример лежит в `.env.example`.

## Docker

```bash
docker build -t awesomecosmonaut/cost_service:latest .
docker run --env-file .env -p 8000:8000 awesomecosmonaut/cost_service:latest
```

## Деплой

Файлы для раскатки лежат в `deploy/`.

```bash
cd deploy
./deploy-from-scratch.sh
```

Если нужно пересобрать образ и полностью переустановить сервис:

```bash
cd deploy
./rebuild-delete-deploy.sh
```

## Автор

Igor Malysh
