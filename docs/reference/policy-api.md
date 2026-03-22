---
title: Policy API Reference
description: REST API reference for the CapiscIO policy management endpoints.
---

# Policy API Reference

The policy management API provides endpoints for creating, approving, and querying YAML-based policy configurations. All endpoints are scoped to an organization.

## Authentication

Policy management endpoints require **user authentication** (via Clerk or test mode headers) and **organization membership**. Write operations (create, approve, reject) require the **admin** role.

The SDK endpoint (`/v1/sdk/policy-context`) uses **registry key** authentication (`X-Capiscio-Registry-Key` header).

## Base URL

All policy management endpoints are under:

```
/v1/orgs/{orgId}/policy
```

---

## Read Endpoints

These endpoints are accessible to any organization member.

### Get Active Org Policy

Returns the currently active org-level policy document.

```
GET /v1/orgs/{orgId}/policy/org
```

**Response** `200 OK`:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "org_id": "22222222-2222-2222-2222-222222222222",
  "scope_type": "org",
  "scope_id": "22222222-2222-2222-2222-222222222222",
  "state": "active",
  "version": 3,
  "yaml_content": "version: \"1\"\nmin_trust_level: \"DV\"\n",
  "schema_version": "1",
  "content_hash": "a1b2c3d4...",
  "created_by_user_id": "...",
  "created_by_type": "human",
  "approved_by_user_id": "...",
  "created_at": "2026-03-22T10:00:00Z",
  "updated_at": "2026-03-22T10:05:00Z"
}
```

**Response** `404 Not Found`: No active org policy exists.

### Get Org Policy History

Returns all policy documents (active, superseded, rejected) for the org scope.

```
GET /v1/orgs/{orgId}/policy/org/history
```

**Response** `200 OK`: Array of policy document objects.

### List Proposals

Returns all pending proposal documents for the organization (across all scopes).

```
GET /v1/orgs/{orgId}/policy/proposals
```

**Response** `200 OK`: Array of policy document objects with `state: "proposal"`.

### Get Resolved Policy for Agent

Returns the effective (merged) policy for a specific agent, computed by merging org → group → agent policies.

```
GET /v1/orgs/{orgId}/policy/agents/{agentId}/resolved
```

**Response** `200 OK`: Resolved policy map.

### Get Policy Lineage for Agent

Returns all active policy documents that contribute to the agent's resolved policy, in precedence order.

```
GET /v1/orgs/{orgId}/policy/agents/{agentId}/lineage
```

**Response** `200 OK`: Array of contributing policy documents with scope attribution.

---

## Write Endpoints

These endpoints require the **admin** role within the organization.

### Create Org Policy

Creates a new policy proposal for the org scope.

```
POST /v1/orgs/{orgId}/policy/org
```

**Request Body**:

```json
{
  "yaml_content": "version: \"1\"\nmin_trust_level: \"DV\"\n"
}
```

**Response** `201 Created`: The created proposal document.

**Errors**:

- `400 Bad Request`: Invalid YAML or validation failure
- `400 Bad Request`: Empty `yaml_content`

### Update Org Policy

Creates a new proposal version (same as Create). The version number auto-increments from the current active policy.

```
PUT /v1/orgs/{orgId}/policy/org
```

Same request/response format as Create.

### Approve Proposal

Approves a proposal document, activating it. The previously active document (if any) is superseded.

```
POST /v1/orgs/{orgId}/policy/proposals/{proposalId}/approve
```

**Response** `200 OK`: The now-active document.

**Errors**:

- `404 Not Found`: Proposal not found
- `400 Bad Request`: Document is not in proposal state

### Reject Proposal

Rejects a proposal document with a reason.

```
POST /v1/orgs/{orgId}/policy/proposals/{proposalId}/reject
```

**Request Body**:

```json
{
  "reason": "This policy is too permissive for production."
}
```

**Response** `200 OK`: The rejected document.

**Errors**:

- `400 Bad Request`: Reason is required

### Simulate Policy Decision

Runs a policy evaluation for a specific agent without side effects. Useful for testing policy changes before deploying.

```
POST /v1/orgs/{orgId}/policy/agents/{agentId}/simulate
```

**Request Body**:

```json
{
  "subject": {
    "did": "did:web:caller.example.com",
    "trust_level": "DV"
  },
  "action": {
    "operation": "agent.invoke"
  },
  "resource": {
    "identifier": "target-agent-id"
  },
  "context": {},
  "environment": {}
}
```

**Response** `200 OK`:

```json
{
  "decision": "ALLOW",
  "decision_id": "sim-abc123",
  "obligations": [],
  "reason": "Policy evaluation passed",
  "ttl": 300
}
```

**Errors**:

- `400 Bad Request`: PDP not configured or agent not found

---

## SDK Endpoint

### Get Policy Context

Aggregate endpoint for SDK/CLI consumption. Returns the complete policy context for the organization.

```
GET /v1/sdk/policy-context
```

**Authentication**: Registry key (`X-Capiscio-Registry-Key` header).

**Response** `200 OK`:

```json
{
  "org_id": "22222222-2222-2222-2222-222222222222",
  "agents": [
    {
      "id": "...",
      "name": "my-agent",
      "did": "did:web:my-agent.example.com",
      "trust_level": "DV",
      "group_ids": ["group-1-id"]
    }
  ],
  "groups": [
    {
      "id": "group-1-id",
      "name": "production",
      "precedence": 10
    }
  ],
  "active_policies": [
    {
      "id": "...",
      "scope_type": "org",
      "version": 3,
      "yaml_content": "..."
    }
  ],
  "pending_proposals": []
}
```

---

## Policy Document States

| State | Description |
|-------|-------------|
| `proposal` | Awaiting review and approval |
| `active` | Currently enforced policy |
| `superseded` | Replaced by a newer active policy |
| `rejected` | Rejected during review |
| `archived` | Manually archived |
