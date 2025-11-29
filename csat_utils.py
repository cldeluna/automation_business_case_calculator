from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SentimentDist:
    happy: float
    neutral: float
    sad: float

    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.happy, self.neutral, self.sad)


SENTIMENT_PRESETS = {
    "Customers mostly happy": SentimentDist(0.60, 0.30, 0.10),
    "Customer ambivalent": SentimentDist(1 / 3, 1 / 3, 1 / 3),
    "Customers mostly unhappy": SentimentDist(0.10, 0.30, 0.60),
}


def apply_distribution(expected_total: int, sentiment_label: str) -> Tuple[int, int, int]:
    """
    Compute Happy/Neutral/Sad counts from expected_total and a preset label.
    Uses rounding for H and N and assigns remainder to S to keep totals exact and non-negative.
    """
    dist = SENTIMENT_PRESETS.get(sentiment_label)
    if not dist or expected_total <= 0:
        return (0, 0, 0)
    p_h, p_n, p_s = dist.as_tuple()
    new_h = int(round(expected_total * p_h))
    new_n = int(round(expected_total * p_n))
    new_s = int(expected_total - new_h - new_n)
    if new_s < 0:
        new_s = 0
        new_n = max(0, expected_total - new_h)
    return (new_h, new_n, new_s)


def responses_per_year(changes_per_month: float, responses_per_change: float, response_rate_pct: float) -> float:
    changes_per_year = (changes_per_month or 0.0) * 12.0
    response_rate = max(0.0, min(100.0, response_rate_pct or 0.0)) / 100.0
    return changes_per_year * (responses_per_change or 0.0) * response_rate


def ces(happy: int, sad: int, total: int) -> float | None:
    if total <= 0:
        return None
    return (float(happy) - float(sad)) / float(total)


def total_cost(happy_cnt: int, neutral_cnt: int, sad_cnt: int, w_happy: float, w_neutral: float, w_sad: float) -> float:
    return (happy_cnt * (w_happy or 0.0)) + (neutral_cnt * (w_neutral or 0.0)) + (sad_cnt * (w_sad or 0.0))


def avg_cost_per_response(total_cost_value: float, total_responses: int) -> float | None:
    if total_responses <= 0:
        return None
    return float(total_cost_value) / float(total_responses)


def annual_csat_cost(avg_cost_per_resp: float | None, responses_year: float) -> float:
    return float(avg_cost_per_resp or 0.0) * float(responses_year or 0.0)


def minutes_to_cost(minutes: float, hourly_rate: float) -> float:
    """Convert minutes of work to cost using hourly rate."""
    return (float(minutes or 0.0) / 60.0) * float(hourly_rate or 0.0)
