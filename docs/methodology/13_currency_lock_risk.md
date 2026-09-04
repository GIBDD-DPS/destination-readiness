# Ось 13 — Currency & Pricing Lock Risk (B2B)

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Формула
```
Currency Lock Risk = (Historical Volatility of Pair × 0.6) + (Booking-to-Travel Lag Exposure × 0.4)
exposure = pair_volatility_annualized * (avg_lag_days / 365)
```

## Источники данных
Любой финансовый API курсов валют — полностью открытые данные.

## Автоматизация
Полностью автоматизируется с первого дня, наравне с Weather Risk — не требует ручного сбора или классификации.

## Ограничение
Ось не даёт рекомендации «хеджировать/не хеджировать» — только входные данные (exposure в цифрах) для финансового отдела оператора.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
