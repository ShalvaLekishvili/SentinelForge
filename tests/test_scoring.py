from backend.services.scoring import risk_summary


def test_risk_score_uses_severity_and_confidence():
    result = risk_summary([
        {"rule_id": "A", "event_id": 1, "severity": "critical", "confidence": "high"},
        {"rule_id": "B", "event_id": 2, "severity": "high", "confidence": "medium"},
    ])
    assert result["score"] >= 50
    assert result["level"] in {"High", "Critical"}
