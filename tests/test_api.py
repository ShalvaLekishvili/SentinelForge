from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_and_rules():
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["version"] == "0.2.0"
    rules = client.get("/api/rules")
    assert rules.status_code == 200
    assert len(rules.json()) >= 12


def test_rejects_unsupported_file():
    response = client.post("/api/analyze", files={"file": ("payload.exe", b"MZ", "application/octet-stream")})
    assert response.status_code == 415
