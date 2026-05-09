---
title: Delegation Chains
description: Create and verify authority delegation chains between agents
---

# Create and Verify Delegation Chains

Use Authority Envelopes to delegate scoped authority from one agent to another in multi-agent workflows.

---

## Prerequisites

- CapiscIO SDK installed (`pip install capiscio-sdk`)
- Agent registered with a trust badge
- `SimpleGuard` initialized with agent keys

```python
from capiscio_sdk import CapiscIO

agent = CapiscIO.connect()  # Reads CAPISCIO_API_KEY from env
guard = agent.simple_guard()
```

---

## Step 1: Create a Root Envelope

The root envelope is the starting point of a delegation chain. It grants authority from your agent to another agent.

```python
# Agent A delegates "tools.database.read" to Agent B
envelope = guard.create_envelope(
    subject_did="did:web:agent-b.example.com",
    capability_class="tools.database.read",
    delegation_depth_remaining=1,  # Agent B can delegate once more
    expires_in_seconds=3600,       # 1 hour
)
```

### With Constraints

Add constraints to further limit what the delegate can do:

```python
envelope = guard.create_envelope(
    subject_did="did:web:agent-b.example.com",
    capability_class="tools.database.read",
    delegation_depth_remaining=1,
    constraints={
        "tables": ["users", "orders"],
        "max_rows": 1000,
    },
)
```

### With Enforcement Mode

Set a minimum enforcement mode for the chain:

```python
envelope = guard.create_envelope(
    subject_did="did:web:agent-b.example.com",
    capability_class="tools.database.read",
    delegation_depth_remaining=1,
    enforcement_mode_min="EM-GUARD",  # Cannot be relaxed downstream
)
```

---

## Step 2: Derive a Child Envelope

When Agent B needs to further delegate to Agent C, it derives a child envelope. The child must be equal or narrower than the parent.

```python
# Agent B narrows the capability and passes to Agent C
child = guard.derive_envelope(
    parent_envelope_jws=envelope,
    subject_did="did:web:agent-c.example.com",
    capability_class="tools.database.read",  # Same or narrower
    delegation_depth_remaining=0,             # No further delegation
    expires_in_seconds=1800,                  # Shorter than parent
    constraints={
        "tables": ["users"],  # Narrower: only "users" table
        "max_rows": 100,      # More restrictive
    },
)
```

!!! warning "Narrowing Rules"
    - `capability_class` must be equal or narrower than the parent's
    - `delegation_depth_remaining` must be less than the parent's
    - `constraints` can only become more restrictive
    - `expires_in_seconds` cannot exceed the parent's remaining validity
    - `enforcement_mode_min` can only escalate (become stricter)

    Violations raise `ConfigurationError`.

---

## Step 3: Send a Delegated Request

Build HTTP headers that include the full chain and send them with your request:

```python
import httpx

# Build headers with the complete delegation chain
headers = guard.make_delegation_headers(
    chain=[envelope, child],  # Ordered: [root, ..., leaf]
    badge_map={
        # Map intermediate agent DIDs to their badge JWS
        "did:web:agent-b.example.com": agent_b_badge_jws,
    },
)

# Send the request — the gateway verifies the entire chain
response = httpx.post(
    "https://api.example.com/data",
    headers=headers,
    json={"query": "SELECT name FROM users LIMIT 10"},
)
```

The `make_delegation_headers()` method produces these headers:

| Header | Content |
|--------|---------|
| `X-Capiscio-Badge` | Your agent's badge JWS |
| `X-Capiscio-Authority` | Leaf envelope JWS |
| `X-Capiscio-Authority-Chain` | Base64url-encoded JSON array of the full chain |
| `X-Capiscio-Badge-Map` | JSON mapping of intermediate DIDs to badge JWS tokens |

---

## Step 4: Server-Side Verification

The CapiscIO gateway PEP automatically verifies delegation chains. No code changes are needed — just configure the gateway.

### Gateway Configuration

```bash
# Enable chain verification (on by default when gateway PEP is active)
export CAPISCIO_MAX_CHAIN_DEPTH=10          # Maximum chain depth (default: 10)
export CAPISCIO_ORG_TRUST_BOUNDARY=""       # Empty = accept cross-org chains
```

### What Gets Verified

The PEP performs these checks on every request with delegation headers:

1. Signature validity of each envelope in the chain
2. Hash chain integrity (each child references its parent)
3. Monotonic narrowing of capabilities, depth, and constraints
4. Leaf subject matches the caller's badge DID
5. Chain length within `MaxChainDepth`
6. All envelopes are within their validity period
7. Enforcement mode escalation is applied

### Error Responses

| Error Code | HTTP Status | Description |
|-----------|-------------|-------------|
| `ENVELOPE_CHAIN_TOO_DEEP` | 403 | Chain exceeds `MaxChainDepth` |
| `ENVELOPE_SIGNATURE_INVALID` | 401 | Envelope signature verification failed |
| `ENVELOPE_NARROWING_VIOLATION` | 403 | Child is wider than parent |
| `ENVELOPE_EXPIRED` | 401 | Envelope has expired |
| `ENVELOPE_DEPTH_EXCEEDED` | 403 | Delegation depth remaining is negative |

In `EM-OBSERVE` mode, chain verification failures are logged but the request proceeds.

---

## Full Example

A complete three-agent delegation:

```python
from capiscio_sdk import CapiscIO
import httpx

# Agent A: the orchestrator
agent_a = CapiscIO.connect(api_key="sk_live_aaa")
guard_a = agent_a.simple_guard()

# Create root envelope: A → B
root = guard_a.create_envelope(
    subject_did="did:web:agent-b.example.com",
    capability_class="tools.database.*",
    delegation_depth_remaining=2,
)

# Agent B: the middleware
agent_b = CapiscIO.connect(api_key="sk_live_bbb")
guard_b = agent_b.simple_guard()

# Derive child: B → C (narrowed to read-only)
child = guard_b.derive_envelope(
    parent_envelope_jws=root,
    subject_did="did:web:agent-c.example.com",
    capability_class="tools.database.read",
    delegation_depth_remaining=1,
)

# Agent C: the leaf executor
agent_c = CapiscIO.connect(api_key="sk_live_ccc")
guard_c = agent_c.simple_guard()

# C sends the delegated request
headers = guard_c.make_delegation_headers(
    chain=[root, child],
    badge_map={
        "did:web:agent-b.example.com": agent_b.get_badge(),
    },
)

response = httpx.post(
    "https://api.example.com/data",
    headers=headers,
    json={"query": "SELECT name FROM users"},
)
```

---

## See Also

- [Delegation Chains concept](../../concepts/delegation.md) — What are delegation chains and why they matter
- [Gateway setup](gateway-setup.md) — Deploy the CapiscIO security gateway
- [Policy enforcement config](../../reference/server/policy-enforcement.md) — Chain verification settings
- [RFC-008: Delegated Authority Envelopes](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/008-delegated-authority-envelopes.md) — Full specification
