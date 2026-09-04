"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Общие схемы запроса/ответа.

Принцип: единая форма результата для всех осей (ScoreResult), но каждая ось
сама решает, заполнять ли score, или вернуть not_applicable — отсутствие
данных не должно маскироваться под 0 или средний балл.
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class TravelerMode(str, Enum):
    B2C = "b2c"
    B2B = "b2b"


@dataclass
class TripQuery:
    destination: str
    month: str  # YYYY-MM
    duration_days: int
    origin: str | None = None
    nationality: str | None = None
    adults: int = 1
    children: int = 0
    mobility_flag: bool = False
    known_flight_price: float | None = None
    mode: TravelerMode = TravelerMode.B2C
    # Поля ниже — только для mode == B2B
    group_size: int | None = None
    booking_lag_days: int | None = None
    operator_id: str | None = None
    detected_lang: str = "ru"  # "ru" | "en", определяется фронтендом по вводу

    @property
    def is_solo(self) -> bool:
        return self.adults == 1 and self.children == 0

    @property
    def has_children(self) -> bool:
        return self.children > 0


@dataclass
class ScoreResult:
    """Единая форма результата для каждой оси."""
    axis: str
    score: float | None  # None если not_applicable — НЕ 0
    label: str | None
    description: str  # что измеряет ось (не зависит от конкретного запроса)
    reason: str | None  # почему именно такое значение в этом конкретном случае
    is_applicable: bool = True
    capped_reason: str | None = None
    source: str | None = None
    data_snapshot_date: date | None = None
    suggested_next: list["SuggestedAudit"] = field(default_factory=list)


@dataclass
class SuggestedAudit:
    """Подсказка на релевантный модуль — НЕ вызов другого модуля.

    Формируется исключительно на основе полей, уже присутствующих
    в текущем запросе, без обращения к коду другой оси.
    """
    axis_id: str
    reason: str


@dataclass
class ReportResponse:
    query: TripQuery
    destination_axes: list[ScoreResult]
    trip_cost: list[ScoreResult]
    profile_barriers: list[ScoreResult]
    b2b_axes: list[ScoreResult]
    generated_at: date
    lang: str
