# SDK API Source of Truth

**Generated from:** `/capiscio-sdk-python/capiscio_sdk/` source code  
**Date:** December 1, 2025  
**SDK Version:** 0.2.0

This document is the authoritative reference for all SDK APIs. All documentation MUST match this exactly.

---

## SimpleGuard Class

**File:** `capiscio_sdk/simple_guard.py`  
**Import:** `from capiscio_sdk.simple_guard import SimpleGuard` or `from capiscio_sdk import SimpleGuard`

### Constructor

```python
def __init__(
    self, 
    base_dir: Optional[Union[str, Path]] = None, 
    dev_mode: bool = False
) -> None
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_dir` | `str \| Path \| None` | `None` | Starting directory to search for config (defaults to cwd) |
| `dev_mode` | `bool` | `False` | If True, auto-generates keys and agent-card.json |

**DOES NOT ACCEPT:**
- ❌ `private_key_path` - DOES NOT EXIST
- ❌ `trust_store_path` - DOES NOT EXIST  
- ❌ `debug` - DOES NOT EXIST
- ❌ `key_id` / `kid` - DOES NOT EXIST

**Behavior:**
- Walks up directory tree from `base_dir` looking for `agent-card.json`
- Expects keys at `{project_root}/capiscio_keys/private.pem`
- Expects trust store at `{project_root}/capiscio_keys/trusted/`
- In `dev_mode=True`: auto-generates all missing files

---

### sign_outbound()

```python
def sign_outbound(self, payload: Dict[str, Any], body: Optional[bytes] = None) -> str
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `payload` | `Dict[str, Any]` | (required) | JWT claims to include in signature |
| `body` | `bytes \| None` | `None` | Optional HTTP body bytes for integrity binding (`bh` claim) |

**Returns:** `str` - Compact JWS string

**Auto-injected claims:**
- `iss` - Set to `self.agent_id` if not provided
- `iat` - Current timestamp
- `exp` - Current timestamp + 60 seconds
- `bh` - Base64url SHA-256 hash of body (if body provided)

---

### verify_inbound()

```python
def verify_inbound(self, jws: str, body: Optional[bytes] = None) -> Dict[str, Any]
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `jws` | `str` | (required) | The compact JWS string to verify |
| `body` | `bytes \| None` | `None` | Optional HTTP body bytes to verify against `bh` claim |

**Returns:** `Dict[str, Any]` - The verified JWT payload

**Raises:** `VerificationError` on any failure:
- Missing `kid` in header
- Untrusted key ID
- Invalid signature
- Body hash mismatch
- Expired token
- Clock skew

**DOES NOT ACCEPT:**
- ❌ `raise_on_failure` - DOES NOT EXIST (always raises)
- ❌ `signature` parameter name - it's `jws`

---

### make_headers()

```python
def make_headers(self, payload: Dict[str, Any], body: Optional[bytes] = None) -> Dict[str, str]
```

**Parameters:** Same as `sign_outbound()`

**Returns:** `Dict[str, str]` - `{"X-Capiscio-Badge": "<token>"}` (RFC-002 §9.1)

---

## Errors

**File:** `capiscio_sdk/errors.py`

| Error Class | Parent | Use Case |
|-------------|--------|----------|
| `CapiscioSecurityError` | `Exception` | Base class for all errors |
| `ConfigurationError` | `CapiscioSecurityError` | Missing keys, invalid paths |
| `VerificationError` | `CapiscioSecurityError` | Invalid signature, expired token, untrusted key |
| `CapiscioValidationError` | `CapiscioSecurityError` | Schema/protocol validation failed |
| `CapiscioSignatureError` | `CapiscioSecurityError` | Signature verification failed |
| `CapiscioRateLimitError` | `CapiscioSecurityError` | Rate limit exceeded |

**Import:** `from capiscio_sdk.errors import ConfigurationError, VerificationError`

---

## SecurityConfig Class

**File:** `capiscio_sdk/config.py`  
**Import:** `from capiscio_sdk import SecurityConfig`

### Class Methods (Presets)

```python
SecurityConfig.development()  # Permissive settings
SecurityConfig.production()   # Balanced settings  
SecurityConfig.strict()       # Maximum security
SecurityConfig.from_env()     # Load from environment variables
```

### DownstreamConfig Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `validate_schema` | `bool` | `True` | Validate message schema |
| `verify_signatures` | `bool` | `True` | Verify incoming signatures |
| `require_signatures` | `bool` | `False` | Reject unsigned requests |
| `check_protocol_compliance` | `bool` | `True` | Check A2A protocol |
| `enable_rate_limiting` | `bool` | `True` | Enable rate limiting |
| `rate_limit_requests_per_minute` | `int` | `60` | Rate limit threshold |

### UpstreamConfig Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `validate_agent_cards` | `bool` | `True` | Validate upstream agent cards |
| `verify_signatures` | `bool` | `True` | Verify upstream signatures |
| `require_signatures` | `bool` | `False` | Require upstream signatures |
| `test_endpoints` | `bool` | `False` | Test endpoint availability |
| `cache_validation` | `bool` | `True` | Cache validation results |
| `cache_timeout` | `int` | `3600` | Cache TTL in seconds |

---

## CapiscioSecurityExecutor Class

**File:** `capiscio_sdk/executor.py`  
**Import:** `from capiscio_sdk import CapiscioSecurityExecutor, secure, secure_agent`

### Constructor

```python
def __init__(
    self,
    delegate: Any,
    config: Optional[SecurityConfig] = None,
)
```

### Methods

```python
async def execute(self, context: RequestContext, event_queue: Any) -> None
async def cancel(self, context: RequestContext, event_queue: Any) -> None
async def validate_agent_card(self, url: str) -> ValidationResult
```

### Helper Functions

```python
# Wrap an executor
secured = secure(my_executor, config=SecurityConfig.production())

# Decorator pattern
@secure_agent(config=SecurityConfig.strict())
class MyAgent:
    ...
```

---

## File/Directory Conventions

SimpleGuard expects this structure (relative to project root):

```
project_root/
├── agent-card.json          # Agent identity card
└── capiscio_keys/
    ├── private.pem          # Ed25519 private key
    ├── public.pem           # Ed25519 public key
    └── trusted/             # Trust store directory
        ├── {kid1}.pem       # Trusted public key (filename = kid)
        └── {kid2}.pem
```

---

## Header Names (RFC-002 §9.1)

| Header | Value |
|--------|-------|
| `X-Capiscio-Badge` | Trust Badge token from `make_headers()` |
| `Authorization` | `Badge <token>` (alternative) |

---

## Constants

From `simple_guard.py`:
- `MAX_TOKEN_AGE = 60` seconds
- `CLOCK_SKEW_LEEWAY = 5` seconds
