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

### Envelope Verification (RFC-008)

| Variable | Default | Description |
|----------|---------|-------------|
| `CAPISCIO_MAX_CHAIN_DEPTH` | `10` | Maximum delegation chain depth (RFC-008 §9.5) |
| `CAPISCIO_ORG_TRUST_BOUNDARY` | _(empty)_ | Org DID prefix for cross-org chain restrictions. Empty = accept all. |

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
    "enforcement_mode": "EM-GUARD",
    "leaf_capability": "tools.database.read",     // From envelope chain (if present)
    "delegation_depth": 2                          // Chain length (if present)
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

## Authority Chain Headers

When a request includes delegation chain headers, the PEP verifies the chain before querying the PDP. See [Delegation Chains](../../concepts/delegation.md) for background.

### Request Headers

| Header | Description |
|--------|-------------|
| `X-Capiscio-Authority` | Leaf authority envelope JWS |
| `X-Capiscio-Authority-Chain` | Base64url-encoded JSON array of the full envelope chain |
| `X-Capiscio-Badge-Map` | JSON object mapping intermediate agent DIDs to their badge JWS tokens |

### Chain Verification Errors

| Error Code | HTTP Status | Description |
|-----------|-------------|-------------|
| `ENVELOPE_CHAIN_TOO_DEEP` | 403 | Chain exceeds `CAPISCIO_MAX_CHAIN_DEPTH` |
| `ENVELOPE_SIGNATURE_INVALID` | 401 | Envelope signature verification failed |
| `ENVELOPE_NARROWING_VIOLATION` | 403 | Child is wider than parent |
| `ENVELOPE_EXPIRED` | 401 | Envelope has expired |
| `ENVELOPE_DEPTH_EXCEEDED` | 403 | Delegation depth remaining is negative |
| `ENVELOPE_CHAIN_BROKEN` | 401 | Hash chain integrity failure |

In `EM-OBSERVE` mode, chain verification failures are logged but the request proceeds.

### PDP Enrichment

When a valid chain is present, the PDP request `context` is enriched with:

| Field | Description |
|-------|-------------|
| `leaf_capability` | Capability class from the leaf envelope |
| `delegation_depth` | Number of envelopes in the verified chain |
| `enforcement_mode` | May be escalated if any envelope sets `enforcement_mode_min` |

---

## See Also

- [Policy Enforcement Setup](../../how-to/security/policy-enforcement.md) — Step-by-step setup guide
- [Delegation Chains](../../how-to/security/delegation-chains.md) — Creating and using delegation chains
- [Policy Config YAML](../policy-config-yaml.md) — Policy configuration format
- [Policy API](../policy-api.md) — Policy management API
