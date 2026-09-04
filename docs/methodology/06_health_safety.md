# Ось 6 — Health & Safety Index

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Что измеряет
Доступность и качество медпомощи, сезонные риски заболеваний, обязательность страховки.

## Формула
```
Health Risk Score = (Medical Access Gap × 0.4)
                   + (Seasonal Disease Risk × 0.35)
                   + (Insurance Mandate Flag × 0.25)
```

| Компонент | Как считается |
|---|---|
| Medical Access Gap | Стоимость визита к врачу без страховки, нормированная к медиане выборки; +15 при отсутствии англоязычного/русскоязычного персонала |
| Seasonal Disease Risk | 0/50/100 по WHO/CDC travel health notices для месяца и региона |
| Insurance Mandate Flag | Бинарный — обязательна ли страховка по визовым правилам |

## Источники данных
- CDC Travel Health Notices, WHO API
- Aetna International / Cigna Global — ориентировочные тарифы по странам

## Автоматизация
Открытые структурированные API — автоматизируется полностью с первого дня.

## B2B-расширение (Duty of Care)
```python
@dataclass
class DutyOfCareDetail:
    accredited_hospitals: list[str]
    cashless_partner_coverage: bool
    evacuation_time_hours: float | None
```
B2B-отчёт обязан называть конкретные аккредитованные госпитали, не общий балл.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
