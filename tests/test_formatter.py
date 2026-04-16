import io
import sys

import pytest

from agent.formatter import format_report
from agent.workflow.state import InvestigationState


def _run_format(state: InvestigationState, body: str) -> str:
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        format_report(state, body)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue()


def _make_state(**kwargs) -> InvestigationState:
    state = InvestigationState(alert_id="alert-test")
    state.alert_data["_classification"] = {"alert_type": "brute-force", "severity": "medium"}
    for k, v in kwargs.items():
        setattr(state, k, v)
    return state


# --- high-confidence false positive ---

def test_false_positive_high_confidence_shows_check_mark():
    state = _make_state(recommendation="false_positive", confidence_score=0.92)
    output = _run_format(state, "Brief summary.")
    assert "✓ LIKELY FALSE POSITIVE" in output


def test_false_positive_high_confidence_ends_with_awaiting():
    state = _make_state(recommendation="false_positive", confidence_score=0.92)
    output = _run_format(state, "Brief summary.\n→ Awaiting analyst decision.")
    assert output.rstrip().endswith("→ Awaiting analyst decision.")


# --- low confidence / escalation ---

def test_escalate_shows_warning():
    state = _make_state(
        recommendation="escalate",
        confidence_score=0.45,
        escalation_tier="Tier 2 — Incident Responder",
        escalation_reason="Lateral movement confirmed.",
    )
    output = _run_format(state, "Full detail report.")
    assert "⚠ REVIEW REQUIRED" in output
    assert "Tier 2 — Incident Responder" in output


def test_low_confidence_shows_warning():
    state = _make_state(recommendation="close", confidence_score=0.40)
    output = _run_format(state, "Uncertain report.")
    assert "⚠ REVIEW REQUIRED" in output


# --- mid-range ---

def test_mid_confidence_shows_uncertain():
    state = _make_state(recommendation="close", confidence_score=0.65)
    output = _run_format(state, "Balanced report.")
    assert "UNCERTAIN" in output or "REVIEW" in output or "FALSE POSITIVE" in output


# --- awaiting line always present ---

def test_awaiting_line_appended_if_missing():
    state = _make_state(recommendation="escalate", confidence_score=0.3)
    output = _run_format(state, "Report without closing line.")
    assert "→ Awaiting analyst decision." in output


def test_awaiting_line_not_duplicated_if_present():
    state = _make_state(recommendation="false_positive", confidence_score=0.9)
    body = "Summary.\n→ Awaiting analyst decision."
    output = _run_format(state, body)
    assert output.count("→ Awaiting analyst decision.") == 1
