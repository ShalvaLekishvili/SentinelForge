from __future__ import annotations

from typing import Any


def _deep_get(data: dict[str, Any], *paths: str) -> Any:
    for path in paths:
        current: Any = data
        ok = True
        for part in path.split("."):
            if not isinstance(current, dict) or part not in current:
                ok = False
                break
            current = current[part]
        if ok and current not in (None, ""):
            return current
    return ""


def normalize_event(raw: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "id": index + 1,
        "timestamp": str(_deep_get(raw, "timestamp", "@timestamp", "time", "EventTime", "event_time", "win.system.systemTime")),
        "host": str(_deep_get(raw, "host", "computer", "Computer", "agent.name", "win.system.computer")),
        "user": str(_deep_get(raw, "user", "User", "username", "win.eventdata.user", "win.eventdata.targetUserName")),
        "event_id": str(_deep_get(raw, "event_id", "EventID", "win.system.eventID", "win.system.eventId")),
        "channel": str(_deep_get(raw, "channel", "Channel", "win.system.channel")),
        "process": str(_deep_get(raw, "process", "process_name", "Image", "image", "win.eventdata.image", "win.eventdata.newProcessName")),
        "process_id": str(_deep_get(raw, "process_id", "ProcessId", "ProcessID", "win.eventdata.processId", "win.eventdata.newProcessId")),
        "parent_process": str(_deep_get(raw, "parent_process", "ParentImage", "parent", "win.eventdata.parentImage", "win.eventdata.parentProcessName")),
        "parent_process_id": str(_deep_get(raw, "parent_process_id", "ParentProcessId", "ParentProcessID", "win.eventdata.parentProcessId")),
        "command_line": str(_deep_get(raw, "command_line", "CommandLine", "message", "Message", "win.eventdata.commandLine")),
        "destination_ip": str(_deep_get(raw, "destination_ip", "DestinationIp", "dst_ip", "win.eventdata.destinationIp")),
        "destination_port": str(_deep_get(raw, "destination_port", "DestinationPort", "dst_port", "win.eventdata.destinationPort")),
        "raw": raw,
    }
