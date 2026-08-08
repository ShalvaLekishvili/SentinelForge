from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from backend.config import RULES_DIR

ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}


def _field_value(event: dict[str, Any], field: str) -> str:
    value = event.get(field, "")
    return str(value) if value is not None else ""


def _match_clause(event: dict[str, Any], clause: dict[str, Any]) -> tuple[bool, list[str]]:
    field = str(clause.get("field", ""))
    operator = str(clause.get("operator", "contains")).lower()
    expected = clause.get("value", "")
    actual = _field_value(event, field)
    values = expected if isinstance(expected, list) else [expected]
    evidence: list[str] = []

    def one(value: Any) -> bool:
        needle = str(value)
        if operator == "equals":
            return actual.lower() == needle.lower()
        if operator == "contains":
            return needle.lower() in actual.lower()
        if operator == "startswith":
            return actual.lower().startswith(needle.lower())
        if operator == "endswith":
            return actual.lower().endswith(needle.lower())
        if operator == "regex":
            return re.search(needle, actual, re.IGNORECASE) is not None
        if operator == "exists":
            return bool(actual.strip()) is bool(value)
        raise ValueError(f"Unsupported operator: {operator}")

    matched = any(one(value) for value in values)
    if matched:
        evidence.append(f"{field} {operator} {expected!r}")
    return matched, evidence


def validate_rule(rule: dict[str, Any]) -> None:
    required = {"id", "title", "severity", "detection"}
    missing = required - rule.keys()
    if missing:
        raise ValueError(f"Missing rule keys: {sorted(missing)}")
    if str(rule["severity"]).lower() not in ALLOWED_SEVERITIES:
        raise ValueError(f"Invalid severity: {rule['severity']}")
    if str(rule.get("confidence", "medium")).lower() not in ALLOWED_CONFIDENCE:
        raise ValueError(f"Invalid confidence: {rule.get('confidence')}")
    detection = rule["detection"]
    if not isinstance(detection, dict) or not isinstance(detection.get("clauses"), list):
        raise ValueError("detection.clauses must be a list")
    if detection.get("condition", "all") not in {"all", "any"}:
        raise ValueError("detection.condition must be 'all' or 'any'")


@lru_cache(maxsize=1)
def load_rules(directory: str | Path = RULES_DIR) -> tuple[dict[str, Any], ...]:
    loaded: list[dict[str, Any]] = []
    for path in sorted(Path(directory).glob("*.yml")):
        with path.open("r", encoding="utf-8") as handle:
            rule = yaml.safe_load(handle) or {}
        validate_rule(rule)
        rule["_source"] = path.name
        loaded.append(rule)
    return tuple(loaded)


def clear_rule_cache() -> None:
    load_rules.cache_clear()


def evaluate_rule(event: dict[str, Any], rule: dict[str, Any]) -> tuple[bool, list[str]]:
    detection = rule["detection"]
    results: list[bool] = []
    evidence: list[str] = []
    for clause in detection["clauses"]:
        matched, clause_evidence = _match_clause(event, clause)
        results.append(matched)
        evidence.extend(clause_evidence)
    condition = detection.get("condition", "all")
    return (all(results) if condition == "all" else any(results)), evidence


def run_detections(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for event in events:
        for rule in load_rules():
            matched, evidence = evaluate_rule(event, rule)
            if not matched:
                continue
            findings.append({
                "rule_id": rule["id"],
                "title": rule["title"],
                "description": rule.get("description", ""),
                "severity": str(rule["severity"]).lower(),
                "confidence": str(rule.get("confidence", "medium")).lower(),
                "mitre": list(rule.get("mitre", [])),
                "event_id": event["id"],
                "timestamp": event.get("timestamp", ""),
                "host": event.get("host", ""),
                "user": event.get("user", ""),
                "process": event.get("process", ""),
                "command_line": event.get("command_line", ""),
                "evidence": evidence,
            })
    return findings
