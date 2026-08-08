from backend.services.detector import run_detections


def test_encoded_powershell_detection():
    events = [{"id": 1, "timestamp": "", "process": "powershell.exe", "parent_process": "", "command_line": "powershell -enc AAA", "raw": {}}]
    findings = run_detections(events)
    assert any(item["rule_id"] == "SF-EXEC-001" for item in findings)


def test_registry_run_key_detection():
    events = [{"id": 1, "timestamp": "", "process": "reg.exe", "parent_process": "", "command_line": r"reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Test /d a.exe", "raw": {}}]
    findings = run_detections(events)
    assert any(item["rule_id"] == "SF-PERS-001" for item in findings)
