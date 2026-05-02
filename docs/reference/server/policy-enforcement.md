# Policy Enforcement Reference

Configuration reference for CapiscIO's Policy Enforcement Point (PEP) and PDP integration.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CAPISCIO_EMBEDDED_PDP` | `false` | Enable embedded OPA evaluator (in-process PDP) |
| `CAPISCIO_PDP_ENDPOINT` | _(empty)_ | External PDP URL. Empty + no embedded PDP = badge-only mode |
| `CAPISCIO_PDP_TIMEOUT_MS` | `500` | External PDP query timeout in milliseconds |
| `CAPISCIO_ENFORCEMENT_MODE` | `EM-OBSERVE` | One of: `EM-OBSERVE`, `EM-GUARD`, `EM-DELEGATE`, `EM-STRICT` |
| `CAPISCIO_WORKSPACE` | _(empty)_ | Workspace/tenant UUID (required for embedded PDP) |
| `CAPISCIO_BUNDLE_POLL_INTERVAL` | `30s` | Embedded PDP bundle rebuild interval |
| `CAPISCIO_BUNDLE_STALENESS_THRESHOLD` | `5m` | Embedded PDP bundle age before staleness warnings |
| `CAPISCIO_BREAKGLASS_PUBLIC_KEY` | _(empty)_ | Path to break-glass Ed25519 public key file |
| `CAPISCIO_PEP_ID` | _(empty)_ | PEP instance identifier (sent to PDP as `X-Capiscio-PEP-ID`) |

---

## Enforcement Modes

| Mode | PDP DENY | PDP Unavailable | Obligations | Staleness |
|------|----------|-----------------|-------------|-----------|
| `EM-OBSERVE` | Logged, request proceeds | Request proceeds | Not enforced | Annotated in telemetry |
| `EM-GUARD` | Request blocked (403) | Request blocked (503) | Not enforced | Annotated in telemetry |
| `EM-DELEGATE` | Request blocked (403) | Request blocked (503) | Best-effort (failures logged) | Annotated in telemetry |
| `EM-STRICT` | Request blocked (403) | Request blocked (503) | Enforced (unknown types cause denial) | Request denied |

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
    "trust_level": "DV"  // Badge trust level code: SS(0), REG(1), DV(2), OV(3), EV(4)
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

### PDP Response Format

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

## Telemetry Fields

Each request through the PEP emits structured telemetry:

| Field | Description |
|-------|-------------|
| `capiscio.policy.decision` | `ALLOW`, `DENY`, or `ALLOW_OBSERVE` |
| `capiscio.policy.decision_id` | Unique evaluation ID from the PDP |
| `capiscio.policy.error_code` | `PDP_UNAVAILABLE` if PDP was unreachable |
| `staleness.bundle_stale` | `true` if the embedded PDP bundle is stale |
| `staleness.bundle_age_ms` | Age of the bundle in milliseconds (when stale) |

---

## Bundle Endpoint (Embedded PDP)

When the embedded PDP is active, a bundle endpoint is available for external OPA consumers:

```
GET /v1/bundles/{workspace_id}
```

Requires `X-Capiscio-Registry-Key` authentication. The API key must belong to the matching workspace/org.

---

## See Also

- [Policy Enforcement Setup](../../how-to/security/policy-enforcement.md) — Step-by-step setup guide
- [Policy Config YAML](../policy-config-yaml.md) — Policy configuration format
- [Policy API](../policy-api.md) — Policy management API
