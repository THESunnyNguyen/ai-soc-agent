# Discord Bot Spec

## Purpose
User-facing interface. Triggers investigations and displays results.

## Commands
- `/investigate <alert_id>` — triggers agent pipeline for the given alert
- `/status` — shows current investigation queue / results

## Formatters
- `formatters/` — converts agent output structs into Discord embeds

## Requirements
- MUST be independently containerizable
- MUST post formatted embeds (not raw text) for investigation results