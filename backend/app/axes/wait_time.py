"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Ось 3 — Wait Time Burden. См. docs/methodology/03_wait_time.md
"""
from app.models.schemas import ScoreResult


async def get_wait_time(destination_id: str) -> ScoreResult:
    # TODO: booking-API объектов (time-slot) + отзывы с датами посещения
    top_venue = "Sagrada Familia"
    peak_wait = 90
    threshold = 45
    score = min(peak_wait / threshold * 100, 150)
    return ScoreResult(
        axis="wait_time",
        score=round(score, 1),
        label="high" if score > 100 else "medium" if score > 50 else "low",
        description="Реальное время ожидания в очереди к самой посещаемой достопримечательности.",
        reason=f"{top_venue} — около {peak_wait} мин без предварительной брони.",
        source="booking_pages+reviews",
    )
