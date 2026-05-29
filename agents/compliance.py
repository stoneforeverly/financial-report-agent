from agents.state import ReportState

_REPLACEMENTS = [
    ("guarantee ", "indicate "),
    ("guaranteed return", "potential return"),
    ("will definitely", "may"),
    ("certain to", "may"),
    ("promise ", "suggest "),
    ("no risk", "lower risk"),
    ("risk-free", "relatively stable"),
    ("ensure profit", "aim for positive returns"),
]


def compliance_node(state: ReportState) -> ReportState:
    print("[compliance] 合规审查")
    report = state["draft_report"]

    for prohibited, replacement in _REPLACEMENTS:
        report = report.replace(prohibited, replacement)
        report = report.replace(prohibited.capitalize(), replacement.capitalize())

    print("[compliance] 审查完成")
    return {**state, "compliant_report": report}
