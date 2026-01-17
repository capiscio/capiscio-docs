# How CapiscIO Works

CapiscIO provides a complete trust infrastructure for AI agents. Here's how the pieces fit together.

## The Problem

AI agents are exploding in capability and prevalence. But there's a trust gap:

> **Agent A** says: *"I'm Weather Bot v2.1"*
>
> **Agent B** asks: *"Should I trust this?"*

- :octicons-x-circle-16: Self-descriptions can be forged
- :octicons-x-circle-16: API keys prove payment, not identity  
- :octicons-x-circle-16: No standard verification mechanism

## The Solution: Three Layers of Trust

CapiscIO provides three products that work together:

| Product | Phase | What It Does |
|---------|-------|--------------|
| **CapiscIO Core** | Build time | CLI for validation, key generation, badge issuance |
| **CapiscIO SDK** | Runtime | Sign requests, verify callers, enforce trust |
| **MCP Guard** | Runtime | Protect MCP tools with trust-level authorization |

**How they connect:** Core produces badges → SDK uses badges at runtime → MCP Guard extends SDK for MCP tools

### 1. CapiscIO Core (CLI)

**What it does:** Build-time validation and badge management.

```bash
# Validate your A2A agent card
capiscio validate agent-card.json
# ✅ Score: 95/100 (A+)

# Generate cryptographic keys
capiscio key gen --did did:key
# ✅ did:key:z6Mk...

# Issue a trust badge
capiscio badge issue --level 0 --self-sign
# ✅ Badge written to badge.jwt
```

**Use cases:**

- CI/CD validation gates
- Pre-deployment checks
- Badge issuance pipeline
- Key management

[:octicons-arrow-right-24: CLI Reference](../reference/cli/index.md)

---

### 2. CapiscIO SDK (Python)

**What it does:** Runtime security enforcement for your agent.

```python
from capiscio_sdk import SimpleGuard, sign_request, verify_request

# 1. Protect your endpoints
guard = SimpleGuard(min_trust_level=2)

@app.post("/task")
@guard.protect
async def handle_task(request):
    # Only Level 2+ agents reach here
    caller = guard.get_caller_identity(request)
    return await process_task(request)

# 2. Sign your outbound requests
signed = await sign_request(request, badge=my_badge)

# 3. Verify incoming requests
result = await verify_request(request)
if result.trust_level >= 2:
    allow_access()
```

**Use cases:**

- API authentication & authorization
- Request signing
- Trust level enforcement
- Audit logging

[:octicons-arrow-right-24: Python SDK](../reference/sdk-python/index.md)

---

### 3. MCP Guard

**What it does:** Trust-level authorization for [Model Context Protocol](https://modelcontextprotocol.io) tool calls.

```python
from capiscio_mcp import guard

# Protect individual tools
@guard(min_trust_level=2)
async def read_database(query: str):
    """Only Level 2+ agents can query."""
    return await db.execute(query)

@guard(min_trust_level=3)
async def write_database(table: str, data: dict):
    """Only Level 3+ agents can write."""
    return await db.insert(table, data)
```

**Use cases:**

- Protecting MCP servers
- Tool-level authorization
- Client-server identity verification
- Cryptographic audit trails

[:octicons-arrow-right-24: MCP Guard](../mcp-guard/index.md)

---

## The Trust Flow

Here's how trust flows through a typical interaction:

| Step | What Happens | Code |
|:----:|--------------|------|
| **1** | Generate DID and cryptographic keypair | `capiscio key gen` |
| **2** | Registry issues trust badge (Level 0-4) | `capiscio badge issue` |
| **3** | Sign outbound requests with badge | `sign_request()` |
| **4** | Verify signature and enforce trust level | `@guard.protect` |

---

## Trust Levels

CapiscIO uses a 5-level trust hierarchy (like SSL certificates):

| Level | Name | What's Verified | Use Case |
|:-----:|------|-----------------|----------|
| **0** | Self-Signed | Cryptographic identity only | Development, testing |
| **1** | Registered | Email verification | Personal projects |
| **2** | Domain Validated | Domain ownership (DNS) | Production APIs |
| **3** | Org Validated | Legal entity verification | Enterprise |
| **4** | Extended Validation | Enhanced due diligence | Regulated industries |

**The key insight:** Higher levels require more verification but enable more sensitive operations.

```python
# Development: Accept any cryptographic identity
@guard.protect(min_trust_level=0)
async def public_endpoint(): ...

# Production: Require verified domain
@guard.protect(min_trust_level=2)
async def internal_api(): ...

# Enterprise: Require verified organization
@guard.protect(min_trust_level=3)
async def financial_operation(): ...
```

---

## Installation Paths

Depending on your use case:

=== "Validate Agent Cards"

    ```bash
    pip install capiscio   # or: npm install -g capiscio
    capiscio validate agent-card.json
    ```

=== "Secure Python APIs"

    ```bash
    pip install capiscio-sdk
    ```

    ```python
    from capiscio_sdk import SimpleGuard
    guard = SimpleGuard(min_trust_level=2)
    ```

=== "Protect MCP Tools"

    ```bash
    pip install capiscio-mcp
    ```

    ```python
    from capiscio_mcp import guard
    @guard(min_trust_level=2)
    async def my_tool(): ...
    ```

=== "CI/CD Integration"

    ```yaml
    # .github/workflows/validate.yml
    - uses: capiscio/validate-a2a@v2
      with:
        path: agent-card.json
        min-score: 80
    ```

---

## What's Next?

<div class="grid cards" markdown>

-   [:material-rocket-launch: **Getting Started**](../getting-started/index.md)

    Pick a tutorial based on your goal

-   [:material-book-open: **Concepts**](../concepts/index.md)

    Deep dive into DIDs, badges, and trust

-   [:material-clipboard-list: **How-To Guides**](../how-to/index.md)

    Specific recipes for common tasks

</div>
