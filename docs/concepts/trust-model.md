# Trust Model

> **How CapiscIO handles agent identity and trust**

## Overview

CapiscIO **verifies** agent identity — it does not **issue** it. This is an important distinction.

| What Guard Does | What Guard Doesn't Do |
|-----------------|----------------------|
| Verifies Ed25519 signatures | Issue agent identities |
| Enforces payload integrity | Run a certificate authority |
| Blocks replay attacks | Auto-discover external keys |
| Works with keys you provision | Replace your existing PKI |

## The SSH Analogy

CapiscIO's trust model is similar to SSH:

- **SSH**: You generate your own keypair. You add trusted public keys to `~/.ssh/authorized_keys` or `known_hosts`.
- **CapiscIO**: Each agent generates its own Ed25519 keypair. You add trusted public keys to `./capiscio_keys/trusted/`.

This model is:

- ✅ **Simple** — No external dependencies
- ✅ **Secure** — Cryptographic verification, not network trust
- ✅ **Self-contained** — Works offline, no registry required
- ⚠️ **Manual** — You manage key distribution yourself

## Directory Structure

```
your-agent/
├── agent-card.json           # Your agent's public metadata + public key
└── capiscio_keys/
    ├── private.pem           # Your private key (never share)
    ├── public.pem            # Your public key
    └── trusted/              # Trust store: public keys of agents you accept
        ├── agent-a-key-1.pem
        ├── agent-b-key-1.pem
        └── ...
```

## Key Generation

### Automatic (Dev Mode)

When you initialize SimpleGuard with `dev_mode=True`, it automatically:

1. Generates an Ed25519 keypair
2. Saves `private.pem` and `public.pem` to `./capiscio_keys/`
3. Updates `agent-card.json` with the public key
4. Adds your own public key to `trusted/` (self-trust)

```python
from capiscio_sdk.simple_guard import SimpleGuard

guard = SimpleGuard(dev_mode=True)  # Auto-generates keys
```

### Manual (Production)

For production, you should generate keys explicitly:

```bash
# Using OpenSSL
openssl genpkey -algorithm Ed25519 -out private.pem
openssl pkey -in private.pem -pubout -out public.pem
```

Or use your organization's key management system (Vault, HSM, KMS).

## Adding Trusted Agents

To accept requests from another agent, add their public key to your trust store:

```bash
# Copy their public key with their key ID as filename
cp /path/to/other-agent/public.pem ./capiscio_keys/trusted/{their-key-id}.pem
```

The filename must match the `kid` (key ID) claim in their JWS headers.

### Example: Two Agents Trusting Each Other

**Agent A** wants to call **Agent B**:

1. Agent A exports its public key
2. Agent B adds Agent A's public key to `./capiscio_keys/trusted/agent-a-key.pem`
3. Agent A signs requests with its private key
4. Agent B's Guard verifies using the trusted public key

For bidirectional trust, repeat in both directions.

## Production Considerations

### Key Distribution at Scale

For teams with many agents, manual key copying doesn't scale. Options:

1. **Automation scripts** — Deploy keys via Ansible, Terraform, or your CD pipeline
2. **Shared storage** — Mount a shared volume with trusted keys (careful with permissions)
3. **PKI integration** — Generate agent keys from your existing CA, distribute via your PKI
4. **Vault/HSM** — Store keys in HashiCorp Vault or a hardware security module

### Key Rotation

To rotate an agent's keys:

1. Generate new keypair
2. Update `agent-card.json` with new public key
3. Distribute new public key to all agents that trust this one
4. (Optional) Keep old key in trust stores during transition period
5. Remove old key from trust stores

### Revocation

To revoke trust in an agent:

1. Delete their public key from `./capiscio_keys/trusted/`
2. Restart Guard (or it will reject on next request when key lookup fails)

!!! warning "No Automatic Revocation"
    Today, revocation is manual. You must remove keys from every trust store that has them.

## What's Coming: Registry

We're designing a **Registry** with early design partners to solve key distribution at scale:

- **Dynamic key discovery** — Fetch public keys by agent ID
- **Revocation lists** — Central revocation without touching every trust store  
- **Key rotation** — Publish new keys, consumers auto-update
- **Audit trail** — Who registered, when, with what keys

The file-based trust model will remain supported as a fallback and for air-gapped environments.

## FAQ

### Does CapiscIO replace Okta/Auth0?

No. Guard handles **agent-to-agent** identity (which software signed this request), not **user** identity (which human is logged in). They're complementary.

### Can I use my existing CA?

Yes. Generate agent keys from your CA, then provision them to agents normally. Guard doesn't care where keys come from — it just verifies signatures.

### What if I have 100 agents?

Today: automate key distribution via your deployment tooling.  
Soon: use the Registry for dynamic key discovery.

### Is the trust store secure?

The trust store contains **public** keys only. The private key (`private.pem`) should be protected with filesystem permissions (0600) and never committed to version control.

## Trust Badges

For scenarios requiring portable, verifiable identity across systems, CapiscIO supports **Trust Badges**—signed JWS tokens that prove an agent's identity and trust level.

```python
from capiscio_sdk import verify_badge, TrustLevel

# Verify an incoming badge
result = verify_badge(
    token,
    trusted_issuers=["https://registry.capisc.io"],
)

if result.valid:
    print(f"Agent: {result.claims.agent_id}")
    print(f"Trust Level: {result.claims.trust_level}")
```

### Trust Levels (0-4)

Trust levels indicate the validation rigor applied during badge issuance:

| Level | Name | Validation | Issuer | Use Case |
|-------|------|------------|--------|----------|
| **0** | Self-Signed (SS) | None | Agent itself (`did:key`) | Development, testing, demos |
| **1** | Registered (REG) | Account verified | CapiscIO CA | Internal agents, early development |
| **2** | Domain Validated (DV) | DNS TXT or HTTP challenge | CapiscIO CA | Production B2B agents |
| **3** | Organization Validated (OV) | DV + legal entity verification | CapiscIO CA | High-trust production |
| **4** | Extended Validated (EV) | OV + manual security audit | CapiscIO CA | Regulated industries |

!!! warning "Level 0 in Production"
    Self-signed (Level 0) badges are for **development only**. In production, verifiers should reject Level 0 badges by default. Use `--accept-self-signed` (CLI) or `accept_self_signed=True` (SDK) to explicitly opt in during development.

### DID Methods by Level

| Level | Typical DID | Description |
|-------|-------------|-------------|
| 0 | `did:key` | Self-describing, derived from public key |
| 1-4 | `did:web` | Registry or domain-hosted identity |

Trust badges include:

- **Agent DID** — Decentralized identifier for the agent
- **Trust Level** — 0-4 indicating validation rigor
- **Issuer** — `did:key` for Level 0, CapiscIO CA for Levels 1-4
- **Expiration** — When the badge expires (default: 5 minutes per RFC-002)

See [RFC-002: Trust Badge System](https://docs.capisc.io/rfcs/blob/main/docs/002-trust-badge.md) for full specification details.

## See Also

- [Enforcement Security](enforcement.md) — How Guard verifies requests
- [SimpleGuard API](../reference/sdk-python/simple-guard.md) — SDK reference
- [Badge API](../reference/sdk-python/badge.md) — Trust Badge verification API
- [Trust Badges Guide](../how-to/security/badges.md) — Practical examples
