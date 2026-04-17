---
title: Quickstart
description: Protect your first MCP tool with CapiscIO trust badges in 5 minutes.
---

# Quickstart

Protect your MCP tools with trust-level requirements using the `@guard` decorator.

## Server-Side: Protect a Tool

```python
from capiscio_mcp import guard

@guard(min_trust_level=2)
async def read_database(query: str) -> list[dict]:
    """Only agents with Trust Level 2+ can execute this tool."""
    # ... your tool logic
    pass
```

## Client-Side: Verify a Server

```python
from capiscio_mcp import verify_server

result = await verify_server("did:web:example.com:mcp:my-server")
if result.verified:
    print(f"Server trust level: {result.trust_level}")
```

## How It Works

1. **Agent sends badge** — the calling agent presents its CapiscIO trust badge
2. **Guard verifies** — `@guard` checks the badge signature, expiry, and trust level
3. **Evidence logged** — every invocation is recorded with a cryptographic audit trail
4. **Tool executes** — if verification passes, the tool runs normally

## Trust Levels

| Level | Name | Meaning |
|-------|------|---------|
| 0 | Self-Signed | Agent generated its own badge |
| 1 | Domain Verified | Agent proved control of its DID |
| 2 | Organization Verified | Agent's organization has been verified |
| 3 | Extended Validation | Full identity verification completed |

## Next Steps

- [Server-Side Guide](../guides/server-side.md) — detailed guard configuration
- [Client-Side Guide](../guides/client-side.md) — verify MCP servers before connecting
- [Evidence Logging](../guides/evidence.md) — audit trail configuration
