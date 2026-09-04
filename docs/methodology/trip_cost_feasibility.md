# Trip Cost & Feasibility (персональный блок, не входит в 13 осей)

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Отличие от 13 осей
Зависит от (origin, destination, month, duration, nationality) — уникален для конкретного запроса, в отличие от 13 осей, которые зависят только от (destination, month).

## Схема входа
```python
@dataclass
class TripQuery:
    origin: str
    destination: str
    month: str
    duration_days: int
    traveler_nationality: str | None = None
    known_flight_price: float | None = None
```

## Компоненты

### Виза
```python
@dataclass
class VisaInfo:
    required: bool
    cost: float | None
    processing_days: int | None
    max_stay_days: int | None
```
Обязательная проверка конфликта: `duration_days > max_stay_days` — блокирующая ошибка, не рядовая строка отчёта.

### Доп. платежи (турналог)
```
total_tourist_tax = per_night_fee × duration_days
```
Переиспользует Active Restrictions из оси Regulatory Risk.

### Стоимость перелёта
```python
if known_flight_price:
    deviation = (known_flight_price - route_median) / route_median × 100
else:
    estimated_price = route_median_for_month(origin, destination, month)
```
Переиспользует Price Volatility Index, но маршрутно (origin→destination).

## Источники данных
- Passport Index / re:Sonance — визовые требования по парам «гражданство → страна»
- На MVP — статическая таблица «10-15 частых гражданств × 5 направлений», обновляемая вручную раз в квартал

## Важно
`nationality` ≠ `origin` — виза зависит от паспорта, не от города вылета. Обязательное разделение полей в форме.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
