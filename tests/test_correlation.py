from backend.services.correlation import build_process_tree, mitre_coverage


def test_process_tree_correlates_parent_child():
    events = [
        {"id": 1, "host": "A", "process_id": "10", "parent_process_id": "", "process": "parent.exe", "command_line": ""},
        {"id": 2, "host": "A", "process_id": "20", "parent_process_id": "10", "process": "child.exe", "command_line": ""},
    ]
    roots = build_process_tree(events)
    assert roots[0]["children"][0]["name"] == "child.exe"


def test_mitre_coverage_counts_hits():
    detections = [{"mitre": ["T1059.001"]}, {"mitre": ["T1059.001", "T1105"]}]
    coverage = mitre_coverage(detections)
    assert coverage[0] == {"technique": "T1059.001", "hits": 2}
