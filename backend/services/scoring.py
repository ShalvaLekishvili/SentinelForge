WEIGHTS = {"critical": 35, "high": 20, "medium": 10, "low": 3}


def risk_summary(detections):
    raw = sum(WEIGHTS.get(d.get("severity", "low"), 1) for d in detections)
    score = min(raw, 100)
    if score >= 75:
        level = "Critical"
    elif score >= 50:
        level = "High"
    elif score >= 20:
        level = "Medium"
    else:
        level = "Low"
    counts = {k: 0 for k in WEIGHTS}
    for detection in detections:
        sev = detection.get("severity", "low")
        counts[sev] = counts.get(sev, 0) + 1
    return {"score": score, "level": level, "counts": counts}
