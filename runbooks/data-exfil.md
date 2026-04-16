# Runbook: Data Exfiltration

## Overview
Investigate large or unusual outbound data transfers that may indicate data theft.

## Investigation Steps

1. **Identify the transfer**
   - Retrieve the alert: source host, source user, destination IP, volume, protocol, timing
   - Enrich the destination IP — reputation, ASN, known categories
   - Check entity context for the source host and user

2. **Assess the destination**
   - Is the destination IP in any allowlist or known business service?
   - Enrich the destination IP for threat intelligence
   - Is the destination a cloud storage provider, personal service, or unknown host?

3. **Assess the user's authorization**
   - Get entity context for the user — what is their role and normal data access?
   - Are there any approved data transfer tasks for this user?
   - What data was accessed before the transfer? (search events for file access)

4. **Examine the data accessed**
   - Search events for file access activity from the same host in the hour before the transfer
   - What directories and file types were accessed? Do they match the user's role?
   - Was access volume abnormal?

5. **Look for related indicators**
   - Search events for other outbound transfers from the same host or user this week
   - Any prior DLP alerts, policy violations, or anomalies for this user?
   - Was the transfer compressed or encrypted in an unusual way?

## Assessment Criteria

| Signal | Weight |
|--------|--------|
| Destination on threat feed | High — likely malicious exfiltration |
| Transfer volume >> normal for user | High — suspicious |
| File access pattern matches user role | Lowers suspicion |
| Transfer to unknown external IP | Medium — warrants investigation |
| No prior DLP alerts for user | Lowers confidence in malice |
| Transfer during business hours | Slightly lowers suspicion |

## Escalation Triggers
- Destination IP on threat feed
- User accessed sensitive directories (finance, HR, IP) immediately before transfer
- Transfer volume exceeds 1GB with no business justification
- Transfer outside business hours

## Recommended Actions
- **Confirmed exfiltration**: Escalate to Tier 2 — Incident Responder; preserve evidence, do not alert user
- **Suspicious but unclear intent**: Escalate to Tier 2 for user interview and deeper review
- **Authorized transfer confirmed**: Close as false positive with note
