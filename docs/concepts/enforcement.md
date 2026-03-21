---
title: Enforcement First Security
description: How CapiscIO enforces Agent Identity and Integrity for A2A Agents.
---

# Enforcement First Security

CapiscIO operates on a simple principle: **Enforcement First**. Before an agent processes a single byte of a request, it must verify the **Identity** of the calling agent and the **Integrity** of the message.

## The Trust Model

!!! info "Key Concept: Self-Issued Keys"
    CapiscIO does not issue agent identities. Each agent generates its own Ed25519 keypair. Guard **verifies** identities using keys you provision — similar to how SSH uses `known_hosts`.

**How it works today:**

1. **Each agent generates its own keys** (Ed25519 keypair)
2. **Public keys are shared manually** (copied to trust stores)
3. **Guard verifies signatures** against keys in the local trust store

This is intentional. We enforce identity verification at the protocol layer without requiring a central authority. You control which agents you trust.

!!! tip "What's Coming"
    We're designing a **Registry** with early partners to enable dynamic key discovery and revocation. Today's file-based model will remain supported as a fallback.

## The "Customs Officer" Model

Think of `SimpleGuard` as a Customs Officer at the border of your agent. It stops every request and asks three questions:

1.  **"Who are you?"** (Agent Identity)
2.  **"Did you really say this?"** (Payload Integrity)
3.  **"Is this current?"** (Freshness / Replay Protection)

If any answer is "No", the request is rejected immediately.

## 1. Agent Identity Verification (Trust Badge)

CapiscIO uses **Trust Badges** (signed JWS tokens per RFC-002) with **Ed25519** keys to prove agent identity.

### The Handshake
1.  **Sender**: Signs the request using their private key.
2.  **Header**: The request includes an `X-Capiscio-Badge` header containing the signature (RFC-002 §9.1).
3.  **Receiver**:
    *   Extracts the Key ID (`kid`) from the header.
    *   Looks up the public key in the local Trust Store (`./capiscio_keys/trusted/`).
    *   Verifies the signature.

### Zero-Config Dev Mode
When initialized with `dev_mode=True`, `SimpleGuard` automatically:

*   Generates a new Ed25519 keypair in `./capiscio_keys/`.
*   Creates an `agent-card.json` with the public key.
*   Adds the public key to the local Trust Store (Self-Trust).

### Adding External Agents to Your Trust Store

To accept requests from another agent:

```bash
# Copy their public key to your trust store
cp /path/to/other-agent/capiscio_keys/public.pem \
   ./capiscio_keys/trusted/{their-key-id}.pem
```

The `{their-key-id}` must match the `kid` claim in their JWS headers.

!!! warning "Manual Key Management"
    Today, you manage trust stores manually (like SSH `known_hosts`). For production deployments with many agents, we recommend automating this via your existing PKI, Vault, or deployment tooling.

## 2. Integrity Verification (Body Hash)

Identity is not enough. An attacker could intercept a valid signed request and change the body (e.g., "Transfer $10" → "Transfer $1M").

To prevent this, CapiscIO enforces **Payload Integrity** using a Body Hash (`bh`) claim.

### The Process
1.  **Sender**:
    *   Calculates `SHA-256(HTTP Body)`.
    *   Adds the hash to the JWS payload as claim `bh`.
    *   Signs the JWS.
2.  **Receiver**:
    *   Verifies the JWS signature (Identity).
    *   Calculates `SHA-256(Received HTTP Body)`.
    *   Compares the calculated hash with the `bh` claim.

If the hashes do not match, `SimpleGuard` raises a `VerificationError` and returns `403 Forbidden`.

## 3. Freshness / Replay Protection

Even with valid identity and integrity, an attacker could capture a legitimate request and replay it.

CapiscIO enforces **Freshness** using timestamp claims per RFC-002 §8.1:

*   `iat` (issued at): When the badge was issued
*   `exp` (expires): When the badge expires

Guard rejects requests outside a **60-second clock skew tolerance** window. Both `iat` and `exp` are validated with this tolerance applied, allowing for clock drift in distributed systems.

### Badge Verification Algorithm (RFC-002 §8.1)

When verifying a Trust Badge, the Guard performs these checks in order:

1. **Decode JWS** — Parse the badge as a signed JSON Web Signature
2. **Validate signature** — Verify using the issuer's public key
3. **Check `iat`** — Reject if `iat` is in the future (minus clock tolerance)
4. **Check `exp`** — Reject if current time is past `exp` (plus clock tolerance)
5. **Validate `iss`** — Confirm issuer is in trusted issuers list
6. **Validate `sub`** — Confirm subject DID format is valid
7. **Check `ial`** — Validate IAL claim is `"0"` or `"1"`
8. **Validate `key`** — Confirm public key JWK is well-formed
9. **If IAL-1, validate `cnf`** — Check confirmation key binding (RFC 7800)
10. **Trust level policy** — Check if `vc.credentialSubject.level` meets minimum required level

!!! tip "Error Codes (RFC-002 §8.5)"
    When verification fails, the Guard returns specific error codes: `BADGE_EXPIRED`, `BADGE_NOT_YET_VALID`, `INVALID_SIGNATURE`, `UNTRUSTED_ISSUER`, `INVALID_DID`, `TRUST_LEVEL_INSUFFICIENT`. See [RFC-002 §8.5](../rfcs/index.md) for the complete error code reference.

## 4. Performance Telemetry

Security shouldn't slow you down. CapiscIO adds negligible overhead (<1ms) and proves it with every response.

Check the `Server-Timing` header in any response:

```http
Server-Timing: capiscio-auth;dur=0.618;desc="CapiscIO Verification"
```

*   `dur`: Duration in milliseconds.
*   `desc`: Description of the operation.

## 5. Policy Enforcement (PDP Integration)

Badge verification answers **"who is calling?"** — but not **"are they allowed to do this?"**. Policy enforcement adds authorization decisions via a Policy Decision Point (PDP).

### How It Works

The Policy Enforcement Point (PEP) sits between badge verification and your route handlers. After a badge is verified, the PEP asks an external PDP whether the request should proceed.

```
┌─────────┐     ┌─────────────┐     ┌─────┐     ┌──────────────┐
│ Request  │────▶│   Badge     │────▶│ PEP │────▶│ Your Handler │
│(+ badge) │     │ Verification│     │     │     │              │
└─────────┘     └─────────────┘     └──┬──┘     └──────────────┘
                                       │
                                  ┌────▼────┐
                                  │   PDP   │
                                  │(external)│
                                  └─────────┘
```

The PEP sends a **PIP request** (Policy Information Point) containing identity, action, and resource attributes. The PDP returns ALLOW or DENY, plus optional **obligations** the PEP must enforce.

### Enforcement Modes

Four modes control how strictly the PEP enforces PDP decisions. They form a total order from most permissive to most restrictive:

| Mode | PDP Denies | PDP Unavailable | Unknown Obligation |
|------|-----------|-----------------|-------------------|
| **EM-OBSERVE** | Log only, allow through | Allow (emit `ALLOW_OBSERVE`) | Log, skip |
| **EM-GUARD** | Block request | Deny (fail-closed) | Log, skip |
| **EM-DELEGATE** | Block request | Deny (fail-closed) | Log warning, proceed |
| **EM-STRICT** | Block request | Deny (fail-closed) | Deny request |

Start with `EM-OBSERVE` to monitor decisions without affecting traffic, then tighten as your policies mature.

### Obligations

A PDP can attach obligations to an ALLOW decision — actions the PEP must perform before forwarding the request. Examples from the RFC:

| Obligation Type | Purpose | Example Params |
|----------------|---------|----------------|
| `rate_limit.apply` | Enforce per-agent rate limits | `{ "rpm": 100, "key": "agent-did" }` |
| `redact.fields` | Remove sensitive fields | `{ "fields": ["/pii/email"] }` |
| `log.enhanced` | Enhanced audit logging | `{ "level": "audit" }` |
| `require_step_up` | Require human review | `{ "mode": "human_review" }` |

How the PEP handles obligation failures depends on the enforcement mode. In EM-STRICT, failing to enforce any known obligation blocks the request. In EM-OBSERVE, failures are logged but the request proceeds.

### Decision Caching

The PEP caches ALLOW decisions to reduce PDP latency. Cache keys are derived from the agent DID, badge JTI, operation, and resource. The effective TTL is the minimum of:

- The PDP-returned `ttl`
- The badge `exp` (expiry)
- The envelope `expires_at` (if present)

DENY decisions are not cached by default.

### Break-Glass Override

For emergencies, a break-glass token bypasses the PDP entirely. The token is a signed JWS (EdDSA) with a scoped grant and an expiry (recommended: 5 minutes). It skips authorization but **not** authentication — the badge must still be valid.

The PEP emits `capiscio.policy.override = true` telemetry for audit when a break-glass token is used.

!!! warning "Break-Glass Keys"
    Use a separate Ed25519 keypair for break-glass tokens. Do not reuse your CA badge-signing key.

### Badge-Only Mode

If no PDP endpoint is configured, the PEP is a no-op passthrough. Badge verification still runs, but no policy decisions are made. This is the default behavior.

!!! tip "Getting Started"
    See [Policy Enforcement Setup](../how-to/security/policy-enforcement.md) for step-by-step configuration.

---

## Summary: What Guard Does and Doesn't Do

| Guard Does | Guard Doesn't |
|------------|---------------|
| ✅ Verify agent identity (Ed25519 signatures) | ❌ Issue identities (you generate keys) |
| ✅ Enforce payload integrity (SHA-256 body hash) | ❌ Manage a central registry (coming soon) |
| ✅ Block replay attacks (timestamp validation) | ❌ Replace your IAM/SSO (human auth) |
| ✅ Work with keys you provision | ❌ Auto-discover external agent keys (coming soon) |
| ✅ Enforce PDP policy decisions (when configured) | ❌ Provide a PDP (bring your own) |
| ✅ Support break-glass emergency overrides | ❌ Bypass authentication for overrides |
