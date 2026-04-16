# Data Spec

## Generators
- `cloudtrail.py` — synthetic CloudTrail logs
- `sysmon.py` — synthetic Sysmon events
- `auth.py` — synthetic auth events

## Samples
- `data/samples/logs/` — static seed logs for dev/test
- `data/samples/alerts/` — static seed alerts

## Schema
- `data/schema/alert.json` — canonical alert shape
- `data/schema/migrations/` — postgres migration files

## Runbooks
- `runbooks/brute_force.md`
- `runbooks/privilege_escalation.md`
- `runbooks/lateral_movement.md`
- `runbooks/data_exfiltration.md`