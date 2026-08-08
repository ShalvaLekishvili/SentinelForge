from __future__ import annotations

from collections import Counter

SEVERITY_WEIGHTS = {"critical": 40, "high": 22, "medium": 10, "low": 3}
CONFIDENCE_MULTIPLIERS = {"high": 1.0, "medium": 0.85, "low": 0.65}


def risk_summary(detections: list[dict]) -> dict:
    unique_pairs = {(d.get("rule_id"), d.get("event_id")): d for d in detections}
    raw = sum(
        SEVERITY_WEIGHTS.get(d.get("severity", "low"), 1)
        * CONFIDENCE_MULTIPLIERS.get(d.get("confidence", "medium"), 0.85)
        for d in unique_pairs.values()
    )
    score = min(round(raw), 100)
    level = "Critical" if score >= 75 else "High" if score >= 50 else "Medium" if score >= 20 else "Low"
    counts = Counter(d.get("severity", "low") for d in detections)
    return {
        "score": score,
        "level": level,
        "counts": {key: counts.get(key, 0) for key in SEVERITY_WEIGHTS},
        "model": "severity × confidence, capped at 100",
    }
