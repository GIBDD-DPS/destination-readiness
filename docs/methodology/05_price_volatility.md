# Ось 5 — Price Volatility Index

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Что измеряет
Отклонение цены в выбранном месяце от годовой медианы — отдельно для жилья и перелётов.

## Формула
```
Price Volatility Index = ((Price(month) - Median(year)) / Median(year)) × 100
```
Считается раздельно: `Accommodation Volatility` и `Flight Volatility` — не усредняются.

## Ключевое разделение: волатильность vs абсолютная дороговизна
```
Absolute Price Tier = квартиль медианной годовой цены относительно всей выборки направлений
Seasonal Volatility  = отклонение конкретного месяца от медианы этого же города
```
Направление может быть дорогим в принципе (высокий Tier), но не волатильным по сезону, и наоборот — оба сигнала показываются, не схлопываются.

## Дополнительно: Booking Window Sensitivity
```
Booking Window Sensitivity = (Price at T-30 days - Price at T-180 days) / Price at T-180 days × 100
```
Положительное — цена растёт к дате (бронировать заранее), отрицательное — продажа остатков со скидкой ближе к дате.

## Источники данных
- Amadeus for Developers / Travelpayouts — авиабилеты
- Booking.com/Airbnb публичный поиск — жильё (через партнёрский API, не скрейпинг)

## Автоматизация
Численная, детерминированная ось — автоматизируется полностью при подключении партнёрских API.

## Пример расчёта (иллюстративно)
```
Санторини, август:
Accommodation Volatility: $180→$340 = +89%
Flight Volatility: $220→$310 = +41%
Absolute Price Tier: 3-й квартиль (дорого даже вне пика)
Booking Window Sensitivity: +35% за 30 дней до поездки → бронировать заранее
```

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
