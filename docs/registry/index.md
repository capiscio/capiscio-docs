---
title: Agent Registry API
description: REST API for managing agents, badges, and DIDs
---

# 📋 Agent Registry API

The CapiscIO Registry provides a REST API for managing agents, issuing badges, and resolving DIDs.

## Core Features

The registry provides:

- **Agent Management** — CRUD operations for agent records
- **Badge CA** — Issue and verify trust badges
- **DID Resolution** — Resolve `did:web` identifiers
- **Public Verification** — Check badge and agent status

---

## API Endpoints

### Public Endpoints (No Authentication)

#### DID Resolution
```http
GET /agents/{id}/did.json
```
Returns W3C DID Document for `did:web:registry.capisc.io:agents:{id}`.

#### JWKS (Public Keys)
```http
GET /.well-known/jwks.json
```
Returns CA public keys for badge verification.

#### Badge Status
```http
GET /v1/badges/{jti}/status
```
Check if a badge is revoked.

#### Agent Status
```http
GET /v1/agents/{id}/status
```
Check if an agent is disabled.

#### Revocation List
```http
GET /v1/revocations
```
Get list of revoked badge JTIs.

### Authenticated Endpoints (Clerk Auth)

#### List Your Agents
```http
GET /v1/agents
Authorization: Bearer {clerk_token}
```

#### Create Agent
```http
POST /v1/agents
Authorization: Bearer {clerk_token}
Content-Type: application/json

{
  "name": "My Agent",
  "description": "Agent description",
  "agent_card": { ... }
}
```

#### Get Agent
```http
GET /v1/agents/{id}
Authorization: Bearer {clerk_token}
```

#### Update Agent
```http
PUT /v1/agents/{id}
Authorization: Bearer {clerk_token}
```

#### Delete Agent
```http
DELETE /v1/agents/{id}
Authorization: Bearer {clerk_token}
```

#### Issue Badge
```http
POST /v1/agents/{id}/badge
Authorization: Bearer {clerk_token}
```

#### Revoke Badge
```http
POST /v1/badges/{jti}/revoke
Authorization: Bearer {clerk_token}
```

#### Create PoP Challenge (RFC-003)
```http
POST /v1/agents/{did}/badge/challenge
```

#### Submit PoP Proof (RFC-003)
```http
POST /v1/agents/{did}/badge/pop
```

---

## Enterprise Deployment

For enterprise customers, capiscio-server is available for on-premises deployment with commercial licensing.

**Features:**

- Private agent registry
- Self-managed Badge CA  
- Custom trust policies
- Air-gapped environments

Your agents get DIDs like:
```
did:web:your-company.com:agents:internal-bot
```

[:octicons-arrow-right-24: Contact Sales](mailto:sales@capisc.io){ .md-button .md-button--primary }

---

## Next Steps

<div class="grid cards" markdown>

-   :material-certificate:{ .lg .middle } **Trust Badges**

    ---

    Learn about badge issuance and verification.

    [:octicons-arrow-right-24: Trust Badges](../trust/index.md)

-   :material-api:{ .lg .middle } **Full API Docs**

    ---

    Complete REST API documentation.

    [:octicons-arrow-right-24: Server API](../reference/server/api.md)

-   :material-server:{ .lg .middle } **Enterprise Deployment**

    ---

    On-premises deployment for enterprise customers.

    [:octicons-arrow-right-24: Contact Sales](mailto:sales@capisc.io)

-   :material-web:{ .lg .middle } **DID Resolution**

    ---

    Learn about did:web identifiers.

    [:octicons-arrow-right-24: Identity](../identity/index.md)

</div>
