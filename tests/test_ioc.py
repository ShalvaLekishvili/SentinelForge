from backend.services.ioc import extract_iocs


def test_ioc_extraction():
    result = extract_iocs("connect to 198.51.100.24 then fetch https://example.invalid/a")
    assert "198.51.100.24" in result["ipv4"]
    assert "https://example.invalid/a" in result["url"]
