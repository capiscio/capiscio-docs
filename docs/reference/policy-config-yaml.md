---
title: Policy Config YAML Reference
description: Complete reference for the capiscio-policy.yaml schema.
---

# Policy Config YAML Reference

This page documents the complete YAML schema for CapiscIO policy configuration files.

## Schema Version

Current schema version: **1**

## Top-Level Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `version` | string | **Yes** | — | Must be `"1"` |
| `min_trust_level` | string | No | `""` | Minimum trust level for all requests |
| `allowed_dids` | string[] | No | `[]` | Allowlist of agent DIDs |
| `denied_dids` | string[] | No | `[]` | Denylist of agent DIDs |
| `rate_limits` | RateLimitRule[] | No | `[]` | Per-DID rate limits |
| `operations` | OperationRule[] | No | `[]` | Operation-scoped rules |
| `mcp_tools` | MCPToolRule[] | No | `[]` | MCP tool-scoped rules |

## Trust Levels

| Value | Name | Description |
|-------|------|-------------|
| `""` | None | No trust requirement |
| `SS` | Self-Signed | Agent has a self-signed key |
| `REG` | Registered | Agent is registered in the CapiscIO registry |
| `DV` | Domain Validated | Agent's domain ownership is verified |
| `OV` | Organization Validated | Agent's organization is verified |
| `EV` | Extended Validation | Agent has undergone extended validation |

Trust levels are ordered: `EV > OV > DV > REG > SS > ""` (none).

## DID Format

All DID values must conform to the DID syntax: they must start with `did:`.

Examples:

- `did:web:agent.example.com`
- `did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK`
- `did:web:registry.capisc.io:agents:my-agent`

## RateLimitRule

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `did` | string | **Yes** | Agent DID to rate limit (must start with `did:`) |
| `rpm` | integer | **Yes** | Requests per minute (must be > 0) |

```yaml
rate_limits:
  - did: "did:web:caller.example.com"
    rpm: 100
```

Rate limits generate **obligations** in policy decisions. The PEP (Policy Enforcement Point) is responsible for tracking and enforcing rate limits.

## OperationRule

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pattern` | string | **Yes** | Operation pattern to match (must not be empty) |
| `min_trust_level` | string | No | Trust level override for this operation |
| `allowed_dids` | string[] | No | Allowlist specific to this operation |
| `denied_dids` | string[] | No | Denylist specific to this operation |

```yaml
operations:
  - pattern: "payment.*"
    min_trust_level: "EV"
    allowed_dids:
      - "did:web:payment-processor.example.com"
```

The `pattern` field is matched against `input.action.operation` during policy evaluation.

## MCPToolRule

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tool` | string | **Yes** | MCP tool name to match (must not be empty) |
| `min_trust_level` | string | No | Trust level override for this tool |
| `allowed_dids` | string[] | No | Allowlist specific to this tool |
| `denied_dids` | string[] | No | Denylist specific to this tool |

```yaml
mcp_tools:
  - tool: "database_query"
    min_trust_level: "OV"
  - tool: "send_email"
    min_trust_level: "EV"
    allowed_dids:
      - "did:web:notification-service.example.com"
```

The `tool` field is matched against `input.action.mcp_tool` during policy evaluation.

## Validation Rules

The following rules are enforced during parsing and validation:

1. **`version`** must be exactly `"1"`
2. **Trust levels** must be one of: `""`, `SS`, `REG`, `DV`, `OV`, `EV`
3. **DID format**: All DID strings must start with `did:`
4. **No duplicate DIDs** within the same list
5. **No cross-listed DIDs**: A DID cannot appear in both `allowed_dids` and `denied_dids`
6. **Rate limit RPM** must be a positive integer
7. **Operation patterns** must not be empty strings
8. **MCP tool names** must not be empty strings

## Minimal Valid Config

```yaml
version: "1"
min_trust_level: ""
```

## Full Example

```yaml
version: "1"
min_trust_level: "DV"

allowed_dids:
  - "did:web:trusted-partner.example.com"

denied_dids:
  - "did:web:blocked-agent.example.com"

rate_limits:
  - did: "did:web:trusted-partner.example.com"
    rpm: 1000

operations:
  - pattern: "payment.*"
    min_trust_level: "EV"
    allowed_dids:
      - "did:web:payment-processor.example.com"
  - pattern: "admin.*"
    min_trust_level: "OV"

mcp_tools:
  - tool: "database_query"
    min_trust_level: "OV"
  - tool: "send_email"
    min_trust_level: "EV"
```
