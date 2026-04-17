---
title: Server Registration
description: Register your MCP server's identity with the CapiscIO registry.
---

# Server Registration

Register your MCP server's DID to establish its identity in the CapiscIO trust network.

## Generate a Keypair

```python
from capiscio_mcp import generate_server_keypair

keypair = generate_server_keypair()
print(f"DID: {keypair.did}")
print(f"Private key saved to: {keypair.key_path}")
```

## Register with the Registry

```python
from capiscio_mcp import register_server

result = await register_server(
    did="did:web:example.com:mcp:my-server",
    name="My MCP Server",
    description="Database access tools",
    registry_url="https://registry.capisc.io",
)
```

## Using the CLI

```bash
# Generate keypair
capiscio mcp keygen --did did:web:example.com:mcp:my-server

# Register server
capiscio mcp register \
    --did did:web:example.com:mcp:my-server \
    --name "My MCP Server"
```

## DID Format

MCP server DIDs follow the `did:web` method:

```
did:web:example.com:mcp:server-name
```

The DID Document is hosted at:

```
https://example.com/.well-known/did.json
```

## Next Steps

- [Server-Side Guide](server-side.md) — protect tools with the @guard decorator
- [Evidence Logging](evidence.md) — audit tool invocations
