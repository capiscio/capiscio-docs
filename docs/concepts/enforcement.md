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

CapiscIO enforces **Freshness** using timestamp claims:

*   `iat` (issued at): When the request was signed
*   `exp` (expires): When the signature expires

Guard rejects requests outside a 60-second window (with 5s clock skew tolerance).

## 4. Performance Telemetry

Security shouldn't slow you down. CapiscIO adds negligible overhead (<1ms) and proves it with every response.

Check the `Server-Timing` header in any response:

```http
Server-Timing: capiscio-auth;dur=0.618;desc="CapiscIO Verification"
```

*   `dur`: Duration in milliseconds.
*   `desc`: Description of the operation.

## Summary: What Guard Does and Doesn't Do

| Guard Does | Guard Doesn't |
|------------|---------------|
| ✅ Verify agent identity (Ed25519 signatures) | ❌ Issue identities (you generate keys) |
| ✅ Enforce payload integrity (SHA-256 body hash) | ❌ Manage a central registry (coming soon) |
| ✅ Block replay attacks (timestamp validation) | ❌ Replace your IAM/SSO (human auth) |
| ✅ Work with keys you provision | ❌ Auto-discover external agent keys (coming soon) |
