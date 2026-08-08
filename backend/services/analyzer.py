from __future__ import annotations

import csv
import json
from datetime import datetime, timezone

from backend.parsers import normalize_event, parse_csv, parse_evtx_bytes, parse_json, parse_lines
from backend.services.correlation import build_process_tree, mitre_coverage
from backend.services.ioc import extract_iocs
from backend.services.rule_engine import run_detections
from backend.services.scoring import risk_summary


def analyze_bytes(data: bytes, suffix: str, source_name: str) -> dict:
    parser_name = "unknown"
    text_for_iocs = ""
    try:
        if suffix == ".evtx":
            raw_events = parse_evtx_bytes(data)
            parser_name = "windows-evtx"
            text_for_iocs = json.dumps(raw_events, ensure_ascii=False)
        else:
            text = data.decode("utf-8", errors="replace")
            text_for_iocs = text
            if suffix == ".json":
                raw_events = parse_json(text)
                parser_name = "json"
            elif suffix == ".csv":
                raw_events = parse_csv(text)
                parser_name = "csv"
            else:
                raw_events = parse_lines(text)
                parser_name = "line-oriented-text"
    except (json.JSONDecodeError, csv.Error, RuntimeError, ValueError) as exc:
        raise ValueError(f"Could not parse {source_name}: {exc}") from exc

    events = [normalize_event(event, index) for index, event in enumerate(raw_events)]
    detections = run_detections(events)
    return {
        "analysis_id": f"SF-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')[:-3]}",
        "source": source_name,
        "parser": parser_name,
        "event_count": len(events),
        "detection_count": len(detections),
        "risk": risk_summary(detections),
        "detections": detections,
        "iocs": extract_iocs(text_for_iocs),
        "timeline": events[:500],
        "process_tree": build_process_tree(events),
        "mitre_coverage": mitre_coverage(detections),
        "metadata": {"truncated_timeline": len(events) > 500},
    }
