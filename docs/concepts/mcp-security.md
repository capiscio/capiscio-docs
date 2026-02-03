# MCP Security

The Model Context Protocol (MCP) enables powerful tool access for AI agents. CapiscIO's **MCP Guard** brings trust infrastructure to MCP with two complementary specifications.

## The Problem

MCP servers expose powerful tools to autonomous agents—file systems, databases, APIs, code execution. But MCP itself doesn't define:

- **Who** is calling a tool (authentication)
- **Whether** they should have access (authorization)
- **What** happened for post-incident review (audit)

## The Solution: Two RFCs

MCP Guard implements two CapiscIO specifications:

### RFC-006: MCP Tool Authority and Evidence

**Server-side protection.** Define trust level requirements for individual tools.

```python
from capiscio_mcp import guard

@guard(min_trust_level=2)
async def read_database(query: str) -> list[dict]:
    """Only Level 2+ agents can query the database."""
    return await db.execute(query)

@guard(min_trust_level=3)
async def write_database(table: str, data: dict):
    """Only Level 3+ (org-validated) agents can write."""
    return await db.insert(table, data)
```

**Key features:**

- **Trust level enforcement** — Require minimum verification level
- **Evidence logging** — Cryptographic audit trail for every call
- **Parameter hashing** — PII-safe evidence records
- **Async and sync** — Both decorator styles supported

[:octicons-arrow-right-24: RFC-006 Full Specification](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/006-mcp-tool-authority-evidence.md)

---

### RFC-007: MCP Server Identity Disclosure

**Client-side verification.** Verify MCP server identity before connecting.

```python
from capiscio_mcp import verify_server, ServerState

result = await verify_server(
    server_did="did:web:mcp.example.com",
    server_badge="eyJhbGc...",
    transport_origin="https://mcp.example.com",
)

if result.state == ServerState.VERIFIED_PRINCIPAL:
    print(f"✓ Trusted server at Level {result.trust_level}")
else:
    print("⚠ Server identity not verified")
```

**Key features:**

- **Server identity verification** — Confirm who you're connecting to
- **Transport binding** — Verify server controls the transport endpoint
- **Trust level inspection** — Check server's verification level
- **Three states** — VERIFIED_PRINCIPAL, DECLARED_PRINCIPAL, UNVERIFIED_ORIGIN

[:octicons-arrow-right-24: RFC-007 Full Specification](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/007-mcp-server-identity-discovery.md)

---

## How They Work Together

```
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Security Flow                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   MCP CLIENT                              MCP SERVER             │
│   ┌─────────────┐                        ┌─────────────┐        │
│   │  Agent A    │                        │  File Tool  │        │
│   │  (Level 2)  │                        │  Server     │        │
│   └─────────────┘                        └─────────────┘        │
│         │                                       │                │
│         │  1. Verify server identity            │                │
│         │     (RFC-007)                         │                │
│         │ ─────────────────────────────────────>│                │
│         │                                       │                │
│         │  2. Call tool with badge              │                │
│         │ ─────────────────────────────────────>│                │
│         │                                       │                │
│         │                   3. Guard evaluates  │                │
│         │                      (RFC-006)        │                │
│         │                                       ▼                │
│         │                              ┌─────────────┐           │
│         │                              │ @guard(2)   │           │
│         │                              │ → ALLOW     │           │
│         │                              │ → log audit │           │
│         │                              └─────────────┘           │
│         │                                       │                │
│         │  4. Return result                     │                │
│         │ <─────────────────────────────────────│                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

1. **Client verifies server** using RFC-007 before connecting
2. **Client calls tool** with their trust badge attached
3. **Server guard evaluates** the caller's trust level (RFC-006)
4. **Evidence logged** regardless of allow/deny decision

---

## Trust Levels in MCP Context

| Level | Server Use | Client Use |
|:-----:|------------|------------|
| **0** | Development servers | Anonymous tool access |
| **1** | Personal project servers | Registered agents |
| **2** | Production read-only tools | Domain-verified agents |
| **3** | Write operations | Org-verified agents |
| **4** | Admin tools | Enterprise agents |

---

## Next Steps

<div class="grid cards" markdown>

-   [:material-shield-check: **Protect Your Tools**](../mcp-guard/guides/server-side.md)

    Add `@guard` to your MCP server tools

-   [:material-check-decagram: **Verify Servers**](../mcp-guard/guides/client-side.md)

    Implement server verification in your MCP client

-   [:material-file-document: **Evidence Logging**](../mcp-guard/guides/evidence.md)

    Set up cryptographic audit trails

-   [:material-api: **API Reference**](../reference/sdk-python/mcp.md)

    Complete MCP Guard API documentation

</div>
