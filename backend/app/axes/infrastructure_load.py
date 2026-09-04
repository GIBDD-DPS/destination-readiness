"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Ось 1 — Infrastructure Load.
См. docs/methodology/01_infrastructure_load.md

Независимый модуль: не импортирует и не вызывает код других осей.
"""
from app.models.schemas import ScoreResult


DENSITY_THRESHOLDS = [
    (0.5, 20), (1.5, 40), (3.0, 65), (5.0, 85), (float("inf"), 100),
]


def _density_score(ratio: float) -> float:
    for threshold, score in DENSITY_THRESHOLDS:
        if ratio < threshold:
            return score
    return 100


async def get_infrastructure_load(destination_id: str, month: str) -> ScoreResult:
    # TODO: заменить на реальный запрос к axis_infrastructure_load
    tourist_count = 1_800_000
    population = 1_600_000
    occupancy = 0.92
    transit_strain = 1.15

    density_ratio = tourist_count / population
    density_score = _density_score(density_ratio)
    accommodation_score = min(occupancy * 100, 100)
    transit_score = min(transit_strain * 100, 100)

    load_index = density_score * 0.4 + accommodation_score * 0.3 + transit_score * 0.3

    return ScoreResult(
        axis="infrastructure_load",
        score=round(load_index, 1),
        label="high" if load_index > 60 else "medium" if load_index > 35 else "low",
        description="Отношение туристического потока к пропускной способности инфраструктуры города.",
        reason=f"Плотность туристов {density_ratio:.1f}x, occupancy {occupancy:.0%}, транспорт {transit_strain:.0%} от нормы.",
        source="municipal_open_data",
    )
