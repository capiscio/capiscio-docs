# capiscio-server Reference

<!-- 
  Source: capiscio-server/internal/api/, capiscio-server/docs/swagger.json
-->

The **capiscio-server** is a commercial backend API server that powers the CapiscIO Registry. It provides agent management, badge issuance (CA-signed), and trust verification services.

!!! info "Enterprise Product"
    capiscio-server is a commercial product available to enterprise customers. [Contact Sales](mailto:sales@capisc.io) for licensing options.

!!! info "Version"
    Current version: **v2.5.0**

## Overview

capiscio-server provides:

- **Agent Registry** — CRUD operations for agent records
- **Badge CA** — Certificate Authority for issuing trust badges (levels 1-4)
- **JWKS Endpoint** — Public key set for badge verification
- **DID Resolution** — `did:web` document serving for registered agents
- **API Key Auth** — Secure API access management

## Quick Links

<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Full OpenAPI documentation with all endpoints.

    [:octicons-arrow-right-24: OpenAPI Spec](api.md)

-   :material-docker:{ .lg .middle } **Deployment**

    ---

    Docker and self-hosted deployment guides.

    [:octicons-arrow-right-24: Deployment Guide](deployment.md)

-   :material-badge-account:{ .lg .middle } **Badge Issuance**

    ---

    How the CA issues trust badges.

    [:octicons-arrow-right-24: Badge CA](badge-ca.md)

</div>

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      capiscio-server                            │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│   API       │   Badge CA  │   Database  │   JWKS              │
│   Handlers  │   Service   │   (Postgres)│   Endpoint          │
├─────────────┼─────────────┼─────────────┼─────────────────────┤
│ /v1/agents  │ Issue badge │ agents      │ /.well-known/       │
│ /v1/validate│ Verify      │ badges      │   jwks.json         │
│ /v1/api-keys│ Auth        │ api_keys    │                     │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
```

---

## API Endpoints Summary

### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/agents` | List all agents |
| `POST` | `/v1/agents` | Create new agent |
| `GET` | `/v1/agents/{id}` | Get agent details |
| `PUT` | `/v1/agents/{id}` | Update agent |
| `DELETE` | `/v1/agents/{id}` | Delete agent |
| `POST` | `/v1/agents/{id}/disable` | Disable agent |
| `POST` | `/v1/agents/{id}/enable` | Enable agent |

### Badges

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/agents/{id}/badge` | Issue badge for agent |
| `POST` | `/v1/validate` | Verify a badge token |
| `GET` | `/.well-known/jwks.json` | Get CA public keys (JWKS) |

### DID Resolution

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/agents/{id}/did.json` | Get agent's DID document |

### API Keys

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/api-keys` | List API keys |
| `POST` | `/v1/api-keys` | Create new API key |
| `DELETE` | `/v1/api-keys/{id}` | Delete API key |

---

## Authentication

capiscio-server supports two authentication methods:

### API Key Authentication

For programmatic access (agents, CI/CD), use the `X-Capiscio-Registry-Key` header:

```bash
curl -X POST https://registry.capisc.io/v1/agents/{id}/badge \
  -H "X-Capiscio-Registry-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "my-agent.example.com", "trustLevel": "2"}'
```

!!! note "Header Name"
    Use `X-Capiscio-Registry-Key` for API key authentication, not `Authorization: Bearer`. The `X-Capiscio-Badge` header is used for agent-to-agent badge transport (RFC-002 §9.1).

### Clerk Authentication

For the web dashboard (capiscio-ui), authentication is handled via [Clerk](https://clerk.dev).

---

## Trust Levels

The server issues badges at trust levels 1-4 (Level 0 is self-signed, not CA-issued):

| Level | Code | Validation Required |
|-------|------|---------------------|
| 1 | `REG` | Account registration |
| 2 | `DV` | Domain verification (DNS TXT) |
| 3 | `OV` | Organization verification |
| 4 | `EV` | Manual security audit |

Trust level is specified in badge requests:

```json
{
  "domain": "my-agent.example.com",
  "trustLevel": "2"
}
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `ENVIRONMENT` | No | `development` | Runtime environment |
| `PORT` | No | `8080` | Server port |
| `CA_KEY_PATH` | No | — | Path to CA private key (generates if missing) |
| `CA_ISSUER_URL` | No | — | Issuer URL for badges |
| `CLERK_SECRET_KEY` | Yes* | — | Clerk API secret (*for dashboard auth) |
| `CLERK_WEBHOOK_SECRET` | Yes* | — | Clerk webhook secret (*for user sync) |

---

## Quick Start

### Local Development

!!! note "Enterprise License Required"
    The CapiscIO server is distributed as a **closed-source binary** (or Docker container) to licensed enterprise customers. [Contact Sales](mailto:sales@capisc.io) for access.

```bash
# Option 1: Docker (recommended)
docker run -d -p 8080:8080 \
  -e DATABASE_URL=postgres://user:pass@localhost/capiscio \
  registry.capisc.io/capiscio-server:latest

# Option 2: Binary
./capiscio-server
```

The server starts at `http://localhost:8080`.

### View API Docs

- **Swagger UI**: http://localhost:8080/swagger/index.html
- **OpenAPI Spec**: http://localhost:8080/swagger/doc.json

---

## See Also

- [API Reference](api.md) — Full endpoint documentation
- [Deployment Guide](deployment.md) — Production deployment
- [Badge CA](badge-ca.md) — Certificate Authority operations
- [RFC-002: Trust Badge](https://docs.capisc.io/rfcs/blob/main/docs/002-trust-badge.md) — Badge specification
