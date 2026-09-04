"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Ось 5 — Price Volatility Index. См. docs/methodology/05_price_volatility.md
"""
from app.models.schemas import ScoreResult


async def get_price_volatility(destination_id: str, month: str) -> ScoreResult:
    # TODO: Amadeus/Travelpayouts (перелёты) + Booking/Airbnb partner API (жильё)
    accommodation_volatility = 65.0  # % отклонения от годовой медианы
    return ScoreResult(
        axis="price_volatility",
        score=accommodation_volatility,
        label="high" if accommodation_volatility > 40 else "medium" if accommodation_volatility > 15 else "low",
        description="Насколько цена в выбранном месяце отклоняется от годовой медианы.",
        reason=f"Жильё в этот месяц примерно на {accommodation_volatility:.0f}% дороже, чем в среднем за год.",
        source="booking_partner_api",
    )
