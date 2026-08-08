from backend.parsers.common import normalize_event


def test_wazuh_sysmon_shape_normalizes():
    raw = {
        "@timestamp": "2026-08-08T12:00:00Z",
        "agent": {"name": "WIN-01"},
        "win": {
            "system": {"eventID": "1", "channel": "Microsoft-Windows-Sysmon/Operational"},
            "eventdata": {
                "image": "C:\\Windows\\System32\\cmd.exe",
                "processId": "100",
                "parentProcessId": "50",
                "commandLine": "cmd.exe /c whoami",
            },
        },
    }
    event = normalize_event(raw, 0)
    assert event["host"] == "WIN-01"
    assert event["event_id"] == "1"
    assert event["process_id"] == "100"
    assert event["process"].endswith("cmd.exe")
