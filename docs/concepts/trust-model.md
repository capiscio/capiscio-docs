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
    print(f"Agent: {result.claims.sub}")  # Agent DID
    print(f"Trust Level: {result.claims.level}")  # String: "0" to "4"
```

### Trust Levels (0-4)

Trust levels indicate the validation rigor applied during badge issuance (RFC-002 §5):

| Level | Name | Validation | Issuer | Use Case |
|-------|------|------------|--------|----------|
| **0** | Self-Signed (SS) | None | Agent itself (`did:key`, `iss` = `sub`) | Development, testing, demos |
| **1** | Registered (REG) | Account verified | CapiscIO CA | Internal agents, early development |
| **2** | Domain Validated (DV) | DNS TXT or HTTP challenge | CapiscIO CA | Production B2B agents |
| **3** | Organization Validated (OV) | DV + legal entity verification | CapiscIO CA | High-trust production |
| **4** | Extended Validated (EV) | OV + manual security audit | CapiscIO CA | Regulated industries |

!!! warning "Level 0 in Production"
    Self-signed (Level 0) badges are for **development only**. In production, verifiers should reject Level 0 badges by default. Use `--accept-self-signed` (CLI) or `accept_self_signed=True` (SDK) to explicitly opt in during development.

!!! note "Trust Levels are Strings"
    Per RFC-002 §3, trust levels MUST be treated as strings (`"0"` through `"4"`), not integers. This avoids bugs where `0` might be falsy in some languages.

### Identity Assurance Levels (IAL)

**Separate from Trust Levels**, badges also have an **Identity Assurance Level** that indicates the key binding assurance (RFC-002 §7.2.1):

| IAL | Name | What It Proves |
|-----|------|----------------|
| **IAL-0** | Account-Attested | "Account X requested a badge for agent DID Y" |
| **IAL-1** | Proof of Possession (PoP) | "Requester cryptographically proved they control the private key for DID Y at issuance time" |

The `ial` claim is REQUIRED in all badges. Key points:

- **Level 0 badges are always IAL-0** — Self-signed badges cannot have issuer-verified key binding
- **Levels 1-4 can be IAL-0 or IAL-1** — IAL-1 requires the PoP protocol (RFC-003)
- **IAL-1 badges include a `cnf` claim** — This binds the badge to a specific key holder

### Badge Claims (RFC-002 §4.3)

A Trust Badge contains these claims:

| Claim | Required | Description |
|-------|----------|-------------|
| `jti` | ✅ | Badge ID (UUID) for revocation and audit |
| `iss` | ✅ | Issuer identifier (CA URL for levels 1-4, `did:key` for level 0) |
| `sub` | ✅ | Subject DID (the agent's identity) |
| `iat` | ✅ | Issued At (Unix timestamp) |
| `exp` | ✅ | Expiration (Unix timestamp, default 5 minutes) |
| `ial` | ✅ | Identity Assurance Level (`"0"` or `"1"`) |
| `key` | ✅ | Agent's public key (JWK) |
| `vc` | ✅ | Verifiable Credential object containing `credentialSubject.level` |
| `aud` | ❌ | Audience (array of trust domains where badge is valid) |
| `cnf` | If IAL-1 | Confirmation key binding (RFC 7800) |

### DID Methods by Level

| Level | Typical DID | Description |
|-------|-------------|-------------|
| 0 | `did:key` | Self-describing, derived from public key |
| 1-4 | `did:web` | Registry or domain-hosted identity |

See [RFC-002: Trust Badge Specification](../rfcs/index.md) for complete details, including the PoP protocol (RFC-003).

## See Also

- [Enforcement Security](enforcement.md) — How Guard verifies requests
- [SimpleGuard API](../reference/sdk-python/simple-guard.md) — SDK reference
- [Badge API](../reference/sdk-python/badge.md) — Trust Badge verification API
- [Trust Badges Guide](../how-to/security/badges.md) — Practical examples
