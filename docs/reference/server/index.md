# capiscio-server Reference

The **capiscio-server** is a commercial backend API server that powers the CapiscIO Registry. It provides agent management, badge issuance (CA-signed), and trust verification services.

!!! info "Enterprise Product"
    capiscio-server is a commercial product available to enterprise customers. [Contact Sales](mailto:sales@capisc.io) for licensing options.

!!! info "Version"
    Current version: **v{{ capiscio_version }}**

## Overview

capiscio-server provides:

- **Agent Registry** — CRUD operations for agent records
- **Badge CA** — Certificate Authority for issuing trust badges (levels 1-4)
- **Embedded PDP** — In-process OPA policy evaluator with auto-built bundles
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

!!! note "Dual-Path Architecture"
    capiscio-server has **two** endpoint groups for agent management — SDK routes (for programmatic access) and Dashboard routes (for the web UI). See [API Reference](api.md) for full details.

### SDK/CLI Routes (`X-Capiscio-Registry-Key`)

Use these routes from the CLI, Python SDK, or CI/CD pipelines:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/sdk/agents` | List agents |
| `POST` | `/v1/sdk/agents` | Create agent |
| `GET` | `/v1/sdk/agents/{id}` | Get agent details |
| `PUT` | `/v1/sdk/agents/{id}` | Update agent |
| `POST` | `/v1/sdk/agents/{did}/badge/challenge` | PoP challenge (RFC-003) |
| `POST` | `/v1/sdk/agents/{did}/badge/pop` | PoP badge issuance |
| `GET` | `/v1/sdk/servers` | List MCP servers (RFC-007) |
| `POST` | `/v1/sdk/servers` | Register MCP server |

### Dashboard Routes (Clerk JWT)

Used by the capiscio-ui web dashboard only:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/agents` | List all agents |
| `POST` | `/v1/agents` | Create new agent |
| `POST` | `/v1/agents/{id}/badge` | Issue IAL-0 badge |
| `POST` | `/v1/agents/{id}/disable` | Disable agent |
| `GET` | `/v1/api-keys` | List API keys |
| `POST` | `/v1/api-keys` | Create new API key |
| `DELETE` | `/v1/api-keys/{id}` | Delete API key |

### Public Endpoints (No Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/validate` | Verify a badge token |
| `GET` | `/.well-known/jwks.json` | Get CA public keys (JWKS) |
| `GET` | `/agents/{id}/did.json` | Get agent's DID document |
| `GET` | `/servers/{id}/did.json` | Get MCP server's DID document |
| `GET` | `/v1/badges/{jti}/status` | Badge revocation status |
| `GET` | `/v1/agents/{id}/status` | Agent status |

---

## Authentication

capiscio-server supports two authentication methods depending on the route group:

### API Key Authentication (SDK/CLI Routes)

For programmatic access via `/v1/sdk/*` endpoints, use the `X-Capiscio-Registry-Key` header:

```bash
curl -X POST https://registry.capisc.io/v1/sdk/agents \
  -H "X-Capiscio-Registry-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "domain": "my-agent.example.com"}'
```

!!! note "Header Name"
    Use `X-Capiscio-Registry-Key` for API key authentication, not `Authorization: Bearer`. The `X-Capiscio-Badge` header is used for agent-to-agent badge transport (RFC-002 §9.1).

### Clerk Authentication (Dashboard Routes)

For the web dashboard (capiscio-ui), authentication is handled via [Clerk](https://clerk.dev). Dashboard routes at `/v1/agents`, `/v1/api-keys`, etc. use Clerk JWTs.

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
- [RFC-002: Trust Badge](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/002-trust-badge.md) — Badge specification
