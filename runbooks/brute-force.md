# Runbook: Brute Force Attack

## Overview
Investigate repeated authentication failures that may indicate a brute-force or credential stuffing attack.

## Investigation Steps

1. **Identify the source**
   - Retrieve the alert and note the source IP and targeted account
   - Enrich the source IP — check reputation score, ASN, threat feed hits
   - Check entity context for the source IP (known malicious? Tor exit node?)

2. **Assess the scope**
   - Search events for all auth failures from this source IP in the past 24 hours
   - Check if the same source IP has targeted other hosts or accounts
   - Count total attempts and unique usernames tried

3. **Determine if access was gained**
   - Search events for any successful authentication from the source IP
   - If successful auth found: treat as confirmed compromise, escalate immediately

4. **Evaluate target sensitivity**
   - Get entity context for the targeted host
   - Is the service supposed to be internet-facing?
   - Is the targeted account privileged?

5. **Check for related activity**
   - Search events for post-auth activity from the source IP (if any success)
   - Check for simultaneous alerts from the same source IP

## Assessment Criteria

| Signal | Weight |
|--------|--------|
| Source IP on threat feed | High — likely malicious |
| No successful auth | Medium — probable false positive if all failures |
| Targeted account is privileged | Raises severity |
| Service not internet-facing | Raises severity (implies bypass) |
| High attempt volume (>100) | Confirms brute-force pattern |

## Escalation Triggers
- Any successful authentication from the attacking IP
- Source IP not on any threat feed but attempt volume is very high
- Targeted account is a service account or admin

## Recommended Actions
- **Confirmed brute force, no success**: Block source IP at firewall; close alert
- **Successful auth detected**: Escalate to Tier 2 — Incident Responder immediately
- **Unclear**: Escalate to Tier 1 senior analyst for review
