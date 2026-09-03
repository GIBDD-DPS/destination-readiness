# Постепенная автоматизация текстовых осей

> **Prizolov Lab** · Destination Readiness · Автор: Dm.Andreyanov · Версия: v0.1.0-draft

## Какие оси это затрагивает

Из 13+ осей реального «накопления доверия» требуют только три — те, где нужна интерпретация текста, а не готовое число из API:

| Группа | Оси | Путь к автоматизации |
|---|---|---|
| Численные, детерминированные | Weather, Currency, Infrastructure Load, Price Volatility, Health & Safety, Group Capacity | Автоматизация сразу на 100% при подключении API |
| Численные, партнёрский доступ | Wait Time, Supplier Reliability | Автоматизация зависит от бизнес-интеграции, не от доверия к данным |
| **Интерпретирующие (LLM-классификация)** | **Regulatory Risk, Local Sentiment, Labor Action Risk** | **Требуют механизма ниже** |

## Trust Tier State Machine

```python
class AutomationTier(Enum):
    LEARNING = "learning"        # человек проверяет 100% сигналов
    CALIBRATING = "calibrating"  # человек проверяет выборку 30%
    TRUSTED = "trusted"          # выборочный аудит 5%
    AUTONOMOUS = "autonomous"    # выборочный аудит 1% — постоянный, не 0%
```

Доверие считается на уровне **конкретного источника**, не оси целиком — RSS муниципального совета и профсоюзный календарь забастовок имеют разную надёжность даже в рамках одной оси. Понижение доверия к одному источнику не откатывает остальные.

## Правила повышения/понижения

```python
PROMOTION_RULES = {
    AutomationTier.LEARNING:    (50,  0.95),   # (мин. проверок, мин. согласие)
    AutomationTier.CALIBRATING: (200, 0.97),
    AutomationTier.TRUSTED:     (500, 0.98),
}

def evaluate_tier(source):
    if source.reviewed_count >= min_reviews and source.rolling_agreement_rate >= min_agreement:
        return next_tier(source.tier)
    return source.tier

def check_demotion(source, latest_audit_agreement):
    # Понижение мгновенное, не постепенное — сознательная асимметрия.
    if latest_audit_agreement < 0.90:
        return demote_one_tier(source.tier)
    return source.tier
```

**Асимметрия скорости:** повышение требует сотен подтверждений подряд, понижение срабатывает от одного плохого аудита. Ложный `AUTONOMOUS`-статус (незамеченная ошибка публикуется как факт) стоит дороже, чем лишний цикл ручной проверки.

## Постоянный контрольный аудит — даже на AUTONOMOUS

```python
async def scheduled_drift_check():
    # Даже в AUTONOMOUS — 1% сигналов уходит на ручную проверку.
    # Не блокирует публикацию — сигнал публикуется сразу, аудит идёт параллельно
    # как страховка от тихого дрейфа источника или деградации классификации.
    sample = await sample_autonomous_signals(rate=0.01)
    for signal in sample:
        human_verdict = await review_queue.enqueue(signal)
        update_trust_state(signal.source_id, human_verdict)
```

## Ускорение для новых городов

Если источник того же типа (тот же формат муниципального RSS) уже прошёл путь до `TRUSTED` в одном городе, аналогичный источник в новом городе стартует не с `LEARNING`, а сразу с `CALIBRATING` — доверие накапливается к типу источника и методу классификации, а не только к конкретному городу.

## Реалистичный график (иллюстративно)

| Ось | LEARNING → CALIBRATING | → TRUSTED | → AUTONOMOUS |
|---|---|---|---|
| Regulatory Risk | ~7-10 недель | ~месяц 4-5 | ~месяц 8-10 |
| Local Sentiment | параллельно | параллельно | параллельно |
| Labor Action Risk | быстрее (структурированные календари) | ~месяц 3 | ~месяц 6 |

## Схема данных для отслеживания доверия

См. `source_trust_state` в `backend/app/db/schema.sql`.

---
*Prizolov Lab · Destination Readiness · v0.1.0-draft*
