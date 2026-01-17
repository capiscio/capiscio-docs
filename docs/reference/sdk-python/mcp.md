---
title: MCP API
description: Model Context Protocol security enforcement for AI tool access control
---

# MCP API

The MCP API provides security enforcement for Model Context Protocol servers and clients, implementing RFC-006 (Tool Authority) and RFC-007 (Server Identity).

!!! info "RFC Implementation"
    This API implements RFC-006: MCP Tool Authority (agent access control) and RFC-007: MCP Server Identity (server verification).

---

## Quick Start

```python
from capiscio_sdk._rpc.client import CapiscioRPCClient

# Connect to capiscio-core
client = CapiscioRPCClient()
client.connect()

# Evaluate tool access for an incoming request
result = client.mcp.evaluate_tool_access(
    tool_name="write_file",
    badge_jws=incoming_badge,
    server_origin="https://files.example.com",
    min_trust_level=1,  # Require at least DV
)

if result["decision"] == "allow":
    print(f"✅ Access granted for agent {result['agent_did']}")
else:
    print(f"❌ Access denied: {result['deny_reason']}")
```

---

## Access Pattern

The `MCPClient` is accessed via the `CapiscioRPCClient.mcp` property:

```python
from capiscio_sdk._rpc.client import CapiscioRPCClient

client = CapiscioRPCClient()
client.connect()

# Access MCP client
mcp = client.mcp

# Now use MCP methods
result = mcp.evaluate_tool_access(tool_name="read_file")
```

---

## Functions

### evaluate_tool_access

Evaluate whether a caller is authorized to invoke an MCP tool (RFC-006 §6.2-6.4).

```python
def evaluate_tool_access(
    tool_name: str,
    params_hash: str = "",
    server_origin: str = "",
    *,
    badge_jws: Optional[str] = None,
    api_key: Optional[str] = None,
    policy_version: str = "",
    trusted_issuers: Optional[list[str]] = None,
    min_trust_level: int = 0,
    accept_level_zero: bool = False,
    allowed_tools: Optional[list[str]] = None,
) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `tool_name` | `str` | Name of the MCP tool being invoked |
| `params_hash` | `str` | SHA-256 hash of tool parameters (for audit trail) |
| `server_origin` | `str` | Origin of the MCP server (e.g., `https://files.example.com`) |
| `badge_jws` | `str` | Caller's Trust Badge JWT for badge-based auth |
| `api_key` | `str` | Caller's API key for key-based auth |
| `policy_version` | `str` | Optional policy version to apply |
| `trusted_issuers` | `list[str]` | List of trusted badge issuer URLs |
| `min_trust_level` | `int` | Minimum required trust level (0-4) |
| `accept_level_zero` | `bool` | Accept self-signed (Level 0) badges |
| `allowed_tools` | `list[str]` | Explicit allowlist of tool names |

**Returns:** `dict` with evaluation result:

| Key | Type | Description |
|-----|------|-------------|
| `decision` | `str` | `"allow"` or `"deny"` |
| `deny_reason` | `str` | Reason code if denied (see table below) |
| `deny_detail` | `str` | Human-readable error message |
| `agent_did` | `str` | Authenticated agent's DID |
| `badge_jti` | `str` | Badge unique identifier |
| `auth_level` | `str` | `"anonymous"`, `"api_key"`, or `"badge"` |
| `trust_level` | `int` | Agent's trust level (0-4) |
| `evidence_json` | `str` | RFC-006 §7 evidence record |
| `evidence_id` | `str` | Unique evidence record ID |
| `timestamp` | `str` | Evaluation timestamp (ISO 8601) |

**Deny Reasons:**

| Code | Description |
|------|-------------|
| `badge_missing` | No badge or API key provided |
| `badge_invalid` | Badge signature verification failed |
| `badge_expired` | Badge has expired |
| `badge_revoked` | Badge has been revoked |
| `trust_insufficient` | Trust level below minimum |
| `tool_not_allowed` | Tool not in allowed list |
| `issuer_untrusted` | Badge issuer not trusted |
| `policy_denied` | Policy explicitly denied access |

**Example:**

```python
import hashlib
import json

# Evaluate with badge authentication
result = client.mcp.evaluate_tool_access(
    tool_name="write_file",
    params_hash=hashlib.sha256(json.dumps({"path": "/tmp/test.txt"}).encode()).hexdigest(),
    server_origin="https://files.example.com",
    badge_jws=badge_token,
    min_trust_level=2,  # Require OV or higher
    trusted_issuers=["https://registry.capisc.io"],
)

if result["decision"] == "allow":
    # Proceed with tool execution
    execute_tool(tool_name, params)
else:
    raise PermissionError(f"{result['deny_reason']}: {result['deny_detail']}")
```

---

### verify_server_identity

Verify an MCP server's identity before trusting its responses (RFC-007 §7.2).

```python
def verify_server_identity(
    server_did: str,
    server_badge: str = "",
    transport_origin: str = "",
    endpoint_path: str = "",
    *,
    trusted_issuers: Optional[list[str]] = None,
    min_trust_level: int = 0,
    accept_level_zero: bool = False,
    offline_mode: bool = False,
    skip_origin_binding: bool = False,
) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `server_did` | `str` | Server's DID (`did:web:...` or `did:key:...`) |
| `server_badge` | `str` | Server's Trust Badge JWT (optional for Level 0) |
| `transport_origin` | `str` | Origin from transport (e.g., `https://files.example.com`) |
| `endpoint_path` | `str` | Endpoint path being accessed |
| `trusted_issuers` | `list[str]` | Trusted badge issuer URLs |
| `min_trust_level` | `int` | Minimum required trust level (0-4) |
| `accept_level_zero` | `bool` | Accept self-signed servers |
| `offline_mode` | `bool` | Use cache only, skip online checks |
| `skip_origin_binding` | `bool` | Skip RFC-007 §5.3 origin binding check |

**Returns:** `dict` with verification result:

| Key | Type | Description |
|-----|------|-------------|
| `state` | `str` | Server state (see table below) |
| `trust_level` | `int` | Server's trust level (0-4) |
| `server_did` | `str` | Verified server DID |
| `badge_jti` | `str` | Server badge identifier |
| `error_code` | `str` | Error code if verification failed |
| `error_detail` | `str` | Human-readable error message |

**Server States (RFC-007 §7.3):**

| State | Description | Trust |
|-------|-------------|-------|
| `verified_principal` | DID verified, badge valid, origin matches | High |
| `declared_principal` | DID provided but not fully verified | Medium |
| `unverified_origin` | Origin doesn't match DID or badge | Low |

**Error Codes:**

| Code | Description |
|------|-------------|
| `did_invalid` | Invalid DID format |
| `badge_invalid` | Badge signature verification failed |
| `badge_expired` | Server badge has expired |
| `badge_revoked` | Server badge has been revoked |
| `trust_insufficient` | Trust level below minimum |
| `origin_mismatch` | Transport origin doesn't match DID |
| `path_mismatch` | Endpoint path doesn't match badge scope |
| `issuer_untrusted` | Badge issuer not trusted |

**Example:**

```python
# Verify server before trusting tool results
result = client.mcp.verify_server_identity(
    server_did="did:web:files.example.com:mcp:files",
    server_badge=server_badge_token,
    transport_origin="https://files.example.com",
    min_trust_level=1,  # Require at least DV
)

if result["state"] == "verified_principal":
    print(f"✅ Server verified at trust level {result['trust_level']}")
    # Trust the server's responses
else:
    print(f"⚠️ Server not fully verified: {result['error_detail']}")
    # Prompt user for confirmation or reject
```

---

### parse_server_identity_http

Extract server identity from HTTP response headers (RFC-007 §5.2).

```python
def parse_server_identity_http(
    capiscio_server_did: str = "",
    capiscio_server_badge: str = "",
) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `capiscio_server_did` | `str` | Value of `Capiscio-Server-DID` header |
| `capiscio_server_badge` | `str` | Value of `Capiscio-Server-Badge` header |

**Returns:** `dict`:

| Key | Type | Description |
|-----|------|-------------|
| `server_did` | `str` | Extracted server DID |
| `server_badge` | `str` | Extracted server badge JWT |
| `identity_present` | `bool` | Whether identity headers were present |

**Example:**

```python
import requests

# Make request to MCP server
response = requests.post("https://files.example.com/mcp/tools/read_file", ...)

# Parse identity from response headers
identity = client.mcp.parse_server_identity_http(
    capiscio_server_did=response.headers.get("Capiscio-Server-DID", ""),
    capiscio_server_badge=response.headers.get("Capiscio-Server-Badge", ""),
)

if identity["identity_present"]:
    # Verify the server identity
    verification = client.mcp.verify_server_identity(
        server_did=identity["server_did"],
        server_badge=identity["server_badge"],
        transport_origin="https://files.example.com",
    )
```

---

### parse_server_identity_jsonrpc

Extract server identity from JSON-RPC `_meta` field (RFC-007 §5.3).

```python
def parse_server_identity_jsonrpc(meta_json: str) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `meta_json` | `str` | JSON string of the `_meta` object |

**Returns:** `dict`:

| Key | Type | Description |
|-----|------|-------------|
| `server_did` | `str` | Extracted server DID |
| `server_badge` | `str` | Extracted server badge JWT |
| `identity_present` | `bool` | Whether identity was present in `_meta` |

**Example:**

```python
import json

# JSON-RPC response from stdio MCP server
response = {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {"content": "..."},
    "_meta": {
        "serverDid": "did:web:files.example.com:mcp:files",
        "serverBadge": "eyJhbGciOiJFZERTQSI..."
    }
}

# Parse identity from _meta
identity = client.mcp.parse_server_identity_jsonrpc(
    meta_json=json.dumps(response.get("_meta", {}))
)

if identity["identity_present"]:
    # Verify the server
    verification = client.mcp.verify_server_identity(
        server_did=identity["server_did"],
        server_badge=identity["server_badge"],
    )
```

---

### health

Check MCP service health and version compatibility.

```python
def health(client_version: str = "") -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `client_version` | `str` | Client version for compatibility check |

**Returns:** `dict`:

| Key | Type | Description |
|-----|------|-------------|
| `healthy` | `bool` | Whether service is healthy |
| `core_version` | `str` | capiscio-core version |
| `proto_version` | `str` | Protocol buffer version |
| `version_compatible` | `bool` | Whether versions are compatible |

**Example:**

```python
status = client.mcp.health(client_version="capiscio-sdk-python/2.5.0")

if status["healthy"]:
    print(f"✅ MCP service healthy (core {status['core_version']})")
else:
    print("❌ MCP service unhealthy")
```

---

## Trust Levels

MCP enforces CapiscIO trust levels (RFC-002):

| Level | Name | Description | Use Case |
|-------|------|-------------|----------|
| **0** | Self-Signed | `did:key` only, no CA | Development, testing |
| **1** | Registered | Account verified by CA | Internal tools |
| **2** | Domain Validated (DV) | DNS/HTTP challenge | Production B2B |
| **3** | Organization Validated (OV) | Legal entity verified | High-trust ops |
| **4** | Extended Validated (EV) | Security audit completed | Regulated industries |

```python
# Require different trust levels for different tools
sensitive_tools = ["execute_shell", "delete_file", "modify_system"]

if tool_name in sensitive_tools:
    min_level = 3  # Require OV for dangerous tools
else:
    min_level = 1  # DV sufficient for normal tools

result = client.mcp.evaluate_tool_access(
    tool_name=tool_name,
    badge_jws=badge,
    min_trust_level=min_level,
)
```

---

## Patterns

### MCP Server Middleware (FastAPI + SSE)

```python
from fastapi import FastAPI, Request, HTTPException
from capiscio_sdk._rpc.client import CapiscioRPCClient

app = FastAPI()
client = CapiscioRPCClient()
client.connect()

@app.middleware("http")
async def mcp_auth(request: Request, call_next):
    # Skip auth for health/docs
    if request.url.path in ["/health", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    # Extract badge from Authorization header
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing badge token")
    
    badge = auth[7:]
    
    # Extract tool name from path (e.g., /tools/read_file)
    tool_name = request.url.path.split("/")[-1]
    
    # Evaluate access
    result = client.mcp.evaluate_tool_access(
        tool_name=tool_name,
        badge_jws=badge,
        server_origin=str(request.base_url).rstrip("/"),
        min_trust_level=1,
        trusted_issuers=["https://registry.capisc.io"],
    )
    
    if result["decision"] != "allow":
        raise HTTPException(
            403,
            detail={
                "error": "access_denied",
                "reason": result["deny_reason"],
                "detail": result["deny_detail"],
            }
        )
    
    # Attach agent info to request
    request.state.agent_did = result["agent_did"]
    request.state.trust_level = result["trust_level"]
    
    return await call_next(request)
```

### MCP Client Verification

```python
from capiscio_sdk._rpc.client import CapiscioRPCClient
import requests

client = CapiscioRPCClient()
client.connect()

def call_mcp_tool(server_url: str, tool_name: str, params: dict) -> dict:
    """Call an MCP tool with server identity verification."""
    
    # Make the tool call
    response = requests.post(
        f"{server_url}/tools/{tool_name}",
        json=params,
        headers={"Authorization": f"Bearer {my_badge}"},
    )
    
    # Parse and verify server identity
    identity = client.mcp.parse_server_identity_http(
        capiscio_server_did=response.headers.get("Capiscio-Server-DID", ""),
        capiscio_server_badge=response.headers.get("Capiscio-Server-Badge", ""),
    )
    
    if not identity["identity_present"]:
        raise ValueError("Server did not provide identity headers")
    
    verification = client.mcp.verify_server_identity(
        server_did=identity["server_did"],
        server_badge=identity["server_badge"],
        transport_origin=server_url,
        min_trust_level=1,
    )
    
    if verification["state"] != "verified_principal":
        raise ValueError(f"Server verification failed: {verification['error_detail']}")
    
    return response.json()
```

### Tool Allowlist Enforcement

```python
# Define allowed tools per trust level
TOOL_ALLOWLIST = {
    0: ["read_file", "list_directory"],  # Level 0: read-only
    1: ["read_file", "list_directory", "search"],  # Level 1: + search
    2: ["read_file", "list_directory", "search", "write_file"],  # Level 2: + write
    3: ["read_file", "list_directory", "search", "write_file", "execute"],  # Level 3: + execute
}

def get_allowed_tools(trust_level: int) -> list[str]:
    """Get allowed tools for a trust level."""
    return TOOL_ALLOWLIST.get(trust_level, TOOL_ALLOWLIST[0])

# Use in evaluation
result = client.mcp.evaluate_tool_access(
    tool_name=requested_tool,
    badge_jws=badge,
    allowed_tools=get_allowed_tools(caller_trust_level),
)
```

---

## Error Handling

```python
from grpc import RpcError, StatusCode

try:
    result = client.mcp.evaluate_tool_access(
        tool_name="write_file",
        badge_jws=badge,
    )
except RpcError as e:
    if e.code() == StatusCode.UNAVAILABLE:
        print("MCP service unavailable - check capiscio-core is running")
    elif e.code() == StatusCode.INVALID_ARGUMENT:
        print(f"Invalid request: {e.details()}")
    else:
        raise
```

---

## See Also

- [gRPC Services: MCPService](../grpc.md#mcpservice) — Low-level gRPC API
- [Trust Badges](../../how-to/security/badges.md) — Badge issuance and verification
- [Trust Model](../../concepts/trust-model.md) — Trust levels explained
- [Server Registration](../../mcp-guard/guides/server-registration.md) — MCP Guard server identity registration
- [RFC-006: MCP Tool Authority](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/006-mcp-tool-authority.md) — Specification
- [RFC-007: MCP Server Identity](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/007-mcp-server-identity.md) — Specification
