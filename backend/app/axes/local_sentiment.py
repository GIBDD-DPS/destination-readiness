"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Ось 4 — Local Sentiment Strain. См. docs/methodology/04_local_sentiment.md
Интерпретирующая ось — проходит через trust-tier механизм.
"""
from app.models.schemas import ScoreResult


async def get_local_sentiment(destination_id: str) -> ScoreResult:
    # TODO: ACLED API (протесты) + News API/GDELT (локальные СМИ) + петиции
    protest_score, media_score, petition_score = 96.0, 45.0, 9.4
    score = protest_score * 0.4 + media_score * 0.3 + petition_score * 0.3
    return ScoreResult(
        axis="local_sentiment",
        score=round(score, 1),
        label="high" if score > 60 else "medium" if score > 30 else "low",
        description="Уровень напряжённости между жителями и туристами.",
        reason="Зафиксированы протестные акции, но массовой петиционной поддержки не наблюдается.",
        source="acled+local_media",
    )
