from backend.services.ioc import extract_iocs


def test_ioc_extraction():
    text = "https://updates-example.invalid/a.exe 198.51.100.24 analyst@example.org " + "a" * 64
    values = extract_iocs(text)
    assert "https://updates-example.invalid/a.exe" in values["url"]
    assert "198.51.100.24" in values["ipv4"]
    assert "analyst@example.org" in values["email"]
    assert "a" * 64 in values["sha256"]
