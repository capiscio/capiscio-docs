---
title: Verify MCP Servers
description: Client-side guide for verifying MCP server identity before connecting.
---

# Verify MCP Servers (Client-Side)

Before connecting to an MCP server, verify its identity using its DID and trust badge.

## Verify a Server

```python
from capiscio_mcp import verify_server

result = await verify_server("did:web:example.com:mcp:my-server")

if result.verified:
    print(f"Trust level: {result.trust_level}")
    print(f"Issuer: {result.issuer}")
else:
    print(f"Verification failed: {result.reason}")
```

## Verification Checks

The client verifier performs the following checks:

1. **DID Resolution** — resolves the server's `did:web` to its DID Document
2. **Badge Validation** — verifies the JWS signature and claims
3. **Trust Level** — confirms the badge meets your minimum trust requirement
4. **Expiry** — ensures the badge has not expired
5. **Revocation** — checks the badge has not been revoked

## Configuration

```python
from capiscio_mcp import MCPClient

client = MCPClient(
    min_trust_level=2,
    require_pop=True,
    registry_url="https://registry.capisc.io",
)
```

## Next Steps

- [Server Registration](server-registration.md) — register your server's DID
- [Quickstart](../getting-started/quickstart.md) — end-to-end example
