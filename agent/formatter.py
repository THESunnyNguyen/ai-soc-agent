from agent.workflow.state import InvestigationState


def format_report(state: InvestigationState, report_body: str) -> None:
    """Print the adaptive investigation report to stdout."""
    classification = state.alert_data.get("_classification", {})
    alert_type = classification.get("alert_type", "unknown").upper()
    severity = classification.get("severity", "unknown").upper()

    if state.recommendation == "false_positive" and state.confidence_score >= 0.8:
        status_line = "✓ LIKELY FALSE POSITIVE"
        confidence_label = f"Confidence: {state.confidence_score:.0%}"
    elif state.recommendation == "escalate" or state.confidence_score <= 0.5:
        status_line = "⚠ REVIEW REQUIRED"
        confidence_label = f"Confidence: {state.confidence_score:.0%}"
    else:
        status_line = "~ UNCERTAIN — ANALYST REVIEW NEEDED"
        confidence_label = f"Confidence: {state.confidence_score:.0%}"

    border = "─" * 60
    print(f"\n┌{border}┐")
    print(f"│ {status_line:<58} │")
    print(f"│ Alert: {state.alert_id:<52} │")
    print(f"│ Type: {alert_type:<53} │")
    print(f"│ Severity: {severity:<49} │")
    print(f"│ {confidence_label:<58} │")
    if state.escalation_tier:
        tier_line = f"Escalation: {state.escalation_tier}"
        print(f"│ {tier_line:<58} │")
    print(f"└{border}┘")

    print()
    print(report_body)

    # Guarantee the required closing line regardless of what Claude produced
    if not report_body.rstrip().endswith("→ Awaiting analyst decision."):
        print("\n→ Awaiting analyst decision.")
