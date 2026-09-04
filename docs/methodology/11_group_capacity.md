# Ось 11 — Group Capacity Feasibility (B2B)

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Формат — статус, не число
```
Feasibility = OK | CONFLICT | AT_RISK
```

```python
def check_group_feasibility(venue, date, group_size, existing_bookings):
    available_capacity = venue.daily_capacity - sum(existing_bookings[date])
    if group_size > available_capacity:
        return "CONFLICT", f"доступно {available_capacity} мест из {group_size} нужных"
    elif available_capacity - group_size < venue.daily_capacity * 0.1:
        return "AT_RISK", "менее 10% запаса"
    return "OK", None
```

## Источники данных
Та же инфраструктура, что и для оси Wait Time — time-slot booking API объектов.

## Автоматизация
Партнёрский API там, где объект продаёт групповые слоты. Для объектов без такой системы — `not_applicable`, ложный «OK» здесь опаснее отсутствия данных.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
