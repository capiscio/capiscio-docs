# API Reference

<!-- 
  VERIFIED: 2025-12-11
  Source: capiscio-server/docs/swagger.json
-->

Complete API reference for capiscio-server. Interactive documentation is available at `/swagger/index.html` when the server is running.

!!! tip "Interactive Docs"
    For the best experience, use the [Swagger UI](http://localhost:8080/swagger/index.html) when running locally.

---

## Base URL

| Environment | URL |
|-------------|-----|
| Production | `https://registry.capisc.io` |
| Local | `http://localhost:8080` |

---

## API Route Architecture

The server provides three distinct route groups with different authentication patterns:

| Path Pattern | Auth Method | Purpose | Consumers |
|--------------|-------------|---------|-----------|
| `/v1/*` | Clerk JWT | Dashboard/UI operations | Web dashboard |
| `/v1/sdk/*` | Registry API Key | Programmatic access | CLI, SDK, CI/CD |
| `/v1/agents/{did}/badge/*` | Registry Key OR Badge | Badge minting (RFC-003) | Agents |
| No auth | None | Public verification | Anyone |

!!! note "Dual-Path Pattern"
    Many endpoints exist under both `/v1/*` (Clerk auth) and `/v1/sdk/*` (API key auth) to support both interactive and programmatic workflows. For SDK/CLI integration, always use the `/v1/sdk/*` routes.

### Route Groups Summary

```
Public (no auth):
├── /.well-known/jwks.json         # CA public keys
├── /agents/{id}/did.json          # Agent DID documents
├── /servers/{id}/did.json         # MCP Server DID documents
├── /v1/badges/{jti}/status        # Badge revocation status
├── /v1/agents/{id}/status         # Agent status
├── /v1/servers/{id}/status        # MCP Server status
├── /v1/validate                   # Badge validation
└── /v1/badges/mint                # DV badge minting (grant + PoP auth)

SDK/CLI Routes (X-Capiscio-Registry-Key):
├── /v1/sdk/agents                 # CRUD agents
├── /v1/sdk/agents/{did}/badge/*   # PoP badge flow (RFC-003)
├── /v1/sdk/servers                # CRUD MCP servers (RFC-007)
└── /v1/badges/dv/*                # Domain Validation flow

Dashboard Routes (Clerk JWT):
├── /v1/agents                     # CRUD agents
├── /v1/servers                    # CRUD MCP servers
├── /v1/orgs                       # Organization management
├── /v1/api-keys                   # API key management
├── /v1/events                     # Event logs
└── /v1/metrics/*                  # Dashboard metrics
```

---

## Authentication

Authentication varies by endpoint type:

### User Dashboard Routes (`/v1/*`)

For dashboard/UI operations (creating agents, managing API keys), use Clerk JWT:

```
Authorization: Bearer YOUR_CLERK_JWT
```

### SDK/CLI Routes (`/v1/sdk/*`)

For programmatic access from CLI, SDK, or CI/CD pipelines, use Registry API Key:

```
X-Capiscio-Registry-Key: YOUR_API_KEY
```

### Agent Operations (Badge Minting)

For badge minting operations, you can use either Registry API Key OR a valid Trust Badge:

```
X-Capiscio-Registry-Key: YOUR_API_KEY
# OR
X-Capiscio-Badge: YOUR_BADGE_JWT
```

### Public Endpoints

These endpoints do not require authentication:
- JWKS (`/.well-known/jwks.json`)
- Badge validation (`/v1/validate`)
- DID resolution (`/agents/{id}/did.json`, `/servers/{id}/did.json`)
- Badge/Agent/Server status (`/v1/badges/{jti}/status`, `/v1/agents/{id}/status`, `/v1/servers/{id}/status`)

---

## Agents

### List Agents

Retrieve all agents for the authenticated user.

```http
GET /v1/agents
```

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "My Agent",
      "domain": "my-agent.example.com",
      "status": "enabled",
      "trustLevel": "2",
      "createdAt": "2025-01-15T10:30:00Z",
      "updatedAt": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Create Agent

Register a new agent.

```http
POST /v1/agents
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "My Agent",
  "domain": "my-agent.example.com",
  "description": "Production agent for task processing"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Agent",
    "domain": "my-agent.example.com",
    "status": "enabled",
    "createdAt": "2025-01-15T10:30:00Z"
  },
  "message": "Agent created successfully"
}
```

### Get Agent

Retrieve a specific agent by ID.

```http
GET /v1/agents/{id}
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `id` | path | Agent UUID |

### Update Agent

Update an existing agent.

```http
PUT /v1/agents/{id}
Content-Type: application/json
```

### Delete Agent

Delete an agent.

```http
DELETE /v1/agents/{id}
```

### Disable Agent

Disable an agent (prevents badge issuance).

```http
POST /v1/agents/{id}/disable
```

### Enable Agent

Re-enable a disabled agent.

```http
POST /v1/agents/{id}/enable
```

---

## Badges

### Issue Badge

Issue a new trust badge for an agent. The badge is signed by the CapiscIO CA.

```http
POST /v1/agents/{id}/badge
Content-Type: application/json
```

**Request Body:**

```json
{
  "domain": "my-agent.example.com",
  "trustLevel": "2"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `domain` | string | Yes | Agent's verified domain |
| `trustLevel` | string | No | Trust level: "1", "2", "3", or "4" (default: "1") |
| `audience` | string[] | No | Allowed verifier URLs |
| `ttl` | int | No | Badge TTL in seconds (default: 300) |

**Response:**

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
    "jti": "badge-uuid-here",
    "subject": "did:web:registry.capisc.io:agents:550e8400-e29b-41d4-a716-446655440000",
    "trustLevel": "2",
    "expiresAt": "2025-01-15T10:35:00Z"
  }
}
```

**Error Responses:**

| Status | Description |
|--------|-------------|
| 400 | Invalid request (missing domain, invalid trust level) |
| 403 | Agent is disabled |
| 404 | Agent not found |

### Validate Badge

Validate a trust badge token. This endpoint is **public** (no auth required).

```http
POST /v1/validate
Content-Type: application/json
```

**Request Body:**

```json
{
  "token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "valid": true,
    "claims": {
      "iss": "https://registry.capisc.io",
      "sub": "did:web:registry.capisc.io:agents:550e8400",
      "exp": 1705316100,
      "iat": 1705315800,
      "vc": {
        "credentialSubject": {
          "domain": "my-agent.example.com",
          "level": "2"
        }
      }
    }
  }
}
```

### Get JWKS

Get the CA's public key set for badge verification. This endpoint is public.

```http
GET /.well-known/jwks.json
```

**Response:**

```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "base64url-encoded-public-key",
      "kid": "capiscio-ca-1705315800",
      "alg": "EdDSA",
      "use": "sig"
    }
  ]
}
```

---

## DID Resolution

### Get DID Document

Retrieve the W3C DID Document for an agent. Used for `did:web` resolution.

```http
GET /agents/{id}/did.json
```

**Response:**

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "id": "did:web:registry.capisc.io:agents:550e8400",
  "verificationMethod": [
    {
      "id": "did:web:registry.capisc.io:agents:550e8400#key-1",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:web:registry.capisc.io:agents:550e8400",
      "publicKeyMultibase": "z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
    }
  ],
  "authentication": [
    "did:web:registry.capisc.io:agents:550e8400#key-1"
  ],
  "assertionMethod": [
    "did:web:registry.capisc.io:agents:550e8400#key-1"
  ]
}
```

---

## API Keys

### List API Keys

List all API keys for the authenticated user.

```http
GET /v1/api-keys
```

### Create API Key

Create a new API key.

```http
POST /v1/api-keys
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Production Key"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "key-uuid",
    "name": "Production Key",
    "key": "cpsc_live_abc123...",
    "createdAt": "2025-01-15T10:30:00Z"
  },
  "message": "API key created. Save it now - it won't be shown again."
}
```

!!! warning "Save Your Key"
    The full API key is only shown once at creation time. Store it securely.

### Delete API Key

Delete an API key.

```http
DELETE /v1/api-keys/{id}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message here"
}
```

| Status | Description |
|--------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid API key |
| 403 | Forbidden - Action not allowed |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

API requests are rate-limited:

| Endpoint | Limit |
|----------|-------|
| Badge issuance | 100/min per agent |
| Other endpoints | 1000/min per API key |

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705315860
```

---

## OpenAPI Specification

The full OpenAPI 2.0 (Swagger) specification is available at:

- **JSON**: `/swagger/doc.json`
- **Interactive UI**: `/swagger/index.html`

Download the spec:

```bash
curl https://registry.capisc.io/swagger/doc.json -o openapi.json
```
