# Архитектура сервиса

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Общая схема

```
Frontend (форма/dashboard)
        │
        ▼
API Gateway (auth, i18n, rate limit)
        │
        ├──▶ Axis Services (13 независимых модулей)
        ├──▶ Report Cache (Redis, TTL)
        └──▶ Data Ingestion (cron/manual импорт)
```

**Ключевой принцип:** каждая ось — отдельный сервис/модуль с собственной таблицей и циклом обновления, не общая денормализованная таблица «городов». Прямое продолжение Non-Coupling Principle: сбой одного модуля не должен ронять остальные.

## Схема БД

По одной таблице на тип данных, не на «город» — так сохраняется типизация полей и честные `NULL`/`not_applicable` вместо JSON-помойки. Полный DDL — `backend/app/db/schema.sql`.

Ключевые решения:
- Каждая ось хранит `data_snapshot_date` и `source` — обязательные поля для `citations` на фронте.
- Гранулярность разная по осям: `axis_weather_risk` — по дням (нужна точность дат), `axis_infrastructure_load` — по месяцам.
- Визовые данные (`visa_requirements`) — общий справочник по парам "гражданство → страна", не пересчитывается на каждый запрос.
- B2B-данные (`operator_incident_log`) — привязаны к `operator_id`, не к направлению глобально.

## API

```
GET  /v1/destinations/{id}/infrastructure-load?month=2026-08
GET  /v1/destinations/{id}/weather-risk?date_from=...&date_to=...
GET  /v1/visa?nationality=RU&destination=ES
POST /v1/report      ← композитный эндпоинт, вызывает нужное подмножество осей
```

`POST /v1/report` не содержит собственной логики скоринга — только параллельно вызывает под-эндпоинты в зависимости от того, что заполнено в форме (см. `backend/app/main.py::build_report`). Это тот же принцип `CompositeScorer`, что и в исходном ТЗ по Agenomics, только на уровне HTTP.

`asyncio.gather(..., return_exceptions=True)` — принципиально: отказ одного модуля (например, Supplier Reliability без данных оператора) не должен ронять весь отчёт, только свою секцию.

## i18n на бэкенде

Тексты `description`/`reason` хранятся в двух версиях в БД (`axis_reasons_i18n`), не переводятся на лету — машинный перевод фактов с конкретными цифрами и названиями объектов рискует исказить факт. Язык интерфейса определяется фронтендом по вводу (кириллица/латиница) и передаётся бэкенду как `detected_lang`.

## Обновление данных — разная периодичность на ось

```
ежедневно, автоматически:      weather_risk, currency_risk
еженедельно, автоматически:    wait_time (booking-страницы, отзывы)
раз в квартал, вручную/автоматом с ревью: regulatory_risk, local_sentiment, labor_action_risk
раз в квартал, импорт CSV:     infrastructure_load, price_volatility
```

Три «интерпретирующих» оси (regulatory_risk, local_sentiment, labor_action_risk) используют механизм постепенной автоматизации — см. `docs/automation_trust_tiers.md`.

## Технологический стек (MVP)

- **Backend:** Python + FastAPI (async из коробки — важно для параллельного `asyncio.gather` по 13 источникам)
- **БД:** PostgreSQL
- **Кеш отчётов:** Redis с TTL (комбинация `destination+month+profile` повторяется у многих пользователей)
- **Фронтенд:** прототип (`prototype/dashboard.html`) как основа — статичные `i18n.axes_*` заменяются на fetch к `/v1/report`

## MVP v0.1 — что входит в первую версию

**Входит сразу:**
- Infrastructure Load, Price Volatility, Wait Time — есть понятные прокси-источники
- Weather Risk, Currency Lock Risk — полностью автоматизируются с первого дня
- Trip Cost & Feasibility (виза, перелёт, турналог) — нужен для персонализации

**Откладывается на v0.2:**
- Regulatory Risk, Local Sentiment — требуют мониторинга на локальном языке
- Health & Safety, Payment Friction, Solo/Family/Mobility барьеры — важны, но не критичны для первой проверки гипотезы
- Все 4 B2B-оси — включаются после первого B2B-пилота (особенно Supplier Reliability, которая без партнёра не может работать в принципе)

## План на 4 недели

| Неделя | Задача |
|---|---|
| 1 | Зафиксировать 5 городов пилота. Собрать вручную Infrastructure Load и Price Volatility за 12 месяцев. |
| 2 | Подключить NOAA (погода) и API курсов валют — программный расчёт без ручного сбора. |
| 3 | Собрать Wait Time по 3-5 объектам на город; заменить статичные данные прототипа на реальные. |
| 4 | Сверка результатов с реальными новостными сигналами (здравый смысл), калибровка порогов. |

## Критерий успеха MVP

Индекс должен согласовываться со здравым смыслом по известным кейсам overtourism (Дубровник в августе, Венеция в пик сезона) — валидация на известных случаях до масштабирования, тот же принцип, что применялся к весам Trust Score в Agenomics.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
