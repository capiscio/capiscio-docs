---
title: Policy Enforcement Setup
description: Configure PDP integration to add authorization decisions to your agent
---

# Policy Enforcement Setup

Add authorization decisions to badge-verified requests by connecting to a Policy Decision Point (PDP).

---

## Problem

You need to:

- Control which agents can access which endpoints based on policy
- Enforce rate limits, field redaction, or audit logging per-agent
- Gradually roll out policy enforcement without breaking existing traffic
- Override policy in emergencies

---

## Solution

Configure the CapiscIO server to enforce policy decisions. Two PDP modes are available:

| Mode | Description | Use When |
|------|-------------|----------|
| **Embedded PDP** | In-process OPA evaluator; zero-latency policy queries | Single-node deployments, fast iteration, no external dependencies |
| **External PDP** | Remote HTTP PDP (any OPA/Cedar/custom endpoint) | Multi-node fleets, existing PDP infrastructure, custom engines |

---

## Option A: Embedded PDP (Recommended)

The embedded PDP runs an OPA evaluator inside the server process. It automatically builds a policy bundle from your registry data (agents, MCP servers) and a built-in starter policy.

### Prerequisites

- A running CapiscIO server with badge verification enabled
- `CAPISCIO_WORKSPACE` set to your workspace/org UUID

### Step 1: Enable the Embedded PDP

```bash
export CAPISCIO_EMBEDDED_PDP=true
export CAPISCIO_WORKSPACE=YOUR_WORKSPACE_UUID
export CAPISCIO_ENFORCEMENT_MODE=EM-OBSERVE
```

The server starts an in-process OPA evaluator with:

- A **starter Rego policy** that allows requests from registered agents with active status
- A **policy bundle** auto-built from registry data (agents, MCP servers, workspace policies)
- **Hybrid rebuild**: timer-based polling (default 30s) plus event-driven rebuild on registry changes

### Step 2: Review Decisions

Check server logs for policy events. Each request emits:

| Field | Description |
|-------|-------------|
| `capiscio.policy.decision` | `ALLOW`, `DENY`, or `ALLOW_OBSERVE` |
| `capiscio.policy.decision_id` | Unique evaluation ID |
| `staleness.bundle_stale` | `true` if the policy bundle is stale |
| `staleness.bundle_age_ms` | Age of the bundle in milliseconds (when stale) |

Verify that legitimate requests receive `ALLOW` and unauthorized access patterns receive `DENY` before tightening the enforcement mode.

### Step 3: Tighten Enforcement

Once decisions look correct, move through the enforcement modes:

```bash
# Allow but log — PDP decisions are informational
export CAPISCIO_ENFORCEMENT_MODE=EM-OBSERVE

# Deny unauthorized — PDP DENY blocks requests (fail-closed on PDP failure)
export CAPISCIO_ENFORCEMENT_MODE=EM-GUARD

# Full enforcement — unknown obligation types also cause denial
export CAPISCIO_ENFORCEMENT_MODE=EM-STRICT
```

### Bundle Staleness

When the embedded PDP's policy bundle hasn't been rebuilt within the staleness threshold:

| Mode | Behavior |
|------|-----------|
| `EM-OBSERVE` | Request proceeds; `staleness.bundle_stale` annotation in telemetry |
| `EM-GUARD` | Request proceeds; `staleness.bundle_stale` annotation in telemetry |
| `EM-STRICT` | Request denied with `BUNDLE_STALE` error code |

Configure staleness via:

```bash
export CAPISCIO_BUNDLE_STALENESS_THRESHOLD=5m  # default: 5m
export CAPISCIO_BUNDLE_POLL_INTERVAL=30s        # default: 30s
```

### Bundle Endpoint

When the embedded PDP is active, a bundle endpoint is available for external OPA consumers:

```
GET /v1/bundles/{workspace_id}
```

This requires `X-Capiscio-Registry-Key` authentication and the API key must belong to the matching workspace/org.

---

## Option B: External PDP

Connect to any PDP that accepts HTTP POST requests with PIP-format decision requests ([RFC-005 §5.1](https://github.com/capiscio/capiscio-rfcs)).

### Prerequisites

- A running CapiscIO server with badge verification enabled
- A PDP that accepts HTTP POST requests

### Step 1: Start in Observe Mode

Begin with `EM-OBSERVE` to monitor PDP decisions without affecting traffic:

```bash
export CAPISCIO_PDP_ENDPOINT=http://localhost:9090/v1/evaluate
export CAPISCIO_ENFORCEMENT_MODE=EM-OBSERVE
export CAPISCIO_PDP_TIMEOUT_MS=500
```

In this mode, PDP DENY decisions are logged but requests proceed. If the PDP is unreachable, requests also proceed with an `ALLOW_OBSERVE` telemetry marker.

Restart the server and monitor logs for policy enforcement events (the event type is `capiscio.policy_enforced`). Each event flattens the PDP verdict into the `capiscio.policy.*` fields described below, including `capiscio.policy.decision`.

---

### Step 2: Review Decisions

Check server logs for policy events. Each request that passes through the PEP emits:

| Field | Description |
|-------|-------------|
| `capiscio.policy.decision` | `ALLOW`, `DENY`, or `ALLOW_OBSERVE` |
| `capiscio.policy.decision_id` | Unique ID from the PDP |
| `capiscio.policy.error_code` | `PDP_UNAVAILABLE` if PDP was unreachable |

Verify that legitimate requests receive `ALLOW` and unauthorized access patterns receive `DENY` before tightening the enforcement mode.

---

### Step 3: Tighten Enforcement

Once decisions look correct, switch to `EM-GUARD`:

```bash
export CAPISCIO_ENFORCEMENT_MODE=EM-GUARD
```

Now PDP DENY decisions block requests with `403 Forbidden`. If the PDP is unavailable, requests are denied with `503 Service Unavailable` (fail-closed).

For full obligation enforcement, use `EM-STRICT`:

```bash
export CAPISCIO_ENFORCEMENT_MODE=EM-STRICT
```

In EM-STRICT, unknown obligation types cause the request to be denied.

---

### Step 4: Configure Break-Glass (Optional)

For emergency access when the PDP is down or misconfigured:

1. Generate a dedicated Ed25519 keypair for break-glass tokens:

    ```bash
    capiscio key gen --out-priv breakglass-key.pem --out-pub breakglass-key.pub.pem
    ```

2. Configure the server with the public key path:

    ```bash
    export CAPISCIO_BREAKGLASS_PUBLIC_KEY=/etc/capiscio/breakglass-key.pub.pem
    ```

3. In an emergency, issue a break-glass token and include it as the `X-Capiscio-Breakglass` header. The token must contain a `reason`, scoped `methods`/`routes`, and a short expiry.

!!! warning
    Break-glass bypasses authorization but **not** authentication. The request must still carry a valid badge.

---

## Configuration Reference

All PDP-related environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CAPISCIO_EMBEDDED_PDP` | `false` | Enable embedded OPA evaluator (in-process PDP) |
| `CAPISCIO_PDP_ENDPOINT` | _(empty)_ | External PDP URL. Empty + no embedded PDP = badge-only mode |
| `CAPISCIO_PDP_TIMEOUT_MS` | `500` | External PDP query timeout in milliseconds |
| `CAPISCIO_ENFORCEMENT_MODE` | `EM-OBSERVE` | One of: `EM-OBSERVE`, `EM-GUARD`, `EM-STRICT` |
| `CAPISCIO_WORKSPACE` | _(empty)_ | Workspace/tenant UUID (required for embedded PDP) |
| `CAPISCIO_BUNDLE_POLL_INTERVAL` | `30s` | Embedded PDP bundle rebuild interval |
| `CAPISCIO_BUNDLE_STALENESS_THRESHOLD` | `5m` | Embedded PDP bundle age before staleness warnings |
| `CAPISCIO_BREAKGLASS_PUBLIC_KEY` | _(empty)_ | Path to break-glass Ed25519 public key file |
| `CAPISCIO_PEP_ID` | _(empty)_ | PEP instance identifier (sent to PDP as `X-Capiscio-PEP-ID`) |

---

## PDP Request Format

The PEP sends a JSON POST to the PDP endpoint. Your PDP must accept this format:

```jsonc
{
  "pip_version": "capiscio.pip.v1",
  "subject": {
    "did": "did:web:agent.example.com",
    "badge_jti": "badge-uuid",
    "ial": "1",
    "trust_level": "DV"  // Trust level code (DV/OV/EV) — maps to IAL 1/2/3
  },
  "action": {
    "operation": "POST /v1/badges",
    "capability_class": null
  },
  "resource": {
    "identifier": "/v1/badges"
  },
  "context": {
    "txn_id": "txn-uuid",
    "enforcement_mode": "EM-GUARD"
  },
  "environment": {
    "workspace": "00000000-0000-0000-0000-000000000000",
    "pep_id": "server-01",
    "time": "2026-03-01T12:00:00Z"
  }
}
```

And return:

```json
{
  "decision": "ALLOW",
  "decision_id": "eval-uuid",
  "obligations": [],
  "reason": "Policy matched: allow-trusted-agents",
  "ttl": 300
}
```

---

## Verification

Confirm policy enforcement is active:

```bash
# Send a request and check response headers
curl -v https://your-server/v1/agents \
  -H "X-Capiscio-Badge: $BADGE_JWS"

# Look for Server-Timing header with policy timing
# Server-Timing: capiscio-auth;dur=0.6, capiscio-policy;dur=12.3
```
