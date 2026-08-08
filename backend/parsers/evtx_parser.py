from __future__ import annotations

import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


def _strip_namespace(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def xml_event_to_dict(xml_text: str) -> dict[str, Any]:
    root = ET.fromstring(xml_text)
    result: dict[str, Any] = {"win": {"system": {}, "eventdata": {}}}
    system = result["win"]["system"]
    eventdata = result["win"]["eventdata"]

    for child in root.iter():
        name = _strip_namespace(child.tag)
        if name == "EventID" and child.text:
            system["eventID"] = child.text
        elif name == "Channel" and child.text:
            system["channel"] = child.text
        elif name == "Computer" and child.text:
            system["computer"] = child.text
        elif name == "TimeCreated":
            system["systemTime"] = child.attrib.get("SystemTime", "")
        elif name == "Data":
            key = child.attrib.get("Name")
            if key:
                normalized_key = key[0].lower() + key[1:]
                eventdata[normalized_key] = child.text or ""
    return result


def parse_evtx_bytes(data: bytes) -> list[dict[str, Any]]:
    try:
        from Evtx.Evtx import Evtx  # type: ignore
    except ImportError as exc:
        raise RuntimeError("EVTX support requires the python-evtx package.") from exc

    records: list[dict[str, Any]] = []
    with tempfile.NamedTemporaryFile(suffix=".evtx", delete=False) as handle:
        handle.write(data)
        temp_path = Path(handle.name)

    try:
        with Evtx(str(temp_path)) as log:
            for record in log.records():
                records.append(xml_event_to_dict(record.xml()))
    finally:
        temp_path.unlink(missing_ok=True)
    return records
