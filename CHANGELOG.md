# Changelog

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov

Все существенные изменения проекта фиксируются в этом файле. Формат основан на [Keep a Changelog](https://keepachangelog.com/), версионирование — [Semantic Versioning](https://semver.org/).

## [0.1.0-draft] — unreleased

### Added
- Методология всех 13 осей + Trip Cost & Feasibility блок (`docs/methodology/`)
- Архитектурный документ и схема БД (`docs/architecture.md`, `backend/app/db/schema.sql`)
- Trust Tier механизм для интерпретирующих осей (`docs/automation_trust_tiers.md`)
- HTML-прототип формы ввода и дашборда с RU/EN автоопределением (`prototype/dashboard.html`)
- Каркас FastAPI-бэкенда: 13 axis-модулей, композитный `/v1/report` эндпоинт, тест на устойчивость к частичным отказам (`backend/`)
- `README.md`, `LICENSE` (MIT)

### Known limitations
- Все значения в axis-модулях захардкожены (`# TODO: заменить на реальный запрос`) — реальные API ещё не подключены
- Тестовое покрытие минимальное — один файл, проверяющий устойчивость к частичным отказам

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
