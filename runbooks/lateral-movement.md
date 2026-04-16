# Runbook: Lateral Movement

## Overview
Investigate suspicious internal connections that may indicate an attacker moving through the network after initial compromise.

## Investigation Steps

1. **Identify the source host and account**
   - Retrieve the alert and note the source host, source IP, and account used
   - Get entity context for the source host — is this behaviour normal for this host?
   - Get entity context for the account — is this a service account? What are its normal hours/permissions?

2. **Map the movement pattern**
   - Search events for all connections initiated by the source host in the past hour
   - Note target hosts, protocols (RDP, SMB, WMI, SSH), and timing
   - Check if connections are sequential (host-hopping) or simultaneous (scanning)

3. **Assess account legitimacy**
   - Is the account being used at an unusual time?
   - Is the account authorized for interactive sessions (RDP) to these targets?
   - Search events for the account's last known legitimate activity

4. **Check target sensitivity**
   - Get entity context for each target host
   - Are any targets high-value (databases, domain controllers, file servers)?

5. **Look for precursor events**
   - Search events for the source host in the past 24 hours before this alert
   - Any prior auth failures, malware detections, or unusual outbound connections?

## Assessment Criteria

| Signal | Weight |
|--------|--------|
| Service account used interactively | High — abnormal behaviour |
| Activity outside normal hours | High — suspicious |
| Sequential host-hopping pattern | High — classic lateral movement |
| Targets include high-value hosts | Raises severity |
| No precursor events found | Lowers confidence |

## Escalation Triggers
- Any access to domain controllers or credential stores
- Account compromise confirmed (used outside normal hours, no legitimate reason)
- More than 3 hosts accessed in a short window

## Recommended Actions
- **Confirmed lateral movement**: Escalate to Tier 2 — Incident Responder; isolate source host
- **Suspicious but unconfirmed**: Escalate to Tier 2 for deeper investigation
- **Legitimate maintenance window**: Close as false positive with note
