"""
Prizolov Lab / Destination Readiness / v0.1.0-draft
Автор: Dm.Andreyanov

Trust Tier State Machine — механизм постепенной автоматизации для трёх
интерпретирующих осей: regulatory_risk, local_sentiment, labor_action_risk.

См. docs/automation_trust_tiers.md для полного обоснования.

Доверие считается на уровне конкретного источника, не оси целиком.
Асимметрия скорости: повышение тира требует накопленной истории согласия
с человеком, понижение срабатывает от одного плохого аудита.
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum


class AutomationTier(str, Enum):
    LEARNING = "learning"          # человек проверяет 100% сигналов
    CALIBRATING = "calibrating"    # человек проверяет выборку 30%
    TRUSTED = "trusted"            # выборочный аудит 5%
    AUTONOMOUS = "autonomous"      # выборочный аудит 1% — постоянный, не 0%


TIER_ORDER = [
    AutomationTier.LEARNING,
    AutomationTier.CALIBRATING,
    AutomationTier.TRUSTED,
    AutomationTier.AUTONOMOUS,
]

# (минимум проверок, минимальная доля согласия с человеком) для перехода на следующий тир
PROMOTION_RULES: dict[AutomationTier, tuple[int, float]] = {
    AutomationTier.LEARNING: (50, 0.95),
    AutomationTier.CALIBRATING: (200, 0.97),
    AutomationTier.TRUSTED: (500, 0.98),
}

DEMOTION_THRESHOLD = 0.90  # доля согласия в контрольном аудите ниже этого — мгновенное понижение

REVIEW_RATE_BY_TIER: dict[AutomationTier, float] = {
    AutomationTier.LEARNING: 1.0,
    AutomationTier.CALIBRATING: 0.30,
    AutomationTier.TRUSTED: 0.05,
    AutomationTier.AUTONOMOUS: 0.01,  # никогда не 0 — постоянная страховка от тихого дрейфа
}


@dataclass
class SourceTrustState:
    source_id: str
    axis: str  # "regulatory_risk" | "local_sentiment" | "labor_action_risk"
    tier: AutomationTier = AutomationTier.LEARNING
    reviewed_count: int = 0
    agreement_count: int = 0
    rolling_agreement_rate: float = 0.0
    last_demoted_at: date | None = None


def _next_tier(current: AutomationTier) -> AutomationTier:
    idx = TIER_ORDER.index(current)
    return TIER_ORDER[min(idx + 1, len(TIER_ORDER) - 1)]


def _previous_tier(current: AutomationTier) -> AutomationTier:
    idx = TIER_ORDER.index(current)
    return TIER_ORDER[max(idx - 1, 0)]


def evaluate_promotion(source: SourceTrustState) -> AutomationTier:
    """Проверяет, не пора ли повысить тир источника. Не понижает — для этого check_demotion."""
    rule = PROMOTION_RULES.get(source.tier)
    if rule is None:
        return source.tier  # уже AUTONOMOUS — дальше повышать некуда
    min_reviews, min_agreement = rule
    if source.reviewed_count >= min_reviews and source.rolling_agreement_rate >= min_agreement:
        return _next_tier(source.tier)
    return source.tier


def check_demotion(source: SourceTrustState, latest_audit_agreement: float) -> AutomationTier:
    """Понижение мгновенное, не постепенное — сознательная асимметрия с evaluate_promotion."""
    if latest_audit_agreement < DEMOTION_THRESHOLD:
        return _previous_tier(source.tier)
    return source.tier


def review_sample_rate(tier: AutomationTier) -> float:
    """Какую долю сигналов этого источника нужно направить на ручную проверку."""
    return REVIEW_RATE_BY_TIER[tier]


def initial_tier_for_new_source(similar_source_tier: AutomationTier | None) -> AutomationTier:
    """Ускорение для новых источников того же типа, что уже прошли путь до TRUSTED+.

    Если аналогичный по формату источник (тот же тип RSS/календаря) уже
    доверенный, новый стартует не с LEARNING, а сразу с CALIBRATING.
    """
    if similar_source_tier in (AutomationTier.TRUSTED, AutomationTier.AUTONOMOUS):
        return AutomationTier.CALIBRATING
    return AutomationTier.LEARNING
