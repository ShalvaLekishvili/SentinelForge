from pathlib import Path

from backend.services.analyzer import analyze_bytes

ROOT = Path(__file__).resolve().parent.parent


def test_demo_incident_produces_investigation():
    path = ROOT / "sample-data" / "demo-incident.json"
    result = analyze_bytes(path.read_bytes(), ".json", path.name)
    assert result["event_count"] == 7
    assert result["detection_count"] >= 6
    assert result["risk"]["level"] in {"High", "Critical"}
    assert any(item["technique"] == "T1059.001" for item in result["mitre_coverage"])
    assert result["process_tree"]
