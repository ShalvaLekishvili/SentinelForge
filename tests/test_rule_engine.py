from backend.services.rule_engine import evaluate_rule, load_rules


def test_rule_library_loads():
    rules = load_rules()
    assert len(rules) >= 12
    assert all(rule["id"].startswith("SF-") for rule in rules)


def test_encoded_powershell_rule_matches():
    rule = next(r for r in load_rules() if r["id"] == "SF-EXEC-001")
    event = {"process": "powershell.exe", "command_line": "powershell -enc SQBFAFgA"}
    matched, evidence = evaluate_rule(event, rule)
    assert matched is True
    assert evidence
