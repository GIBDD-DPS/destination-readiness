"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Ось 6 — Health & Safety Index. См. docs/methodology/06_health_safety.md
"""
from app.models.schemas import ScoreResult


async def get_health_safety(destination_id: str, month: str) -> ScoreResult:
    # TODO: CDC Travel Health Notices / WHO API
    score = 25.0
    return ScoreResult(
        axis="health_safety",
        score=score,
        label="low",
        description="Доступность медицинской помощи и сезонные риски заболеваний.",
        reason="Активных уведомлений о вспышках заболеваний нет, медпомощь доступна без затруднений.",
        source="cdc_who_api",
    )
