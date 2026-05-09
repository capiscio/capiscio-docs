---
title: SimpleGuard
description: Zero-config security for A2A agents
---

# SimpleGuard

Zero-configuration security for signing and verifying A2A requests.

---

## Overview

`SimpleGuard` is the recommended way to add security to your A2A agent. It handles:

- **Signing outbound requests** with JWS (JSON Web Signature)
- **Verifying inbound requests** against a trust store
- **Key management** with file-based storage

---

## Basic Usage

```python
from capiscio_sdk.simple_guard import SimpleGuard

# Initialize - uses convention over configuration
# Looks for capiscio_keys/ and agent-card.json in project root
guard = SimpleGuard(dev_mode=True)  # Auto-generates keys for development

# Sign a request
body = b'{"method": "tasks/send", "params": {}}'
jws = guard.sign_outbound({}, body=body)

# Verify an incoming request
claims = guard.verify_inbound(jws, body=body)
```

## Convention Over Configuration

SimpleGuard automatically finds keys based on directory structure:

```
your-project/
├── agent-card.json           # Agent identity
└── capiscio_keys/
    ├── private.pem           # Signing key
    ├── public.pem            # Public key
    └── trusted/              # Trust store
        └── {kid}.pem         # Trusted keys (filename = key ID)
```

In `dev_mode=True`, all files are auto-generated if missing.

---

## API Reference

::: capiscio_sdk.simple_guard.SimpleGuard
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

---

## Authority Envelopes (RFC-008)

SimpleGuard provides methods for creating and verifying delegated authority chains. See the [Delegation Chains concept](../../concepts/delegation.md) for background.

### `create_envelope()`

Create a root Authority Envelope delegating authority to another agent.

```python
envelope_jws = guard.create_envelope(
    subject_did="did:web:worker.example.com",
    capability_class="tools.database.read",
    delegation_depth_remaining=1,
    expires_in_seconds=3600,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `subject_did` | `str` | *(required)* | DID of the agent receiving delegated authority |
| `capability_class` | `str` | *(required)* | Dot-notation capability (e.g., `tools.database.read`) |
| `delegation_depth_remaining` | `int` | `1` | How many further delegations allowed |
| `issuer_badge_jti` | `str` | `""` | JTI of the issuer's badge |
| `txn_id` | `str` | `""` | Transaction ID (auto-generated if empty) |
| `expires_in_seconds` | `int` | `3600` | TTL from now |
| `constraints` | `dict | None` | `None` | JSON-serializable constraints |
| `subject_badge_jti` | `str` | `""` | JTI of the subject's badge |
| `enforcement_mode_min` | `str` | `""` | Minimum enforcement mode |

**Returns:** `str` — JWS Compact Serialization of the signed envelope.

**Raises:** `ConfigurationError` — If signing fails or key is not available.

### `derive_envelope()`

Derive a child Authority Envelope from a parent, with hash linking and monotonic narrowing validation.

```python
child_jws = guard.derive_envelope(
    parent_envelope_jws=root_envelope,
    subject_did="did:web:reader.example.com",
    capability_class="tools.database.read",
    delegation_depth_remaining=0,
    constraints={"tables": ["users"]},
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `parent_envelope_jws` | `str` | *(required)* | Parent envelope JWS to derive from |
| `subject_did` | `str` | *(required)* | DID of the next delegate |
| `capability_class` | `str` | *(required)* | Must be equal or narrower than parent's |
| `delegation_depth_remaining` | `int` | `0` | Must be less than parent's depth |
| `issuer_badge_jti` | `str` | `""` | JTI of the child issuer's own badge |
| `expires_in_seconds` | `int` | `1800` | TTL from now |
| `constraints` | `dict | None` | `None` | Must be equal or more restrictive than parent's |
| `subject_badge_jti` | `str` | `""` | JTI of the subject's badge |
| `enforcement_mode_min` | `str` | `""` | Cannot relax parent's mode |

**Returns:** `str` — JWS Compact Serialization of the signed child envelope.

**Raises:** `ConfigurationError` — On narrowing violation, depth exceeded, or signing failure.

### `make_delegation_headers()`

Generate HTTP headers for a delegated request combining the delegation chain with the agent's badge.

```python
headers = guard.make_delegation_headers(
    chain=[root_envelope, child_envelope],
    badge_map={"did:web:worker.example.com": worker_badge_jws},
)
# headers contains: X-Capiscio-Badge, X-Capiscio-Authority,
#                   X-Capiscio-Authority-Chain, X-Capiscio-Badge-Map
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chain` | `list[str]` | *(required)* | Ordered list of envelope JWS strings `[root, ..., leaf]` |
| `badge_map` | `dict | None` | `None` | DID → badge JWS for intermediate agents in the chain |
| `payload` | `dict | None` | `None` | Optional payload for badge signing |
| `body` | `bytes | None` | `None` | Optional HTTP body bytes to bind to badge signature |

**Returns:** `dict[str, str]` — Dictionary with these headers:

| Header | Description |
|--------|-------------|
| `X-Capiscio-Badge` | This agent's badge JWS |
| `X-Capiscio-Authority` | Leaf envelope JWS |
| `X-Capiscio-Authority-Chain` | Base64url-encoded JSON array of the full chain |
| `X-Capiscio-Badge-Map` | JSON mapping of intermediate DIDs to badge JWS tokens |
