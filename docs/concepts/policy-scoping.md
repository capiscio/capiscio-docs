---
title: Policy Scoping
description: How CapiscIO's three-level policy scoping model (org → group → agent) enables granular trust and access control.
---

# Policy Scoping

CapiscIO uses a **three-level scoping model** for policy configuration, providing flexible control over agent trust and access at every level of your organization.

## Scope Levels

```
┌─────────────────────────────────────────┐
│              Org Policy                 │  Baseline for all agents
│  min_trust_level: DV                    │
│  denied_dids: [did:web:blocked.ex]      │
├─────────────┬───────────────────────────┤
│ Group: PII  │ Group: Public             │  Named agent collections
│ min_trust:  │ min_trust: ""             │
│   OV        │                           │
├──────┬──────┼───────────────────────────┤
│ Agent│Override                          │  Per-agent overrides
│ EV   │                                  │
└──────┴──────┴───────────────────────────┘
```

### 1. Organization Scope (Baseline)

The **org-level policy** is the baseline that applies to every agent in your organization. It defines the minimum trust requirements, default access rules, and rate limits.

```yaml
# capiscio-policy.yaml (org scope)
version: "1"
min_trust_level: "DV"
denied_dids:
  - "did:web:known-bad-actor.example.com"
rate_limits:
  - did: "did:web:high-volume.example.com"
    rpm: 100
```

### 2. Group Scope (Named Collections)

**Policy groups** allow you to apply rules to named collections of agents. For example, you might create a "PII Handlers" group with stricter trust requirements, or a "Public APIs" group with more permissive settings.

Groups have a **precedence** value (lower = higher priority) that determines which group policy takes effect when an agent belongs to multiple groups.

```yaml
# Group: pii-handlers (precedence: 10)
version: "1"
min_trust_level: "OV"
allowed_dids:
  - "did:web:trusted-processor.example.com"
```

### 3. Agent Scope (Per-Agent Overrides)

**Agent-level policies** provide the finest granularity. They override both org and group policies for a specific agent. Use these for agents with unique requirements.

```yaml
# Agent: critical-payment-processor
version: "1"
min_trust_level: "EV"
operations:
  - pattern: "payment.*"
    min_trust_level: "EV"
    allowed_dids:
      - "did:web:payment-gateway.example.com"
```

## Resolution Algorithm

When evaluating a policy decision, CapiscIO resolves the **effective policy** for each agent by merging policies in order:

1. Start with the **org policy** (baseline)
2. Apply **group policies** in precedence order (lowest precedence number first)
3. Apply **agent-specific overrides** (highest priority)

The resolution is **deterministic**: given the same set of active policies, the resolved result is always identical. This is critical for audit and debugging.

### Override Behavior

- **`min_trust_level`**: Narrower scope wins (agent > group > org)
- **`allowed_dids`**: Intersection (more specific scope restricts further)
- **`denied_dids`**: Union (denied at any scope = denied everywhere)
- **`rate_limits`**: Most specific scope wins per DID
- **`operations`** and **`mcp_tools`**: Most specific scope wins per pattern/tool name

## Visibility and Auditability

Every policy resolution produces an **attribution trail** showing which scope contributed which rule. This is accessible via:

- **Resolved Policy endpoint**: `GET /v1/orgs/{orgId}/policy/agents/{agentId}/resolved`
- **Lineage endpoint**: `GET /v1/orgs/{orgId}/policy/agents/{agentId}/lineage`
- **Policy Context** (SDK): `capiscio policy context`

The resolved endpoint returns the effective policy for a specific agent. The lineage endpoint returns all policy documents that contributed to the resolution, in precedence order.

## Trust Levels

CapiscIO defines six trust levels, each representing increasing assurance about an agent's identity:

| Level | Name | Meaning |
|-------|------|---------|
| (empty) | None | No trust requirement |
| `SS` | Self-Signed | Agent has a self-signed key |
| `REG` | Registered | Agent is registered in the registry |
| `DV` | Domain Validated | Agent's domain ownership is verified |
| `OV` | Organization Validated | Agent's organization is verified |
| `EV` | Extended Validation | Agent has undergone extended validation |

Trust levels are hierarchical: `EV > OV > DV > REG > SS > (none)`.

## Next Steps

- [Configure Agent Policy](../how-to/configure-agent-policy.md) — YAML config walkthrough
- [Policy API Reference](../reference/policy-api.md) — Phase-one API endpoints
- [CLI Reference](../reference/cli/index.md) — `capiscio policy` commands
