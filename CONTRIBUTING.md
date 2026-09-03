# Contributing

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Принципы, которые нельзя нарушать

1. **Non-Coupling.** Модуль в `backend/app/axes/` не может импортировать другой модуль из этой же папки. Единственная разрешённая связь — через `SuggestedAudit` в `ScoreResult`.
2. **not_applicable ≠ 0.** Если данных недостаточно, `ScoreResult.score = None` и `is_applicable = False`. Подстановка 0 или среднего значения вместо этого считается багом.
3. **Каждое значение — с причиной.** Поле `reason` в `ScoreResult` обязательно для непустого `score`.

## Как запустить тесты

```
cd backend
pip install -r requirements.txt
pytest tests/
```

## Как добавить новый источник данных для интерпретирующей оси

Regulatory Risk, Local Sentiment и Labor Action Risk используют trust-tier механизм (`backend/app/trust/trust_tier.py`). Новый источник стартует с `AutomationTier.LEARNING`, если аналогичного по формату источника ещё не было в системе — см. `initial_tier_for_new_source()`.

## Стиль коммитов

Формат: `<тип>: <краткое описание>` — например, `feat: add wait_time booking API integration` или `fix: correct rounding in currency_lock_risk`. Типы: `feat`, `fix`, `docs`, `refactor`, `test`.

## Авторство

Любой вклад в проект сохраняет атрибуцию **Prizolov Lab** и оригинальное авторство методологии за Dm.Andreyanov — см. `LICENSE`.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
