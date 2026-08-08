from __future__ import annotations

from collections import Counter


def build_process_tree(events: list[dict]) -> list[dict]:
    processes: dict[tuple[str, str], dict] = {}
    for event in events:
        pid = str(event.get("process_id", "")).strip()
        if not pid:
            continue
        host = event.get("host", "")
        key = (host, pid)
        processes.setdefault(key, {
            "host": host,
            "pid": pid,
            "name": event.get("process", ""),
            "parent_pid": str(event.get("parent_process_id", "")),
            "parent_name": event.get("parent_process", ""),
            "command_line": event.get("command_line", ""),
            "event_ids": [],
            "children": [],
        })
        processes[key]["event_ids"].append(event.get("id"))

    roots: list[dict] = []
    for key, node in processes.items():
        parent_key = (node["host"], node["parent_pid"])
        if node["parent_pid"] and parent_key in processes and parent_key != key:
            processes[parent_key]["children"].append(node)
        else:
            roots.append(node)
    return roots


def mitre_coverage(detections: list[dict]) -> list[dict]:
    counter: Counter[str] = Counter()
    for detection in detections:
        counter.update(detection.get("mitre", []))
    return [{"technique": technique, "hits": hits} for technique, hits in counter.most_common()]
