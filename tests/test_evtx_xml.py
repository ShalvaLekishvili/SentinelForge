from backend.parsers.evtx_parser import xml_event_to_dict
from backend.parsers.common import normalize_event


def test_evtx_xml_record_mapping():
    xml = '''<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
      <System><EventID>1</EventID><TimeCreated SystemTime="2026-08-08T10:00:00Z"/><Channel>Microsoft-Windows-Sysmon/Operational</Channel><Computer>WS-1</Computer></System>
      <EventData><Data Name="Image">C:\\Windows\\System32\\cmd.exe</Data><Data Name="ProcessId">101</Data><Data Name="ParentProcessId">55</Data><Data Name="CommandLine">cmd.exe /c echo test</Data></EventData>
    </Event>'''
    raw = xml_event_to_dict(xml)
    event = normalize_event(raw, 0)
    assert event["event_id"] == "1"
    assert event["host"] == "WS-1"
    assert event["process_id"] == "101"
