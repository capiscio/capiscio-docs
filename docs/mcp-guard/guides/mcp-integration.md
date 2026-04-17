---
title: MCP SDK Integration
description: Integrate CapiscIO MCP Guard with the FastMCP SDK for automatic tool protection.
---

# MCP SDK Integration

Integrate MCP Guard with the [FastMCP](https://github.com/jlowin/fastmcp) SDK for automatic tool wrapping and evidence logging.

## Installation

```bash
pip install capiscio-mcp[mcp]
```

## Usage with FastMCP

```python
from fastmcp import FastMCP
from capiscio_mcp.mcp import SecureMCP

# Wrap your FastMCP server with MCP Guard
mcp = FastMCP("My Server")
secure = SecureMCP(mcp, min_trust_level=1)

@secure.tool()
async def query_database(sql: str) -> list[dict]:
    """All tools registered via secure.tool() are automatically guarded."""
    return await db.execute(sql)
```

## How It Works

`SecureMCP` wraps the FastMCP server and:

1. Intercepts incoming tool calls
2. Extracts the agent's badge from the request context
3. Verifies the badge signature, trust level, and expiry
4. Logs evidence for the invocation
5. Forwards the call to the original tool if verification passes

## Configuration

```python
secure = SecureMCP(
    mcp,
    min_trust_level=2,
    require_pop=True,
    evidence_enabled=True,
    registry_url="https://registry.capisc.io",
)
```

## Next Steps

- [Server-Side Guide](server-side.md) — manual guard decorator usage
- [Evidence Logging](evidence.md) — configure audit trails
- [Server Registration](server-registration.md) — register your server DID
