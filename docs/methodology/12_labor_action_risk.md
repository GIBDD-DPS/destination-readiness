# Ось 12 — Labor Action Risk (B2B)

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Формула
```
Labor Risk Score = (Historical Strike Frequency × 0.5) + (Active Labor Dispute Signal × 0.5)
```

| Компонент | Формула |
|---|---|
| Historical Strike Frequency | число забастовок транспорта/аэропортов за 24 мес., потолок 100 |
| Active Labor Dispute Signal | structured news monitoring на локальном языке ("grève", "sciopero") |

## Источники данных
Профсоюзные календари предупредительных забастовок (préavis de grève во Франции публикуются заранее и структурированно) — лучшая точка старта пилота именно для этой оси.

## Автоматизация
Требует trust-tier механизма, но быстрее выходит на AUTONOMOUS, чем Regulatory Risk — структурированные календари оставляют меньше простора для ошибки классификации.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
