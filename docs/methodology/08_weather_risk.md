# Ось 8 — Weather Risk Window

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Формула
```
Weather Risk Score = (Extreme Event Probability × 0.5) + (Comfort Deviation × 0.5)
```

| Компонент | Формула |
|---|---|
| Extreme Event Probability | % дней месяца с историческим экстремальным событием за 20+ лет |
| Comfort Deviation | отклонение ощущаемой температуры/влажности от диапазона 18-26°C, влажность <70% |

## Источники данных
NOAA, Open-Meteo — открытые исторические ряды.

## Автоматизация
Полностью автоматизируется с первого дня — единственная ось (вместе с Currency Lock Risk), не требующая никакого ручного труда на MVP.

## Обязательное требование
Расчёт привязан к конкретным датам, не к месяцу целиком — пик сезона ураганов неоднороден внутри самого сезона.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
