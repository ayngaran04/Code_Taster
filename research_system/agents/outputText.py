from research_system.core.state import ReviewState
from collections import defaultdict
from datetime import datetime

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}

def run_synthesizer_agent(state: ReviewState) -> ReviewState:
    all_findings = (
        state["security_findings"] +
        state["architecture_findings"] +
        state["code_quality_findings"]
    )

    all_findings.sort(key=lambda f: SEVERITY_ORDER.get(f["severity"], 99))

    by_file = defaultdict(list)
    for finding in all_findings:
        by_file[finding["file"]].append(finding)

    severity_counts = defaultdict(int)
    for f in all_findings:
        severity_counts[f["severity"]] += 1

    report = {
        "meta": {
            "scanned_at": datetime.now().isoformat(),
            "target": state["target_directory"],
            "total_files_scanned": len(state["files"]),
            "total_findings": len(all_findings),
        },
        "summary": {
            "critical": severity_counts.get("critical", 0),
            "high": severity_counts.get("high", 0),
            "medium": severity_counts.get("medium", 0),
            "low": severity_counts.get("low", 0),
            "info": severity_counts.get("info", 0),
        },
        "findings_by_severity": all_findings,
        "findings_by_file": dict(by_file),
        "scan_errors": state["errors"],
    }

    return {"final_report": report}