# Infra Spec

## Local
- `docker-compose.yml` — full local stack
- `docker-compose.dev.yml` — hot reload + debug ports

## Kubernetes (Phase 5+)
- `infra/k8s/namespace.yaml`
- `infra/k8s/mcp-server/` — deployment + service
- `infra/k8s/agent/`
- `infra/k8s/discord-bot/`
- `infra/k8s/postgres/`

## CI/CD (Phase 7)
- `.github/workflows/ci.yml` — lint, test, build on PR
- `.github/workflows/deploy.yml` — push to OCI registry + rollout