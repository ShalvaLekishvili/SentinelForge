from __future__ import annotations

import re
from typing import Any

RULES = [
    {
        "id": "SF-EXEC-001",
        "title": "Encoded PowerShell Execution",
        "severity": "high",
        "mitre": "T1059.001",
        "matcher": lambda e, text: bool(re.search(r"powershell(?:\.exe)?", text, re.I) and re.search(r"(?:-enc|-encodedcommand)\b", text, re.I)),
    },
    {
        "id": "SF-EXEC-002",
        "title": "Office Application Spawned PowerShell",
        "severity": "high",
        "mitre": "T1204.002 / T1059.001",
        "matcher": lambda e, text: any(x in (e.get("parent_process") or "").lower() for x in ("winword", "excel", "powerpnt", "outlook")) and "powershell" in (e.get("process") or "").lower(),
    },
    {
        "id": "SF-PERS-001",
        "title": "Registry Run Key Persistence Indicator",
        "severity": "medium",
        "mitre": "T1060 / T1547.001",
        "matcher": lambda e, text: bool(re.search(r"\\CurrentVersion\\Run(?:Once)?\b", text, re.I)),
    },
    {
        "id": "SF-PERS-002",
        "title": "Scheduled Task Creation Indicator",
        "severity": "medium",
        "mitre": "T1053.005",
        "matcher": lambda e, text: bool(re.search(r"schtasks(?:\.exe)?\s+/create", text, re.I)),
    },
    {
        "id": "SF-CRED-001",
        "title": "Potential LSASS Access or Dump",
        "severity": "critical",
        "mitre": "T1003.001",
        "matcher": lambda e, text: "lsass.exe" in text.lower() and any(x in text.lower() for x in ("procdump", "minidump", "comsvcs", "sekurlsa")),
    },
    {
        "id": "SF-DEF-001",
        "title": "Microsoft Defender Configuration Tampering",
        "severity": "high",
        "mitre": "T1562.001",
        "matcher": lambda e, text: bool(re.search(r"Set-MpPreference.*DisableRealtimeMonitoring\s+\$?true", text, re.I)),
    },
    {
        "id": "SF-EXEC-003",
        "title": "Executable Launched from User-Writable Directory",
        "severity": "medium",
        "mitre": "T1204.002",
        "matcher": lambda e, text: bool(re.search(r"\\(?:AppData|Temp)\\[^\s\"']+\.exe\b", text, re.I)),
    },
    {
        "id": "SF-LOLBIN-001",
        "title": "Suspicious LOLBin Usage",
        "severity": "medium",
        "mitre": "T1218",
        "matcher": lambda e, text: bool(re.search(r"\b(?:certutil|bitsadmin|regsvr32|rundll32)(?:\.exe)?\b", text, re.I)),
    },
]


def _event_text(event: dict[str, Any]) -> str:
    parts = [
        event.get("process", ""),
        event.get("parent_process", ""),
        event.get("command_line", ""),
        str(event.get("raw", "")),
    ]
    return " ".join(str(x) for x in parts)


def run_detections(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for event in events:
        text = _event_text(event)
        for rule in RULES:
            try:
                matched = rule["matcher"](event, text)
            except Exception:
                matched = False
            if matched:
                findings.append({
                    "rule_id": rule["id"],
                    "title": rule["title"],
                    "severity": rule["severity"],
                    "mitre": rule["mitre"],
                    "event_id": event["id"],
                    "timestamp": event.get("timestamp", ""),
                    "process": event.get("process", ""),
                    "command_line": event.get("command_line", ""),
                })
    return findings
