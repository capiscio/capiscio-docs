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

Configure the CapiscIO server to forward policy queries to your PDP. The PEP middleware runs after badge verification and before your route handlers.

---

## Prerequisites

- A running CapiscIO server with badge verification enabled
- A PDP that accepts HTTP POST requests with PIP-format decision requests (RFC-005 §5.1)

---

## Step 1: Start in Observe Mode

Begin with `EM-OBSERVE` to monitor PDP decisions without affecting traffic:

```bash
export CAPISCIO_PDP_ENDPOINT=http://localhost:9090/v1/evaluate
export CAPISCIO_ENFORCEMENT_MODE=EM-OBSERVE
export CAPISCIO_PDP_TIMEOUT_MS=500
```

In this mode, PDP DENY decisions are logged but requests proceed. If the PDP is unreachable, requests also proceed with an `ALLOW_OBSERVE` telemetry marker.

Restart the server and monitor logs for `capiscio.policy_enforced` events.

---

## Step 2: Review Decisions

Check server logs for policy events. Each request that passes through the PEP emits:

| Field | Description |
|-------|-------------|
| `capiscio.policy.decision` | `ALLOW`, `DENY`, or `ALLOW_OBSERVE` |
| `capiscio.policy.decision_id` | Unique ID from the PDP |
| `capiscio.policy.error_code` | `PDP_UNAVAILABLE` if PDP was unreachable |

Verify that legitimate requests receive `ALLOW` and unauthorized access patterns receive `DENY` before tightening the enforcement mode.

---

## Step 3: Tighten Enforcement

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

## Step 4: Configure Break-Glass (Optional)

For emergency access when the PDP is down or mis-configured:

1. Generate a dedicated Ed25519 keypair for break-glass tokens:

    ```bash
    capiscio keygen --output breakglass-key
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
| `CAPISCIO_PDP_ENDPOINT` | _(empty)_ | PDP URL. Empty = badge-only mode (no policy enforcement) |
| `CAPISCIO_PDP_TIMEOUT_MS` | `500` | PDP query timeout in milliseconds |
| `CAPISCIO_ENFORCEMENT_MODE` | `EM-OBSERVE` | One of: `EM-OBSERVE`, `EM-GUARD`, `EM-DELEGATE`, `EM-STRICT` |
| `CAPISCIO_BREAKGLASS_PUBLIC_KEY` | _(empty)_ | Path to break-glass Ed25519 public key file |
| `CAPISCIO_PEP_ID` | _(empty)_ | PEP instance identifier (sent to PDP as `X-Capiscio-PEP-ID`) |
| `CAPISCIO_WORKSPACE` | _(empty)_ | Workspace/tenant identifier |

---

## PDP Request Format

The PEP sends a JSON POST to the PDP endpoint. Your PDP must accept this format:

```json
{
  "pip_version": "capiscio.pip.v1",
  "subject": {
    "did": "did:web:agent.example.com",
    "badge_jti": "badge-uuid",
    "ial": "1",
    "trust_level": "DV"
  },
  "action": {
    "operation": "POST /api/v1/badges",
    "capability_class": null
  },
  "resource": {
    "identifier": "/api/v1/badges"
  },
  "context": {
    "txn_id": "txn-uuid",
    "enforcement_mode": "EM-GUARD"
  },
  "environment": {
    "workspace": "production",
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
curl -v https://your-server/api/v1/badges \
  -H "X-Capiscio-Badge: $BADGE_JWS"

# Look for Server-Timing header with policy timing
# Server-Timing: capiscio-auth;dur=0.6, capiscio-policy;dur=12.3
```
