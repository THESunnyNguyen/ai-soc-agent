# Report Formatter Spec

## Purpose
Adaptive stdout report formatted by confidence level and escalation recommendation; always awaits human analyst decision.

## Requirements

### Requirement: Adaptive report formatting
The respond step SHALL format the investigation output differently based on `InvestigationState.confidence_score` and `InvestigationState.recommendation`:

- **High confidence (≥ 0.8) + false positive**: brief summary, key exonerating evidence, minimal detail
- **Low confidence (≤ 0.5) or escalation recommended**: full detail, all indicators, complete findings
- **Mid-range (0.5–0.8)**: balanced summary with uncertainty explicitly noted

All reports SHALL end with "→ Awaiting analyst decision."

#### Scenario: High-confidence false positive report
- **WHEN** confidence_score ≥ 0.8 and recommendation is "false_positive"
- **THEN** the report is concise, leads with "✓ LIKELY FALSE POSITIVE", and shows key exonerating evidence only

#### Scenario: Low-confidence escalation report
- **WHEN** confidence_score ≤ 0.5 or recommendation is "escalate"
- **THEN** the report leads with "⚠ REVIEW REQUIRED", includes all findings and indicators, and names the recommended analyst tier

#### Scenario: All reports end with human decision prompt
- **WHEN** any report is generated
- **THEN** the final line reads "→ Awaiting analyst decision."

### Requirement: Escalation recommendation includes tier and reason
When the respond step recommends escalation, the report SHALL include the recommended analyst tier (e.g., "Tier 2 — Threat Hunter") and a one-sentence reason. The agent SHALL NOT take any escalation action autonomously.

#### Scenario: Escalation recommendation in report
- **WHEN** the agent recommends escalation
- **THEN** the report includes the tier label and reason, but no Discord action is taken

### Requirement: Report printed to stdout
The formatted report SHALL be printed to stdout. No file is written in Phase 1.

#### Scenario: Report output destination
- **WHEN** the pipeline completes
- **THEN** the report appears on stdout and nothing is written to disk
