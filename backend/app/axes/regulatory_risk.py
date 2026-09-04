"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Ось 2 — Regulatory Risk.
См. docs/methodology/02_regulatory_risk.md

Интерпретирующая ось — проходит через trust-tier механизм (app/trust/trust_tier.py).
Каждый сигнал обязан нести конкретную ссылку и дату — не абстрактный вывод.
"""
from app.models.schemas import ScoreResult


async def get_regulatory_risk(destination_id: str) -> ScoreResult:
    # TODO: реальный запрос к axis_regulatory_risk, заполняемой через
    # automated_signal_scan() + classify_signal() с review-очередью для
    # источников ниже TRUSTED-тира (см. app/trust/trust_tier.py)
    active_restrictions_score = 35.0
    pending_legislation_score = 20.0
    historical_volatility_score = 60.0

    score = (
        active_restrictions_score * 0.35
        + pending_legislation_score * 0.35
        + historical_volatility_score * 0.30
    )

    return ScoreResult(
        axis="regulatory_risk",
        score=round(score, 1),
        label="high" if score > 60 else "medium" if score > 30 else "low",
        description="Вероятность новых или уже действующих ограничений для туристов.",
        reason="Обсуждается расширение туристического сбора, закон пока не принят.",
        source="municipal_records+news_monitoring",
    )
