---
title: Protect MCP Tools
description: Server-side guide for protecting MCP tools with the @guard decorator.
---

# Protect MCP Tools (Server-Side)

Use the `@guard` decorator to enforce trust-level requirements on your MCP tool functions.

## Basic Usage

```python
from capiscio_mcp import guard

@guard(min_trust_level=2)
async def sensitive_operation(data: str) -> dict:
    """Requires Trust Level 2 or higher."""
    return {"status": "ok"}
```

## Synchronous Tools

```python
from capiscio_mcp import guard_sync

@guard_sync(min_trust_level=1)
def read_config(key: str) -> str:
    """Synchronous tool with trust verification."""
    return config[key]
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_trust_level` | `int` | `1` | Minimum trust level required (0-3) |
| `require_pop` | `bool` | `False` | Require Proof of Possession (RFC-003) |
| `evidence` | `bool` | `True` | Log evidence for this invocation |

## Error Handling

When a badge fails verification, the guard raises `GuardError` with a descriptive message:

```python
from capiscio_mcp.errors import GuardError

try:
    result = await guarded_tool("input")
except GuardError as e:
    print(f"Access denied: {e}")
```

## Next Steps

- [Evidence Logging](evidence.md) — configure audit trails
- [MCP SDK Integration](mcp-integration.md) — automatic FastMCP wrapping
