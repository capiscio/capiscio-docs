---
title: Delegation Chains
description: How authority envelopes enable scoped, verifiable delegation between agents
---

# Delegation Chains

In multi-agent workflows, one agent often needs to act on behalf of another. Authority Envelopes provide a cryptographic mechanism for scoped, verifiable delegation.

---

## The Problem

Consider a workflow where Agent A asks Agent B to perform a database query, and Agent B delegates that to Agent C (a specialized database reader). Without delegation:

- Agent C has no proof that Agent A authorized this action
- There's no way to scope what Agent C is allowed to do
- The chain of authority is invisible to enforcement points

Trust badges prove **identity** ("I am Agent B"), but not **authority** ("Agent A authorized me to read from the database").

---

## Authority Envelopes

An **Authority Envelope** is a JWS-signed token (defined in [RFC-008](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/008-delegated-authority-envelopes.md)) that grants scoped authority from one agent to another.

Key claims in an envelope:

| Claim | Description |
|-------|-------------|
| `iss` | DID of the agent granting authority |
| `sub` | DID of the agent receiving authority |
| `cap` | Capability class (e.g., `tools.database.read`) |
| `depth` | Remaining delegation depth (decrements at each hop) |
| `exp` | Expiration time |
| `parent_hash` | SHA-256 hash of the parent envelope (for chain integrity) |
| `constraints` | Optional restrictions (time windows, resource filters) |
| `enforcement_mode_min` | Minimum enforcement mode for this delegation |

---

## Chain Structure

Envelopes form **hash-linked chains** where each child references its parent:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Root Envelope   │────▶│  Child Envelope  │────▶│  Leaf Envelope   │
│                  │     │                  │     │                  │
│ iss: Agent A     │     │ iss: Agent B     │     │ iss: Agent C     │
│ sub: Agent B     │     │ sub: Agent C     │     │ sub: Agent D     │
│ cap: tools.*     │     │ cap: tools.db.*  │     │ cap: tools.db.rd │
│ depth: 2         │     │ depth: 1         │     │ depth: 0         │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Monotonic Narrowing

Each link in the chain must be **equal or narrower** than its parent:

- **Capability class** can only narrow (e.g., `tools.*` → `tools.db.*` → `tools.db.read`)
- **Delegation depth** must decrease
- **Constraints** can only become more restrictive
- **Expiration** cannot exceed the parent's expiration

This ensures authority can never be escalated through delegation.

### Enforcement Mode Escalation

Envelopes can set a minimum enforcement mode via `enforcement_mode_min`. This mode can only **escalate** (become stricter) through the chain:

| Mode | Strictness | Behavior on DENY |
|------|-----------|-------------------|
| `EM-OBSERVE` | Lowest | Logged, request proceeds |
| `EM-GUARD` | Medium | Request blocked |
| `EM-STRICT` | Highest | Request blocked, unknown obligations denied |

If a parent sets `EM-GUARD`, no child can relax it to `EM-OBSERVE`.

---

## Chain Verification

When the gateway PEP receives a request with delegation headers, it verifies the entire chain (RFC-008 §9.2):

1. **Signature verification** — Each envelope is signed by its issuer
2. **Hash chain integrity** — Each child's `parent_hash` matches the parent
3. **Narrowing validation** — Capabilities, depth, and constraints narrow monotonically
4. **Badge binding** — The leaf envelope's `sub` matches the caller's badge subject
5. **Depth limits** — Chain length does not exceed `MaxChainDepth` (default: 10)
6. **Expiration** — All envelopes in the chain are within their validity period
7. **Enforcement mode** — The strictest mode across the chain is applied

---

## Trust Boundaries

Delegation chains can span organizational boundaries. The `OrgTrustBoundary` configuration controls whether cross-org chains are accepted:

- **Same-org chains**: All issuers share the same org DID prefix — always accepted
- **Cross-org chains**: Issuers from different orgs — accepted only when `OrgTrustBoundary` is empty or matches

---

## Relationship to Badges

Envelopes and badges serve complementary roles:

| | Badge | Envelope |
|-|-------|----------|
| **Proves** | Identity ("I am Agent B") | Authority ("Agent A authorized me") |
| **Issued by** | CA / Self-signed | Another agent |
| **Scope** | Agent-level trust | Per-action capability |
| **Lifetime** | Hours to days | Minutes to hours |
| **Header** | `X-Capiscio-Badge` | `X-Capiscio-Authority` |

A delegated request carries both: the badge proves who the caller is, and the envelope chain proves they have authority to act.

---

## Transport Headers

Delegation chains are transmitted via HTTP headers:

| Header | Content |
|--------|---------|
| `X-Capiscio-Authority` | Leaf envelope JWS |
| `X-Capiscio-Authority-Chain` | Base64url-encoded JSON array of the full chain |
| `X-Capiscio-Badge-Map` | JSON object mapping intermediate agent DIDs to their badge JWS tokens |

---

## DID Resolution

Chain verification requires resolving issuer DIDs to their public keys. CapiscIO uses a **composite key resolver** that handles both DID methods:

| DID Method | Resolution | Example |
|------------|-----------|---------|
| `did:key` | Local decode (no network) | `did:key:z6Mk...` |
| `did:web` | HTTPS fetch of DID document | `did:web:agent.example.com` |

### DID:web Security

The `did:web` resolver includes SSRF protections (RFC-008 §17.1):

- **HTTPS required** in production (HTTP only allowed in dev mode)
- **Blocked destinations**: localhost, private IPs (10.x, 172.16.x, 192.168.x), link-local, cloud metadata endpoints
- **No redirect following** (prevents SSRF via redirect chains)
- **Response size limits**: 64 KB maximum
- **Request timeouts**: 10 seconds
- **Document caching**: 5-minute TTL (reduces network calls)

---

## Next Steps

- [Create and use delegation chains](../how-to/security/delegation-chains.md) — Step-by-step guide
- [Gateway setup](../how-to/security/gateway-setup.md) — Configure the PEP to verify chains
- [Policy enforcement config](../reference/server/policy-enforcement.md) — Chain verification settings
- [RFC-008](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/008-delegated-authority-envelopes.md) — Full specification
