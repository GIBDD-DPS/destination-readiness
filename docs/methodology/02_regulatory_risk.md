# Ось 2 — Regulatory Risk

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Что измеряет
Вероятность новых или уже действующих ограничений для туристов — налоги, лимиты, запреты аренды.

## Формула

```
Regulatory Risk Index = (Active Restrictions × 0.35)
                       + (Pending Legislation Signal × 0.35)
                       + (Historical Volatility × 0.30)
```

### Active Restrictions (вес 0.35)
| Тип ограничения | Балл вклада |
|---|---|
| Туристический налог/сбор | +15 |
| Лимит круизных судов | +20 |
| Запрет/ограничение краткосрочной аренды | +20 |
| Квоты на посещение объектов | +15 |
| Комендантский час/ограничения на алкоголь | +10 |
Сумма с потолком 100.

### Pending Legislation Signal (вес 0.35) — structured news monitoring
```
1. Фиксированные запросы на языке страны ("turismo + tasa", "limite + turisti" и т.п.)
2. Фильтр по официальным муниципальным источникам и локальным СМИ, окно 6 месяцев
3. Классификация стадии:
   обсуждается в совете → +10 | внесён законопроект → +20 | принят, вступает позже даты → +30
```

### Historical Volatility (вес 0.30)
```
Historical Volatility = число значимых изменений политики за 36 месяцев × 15, потолок 100
```

## Источники данных
- Муниципальные сайты постановлений (Active Restrictions)
- News API / GDELT для локальных СМИ (Pending Legislation)
- Архив муниципальных решений за 3 года (Historical Volatility)

## Автоматизация
Единственная из трёх «интерпретирующих» осей — требует trust-tier механизма (см. `docs/automation_trust_tiers.md`). Active Restrictions структурирован и автоматизируется быстро; Pending Legislation Signal требует LLM-классификации локальных новостей и проходит через `LEARNING → AUTONOMOUS`.

## Обязательное требование
Каждый найденный сигнал публикуется вместе с конкретной ссылкой и датой — не абстрактным выводом «ожидаются ограничения».

## Пример расчёта (иллюстративно)
```
Венеция:
Active Restrictions: 15+20 = 35 → балл 35
Pending Legislation: "внесён законопроект" = 20
Historical Volatility: 4 изменения × 15 = 60

Regulatory Risk Index = 35×0.35 + 20×0.35 + 60×0.30 = 37.25 → «Средний риск»
```

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
