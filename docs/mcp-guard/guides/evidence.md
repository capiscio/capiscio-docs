---
title: Evidence Logging
description: Configure cryptographic audit trails for MCP tool invocations.
---

# Evidence Logging

MCP Guard records a cryptographic audit trail for every tool invocation, enabling post-incident review and compliance reporting.

## How It Works

When a guarded tool is invoked, MCP Guard records:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 invocation time |
| `tool_name` | Name of the MCP tool called |
| `agent_did` | DID of the calling agent |
| `trust_level` | Agent's verified trust level |
| `badge_jti` | Badge ID used for verification |
| `result` | `allowed` or `denied` |
| `reason` | Denial reason (if denied) |

## Configuration

```python
from capiscio_mcp import configure_evidence

configure_evidence(
    enabled=True,
    output="file",           # "file", "stdout", or "http"
    path="./evidence.jsonl", # for file output
)
```

## Output Formats

### File (default)

Evidence records are appended to a JSONL file:

```json
{"timestamp":"2026-01-15T10:30:00Z","tool_name":"read_database","agent_did":"did:web:agent.example.com","trust_level":2,"result":"allowed"}
```

### HTTP

Send evidence to a remote collector:

```python
configure_evidence(
    output="http",
    endpoint="https://registry.capisc.io/v1/evidence",
)
```

## Next Steps

- [Server-Side Guide](server-side.md) — protect tools with trust levels
- [MCP SDK Integration](mcp-integration.md) — automatic evidence with FastMCP
