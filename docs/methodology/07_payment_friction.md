# Ось 7 — Payment & Cash Friction

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Формула
```
Payment Friction Score = (Card Acceptance Gap × 0.5)
                        + (ATM Fee Burden × 0.3)
                        + (Airport Exchange Markup × 0.2)
```

| Компонент | Формула |
|---|---|
| Card Acceptance Gap | 100 − доля точек, принимающих карты |
| ATM Fee Burden | средняя комиссия за снятие, нормированная к медиане выборки |
| Airport Exchange Markup | % отклонения курса в аэропорту от межбанковского |

## Источники данных
- Visa/Mastercard агрегированные отчёты (страновой уровень)
- Сайты обменников/банков (городской уровень, периодический импорт)

## Автоматизация
Периодический автоимпорт годовых отчётов — не real-time API, но не требует ручной классификации текста.

## Пример (иллюстративно)
```
Бали: Card Gap 60, ATM Fee 70, Exchange Markup 40
Friction = 60×0.5+70×0.3+40×0.2 = 59 → «Заметное неудобство»
```

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
