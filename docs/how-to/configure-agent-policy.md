---
title: Configure Agent Policy
description: How to write and deploy YAML-based policy configurations for your CapiscIO agents.
---

# Configure Agent Policy

This guide walks you through writing, validating, and deploying YAML policy configurations. Policy configs define trust requirements, access rules, and rate limits for your agents.

## Quick Start

### 1. Create a Policy Config File

Create a file named `capiscio-policy.yaml` in your project root:

```yaml
version: "1"
min_trust_level: "DV"
denied_dids:
  - "did:web:known-bad-actor.example.com"
```

### 2. Validate Locally

```bash
capiscio policy validate -f capiscio-policy.yaml
```

### 3. Deploy to Your Organization

Use the dashboard UI or the CLI to create and approve a policy:

```bash
# View current policy context
capiscio policy context --registry https://api.capisc.io --api-key $CAPISCIO_API_KEY
```

## YAML Schema

### Version

Every policy config must specify `version: "1"`. This is the current and only supported version.

```yaml
version: "1"
```

### Minimum Trust Level

Set a baseline trust requirement for all incoming agent requests:

```yaml
min_trust_level: "DV"  # Require domain validation or higher
```

Valid values: `""` (none), `SS`, `REG`, `DV`, `OV`, `EV`

### DID Access Lists

Control which agents can interact with your agents by DID:

```yaml
# Only these agents may call your agents
allowed_dids:
  - "did:web:partner-a.example.com"
  - "did:web:partner-b.example.com"

# These agents are always blocked
denied_dids:
  - "did:web:known-bad-actor.example.com"
```

!!! warning "Mutual Exclusivity"
    A DID cannot appear in both `allowed_dids` and `denied_dids`. The validator will reject such configurations.

### Rate Limits

Define per-DID rate limits (requests per minute):

```yaml
rate_limits:
  - did: "did:web:high-volume-caller.example.com"
    rpm: 100
  - did: "did:web:low-priority.example.com"
    rpm: 10
```

Rate limits generate **obligations** in policy decisions — the enforcement point is responsible for applying them.

### Operation-Scoped Rules

Apply different trust/access rules to specific operations:

```yaml
operations:
  - pattern: "payment.*"
    min_trust_level: "EV"
    allowed_dids:
      - "did:web:payment-gateway.example.com"
  - pattern: "read.*"
    min_trust_level: ""  # No trust required for reads
```

Operations are matched against `input.action.operation` in policy evaluation.

### MCP Tool-Scoped Rules

Apply rules to specific MCP tools exposed by your agent:

```yaml
mcp_tools:
  - tool: "database_query"
    min_trust_level: "OV"
    denied_dids:
      - "did:web:untrusted.example.com"
  - tool: "file_read"
    min_trust_level: "DV"
```

MCP tool rules are matched against `input.action.mcp_tool` in policy evaluation.

## Complete Example

```yaml
version: "1"
min_trust_level: "DV"

allowed_dids:
  - "did:web:trusted-partner.example.com"
  - "did:web:internal-service.example.com"

denied_dids:
  - "did:web:blocked-agent.example.com"

rate_limits:
  - did: "did:web:trusted-partner.example.com"
    rpm: 1000
  - did: "did:web:internal-service.example.com"
    rpm: 500

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
    allowed_dids:
      - "did:web:notification-service.example.com"
```

## Validation

### CLI Validation

Validate your policy config before deploying:

```bash
# Default file (capiscio-policy.yaml)
capiscio policy validate

# Custom file
capiscio policy validate -f my-policy.yaml

# JSON output for CI integration
capiscio policy validate -f my-policy.yaml --json
```

Exit code `0` means valid; non-zero means validation errors.

### Validation Rules

The validator checks:

- **Version**: Must be `"1"`
- **Trust levels**: Must be one of `""`, `SS`, `REG`, `DV`, `OV`, `EV`
- **DID format**: All DIDs must start with `did:`
- **No duplicates**: A DID cannot appear twice in the same list
- **No cross-listing**: A DID cannot be in both `allowed_dids` and `denied_dids`
- **Rate limits**: RPM must be positive
- **Operations**: Pattern must not be empty
- **MCP tools**: Tool name must not be empty

## Policy Lifecycle

### 1. Create a Proposal

Policies go through a proposal workflow:

```
Create Proposal → Review → Approve → Active
                        ↘ Reject (with reason)
```

### 2. Approval Activates Policy

When a proposal is approved, it becomes the active policy. The previously active policy is marked as superseded.

### 3. Bundle Rebuild

After activation, the policy bundle is automatically rebuilt. Agents polling the bundle endpoint will pick up the new policy on their next refresh cycle.

### 4. Enforcement

Policy enforcement follows the [enforcement mode](../concepts/enforcement.md) configured for your deployment:

- **EM-OBSERVE**: Violations logged but allowed (default)
- **EM-GUARD**: Violations blocked, PDP-unavailable allowed with warning
- **EM-STRICT**: All violations blocked, including PDP unavailability

## Next Steps

- [Policy Scoping](../concepts/policy-scoping.md) — Org/group/agent scoping model
- [Policy API Reference](../reference/policy-api.md) — REST API for policy management
- [CLI Reference](../reference/cli/index.md) — `capiscio policy` commands
