from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.services.detector import run_detections
from backend.services.ioc import extract_iocs
from backend.services.scoring import risk_summary


def _normalize_event(raw: dict[str, Any], index: int) -> dict[str, Any]:
    timestamp = (
        raw.get("timestamp")
        or raw.get("@timestamp")
        or raw.get("time")
        or raw.get("EventTime")
        or raw.get("event_time")
        or ""
    )
    process = raw.get("process") or raw.get("process_name") or raw.get("Image") or raw.get("image") or ""
    command = raw.get("command_line") or raw.get("CommandLine") or raw.get("message") or raw.get("Message") or ""
    parent = raw.get("parent_process") or raw.get("ParentImage") or raw.get("parent") or ""
    user = raw.get("user") or raw.get("User") or raw.get("username") or ""
    host = raw.get("host") or raw.get("computer") or raw.get("Computer") or raw.get("agent", {}).get("name", "") if isinstance(raw.get("agent"), dict) else raw.get("host", "")
    event_id = raw.get("event_id") or raw.get("EventID") or raw.get("win", {}).get("system", {}).get("eventID", "") if isinstance(raw.get("win"), dict) else raw.get("event_id", "")

    return {
        "id": index + 1,
        "timestamp": str(timestamp),
        "host": str(host),
        "user": str(user),
        "event_id": str(event_id),
        "process": str(process),
        "parent_process": str(parent),
        "command_line": str(command),
        "raw": raw,
    }


def _parse_json(text: str) -> list[dict[str, Any]]:
    payload = json.loads(text)
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("events", "data", "alerts", "hits"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
        return [payload]
    return []


def _parse_csv(text: str) -> list[dict[str, Any]]:
    return list(csv.DictReader(io.StringIO(text)))


def _parse_lines(text: str) -> list[dict[str, Any]]:
    events = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            events.append({"message": line})
    return events


def analyze_bytes(data: bytes, suffix: str, source_name: str) -> dict[str, Any]:
    text = data.decode("utf-8", errors="replace")
    try:
        if suffix == ".json":
            raw_events = _parse_json(text)
        elif suffix == ".csv":
            raw_events = _parse_csv(text)
        else:
            raw_events = _parse_lines(text)
    except (json.JSONDecodeError, csv.Error) as exc:
        raise ValueError(f"Could not parse {source_name}: {exc}") from exc

    events = [_normalize_event(event, i) for i, event in enumerate(raw_events)]
    detections = run_detections(events)
    iocs = extract_iocs(text)
    risk = risk_summary(detections)

    return {
        "analysis_id": f"SF-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "source": source_name,
        "event_count": len(events),
        "detection_count": len(detections),
        "risk": risk,
        "detections": detections,
        "iocs": iocs,
        "timeline": events[:100],
    }
