---
title: Configuration Reference
description: Configuration options for the Capiscio SDK
---

# Configuration Reference

This page documents all configuration options for the Capiscio Python SDK.

!!! info "Auto-Generated Reference"
    For the most accurate API documentation, see the [SDK Reference](./sdk-python/index.md) which is auto-generated from source code.

---

## SimpleGuard Configuration

SimpleGuard uses **convention over configuration**. It auto-discovers keys based on directory structure.

### Constructor Parameters

```python
from capiscio_sdk import SimpleGuard

guard = SimpleGuard(
    base_dir=None,     # Optional: Starting directory (defaults to cwd)
    dev_mode=False,    # Optional: Auto-generate keys if missing
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_dir` | `str \| Path \| None` | `None` | Directory to search for config (defaults to current working directory) |
| `dev_mode` | `bool` | `False` | If `True`, auto-generates keys and agent-card.json |

### Expected Directory Structure

SimpleGuard walks up from `base_dir` looking for `agent-card.json`:

```
your-project/              # ← SimpleGuard finds this via walk-up
├── agent-card.json        # Agent identity (required)
└── capiscio_keys/
    ├── private.pem        # Ed25519 private key (required for signing)
    ├── public.pem         # Ed25519 public key
    └── trusted/           # Trust store directory
        ├── partner-a.pem  # Trusted public key (filename = kid)
        └── partner-b.pem
```

### Development vs Production

=== "Development"

    ```python
    # Auto-generates all missing files
    guard = SimpleGuard(dev_mode=True)
    ```
    
    - Creates `agent-card.json` with default values
    - Generates Ed25519 keypair
    - Adds self-trust for local testing

=== "Production"

    ```python
    # Requires existing keys
    guard = SimpleGuard()  # dev_mode=False by default
    
    # Or specify config location
    guard = SimpleGuard(base_dir="/etc/capiscio")
    ```
    
    - Raises `ConfigurationError` if keys missing
    - No auto-generation

---

## SecurityConfig

Configuration for `CapiscioSecurityExecutor`. Controls security behavior for incoming and outgoing requests.

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `downstream` | `DownstreamConfig` | `DownstreamConfig()` | Incoming request settings |
| `upstream` | `UpstreamConfig` | `UpstreamConfig()` | Outgoing request settings |
| `strict_mode` | `bool` | `False` | Enable strict validation |
| `fail_mode` | `"block" \| "monitor" \| "log"` | `"block"` | How to handle failures |
| `log_validation_failures` | `bool` | `True` | Log validation failures |
| `timeout_ms` | `int` | `5000` | Request timeout in milliseconds |

### Presets

```python
from capiscio_sdk import SecurityConfig

# Development - permissive, logs instead of blocking
config = SecurityConfig.development()

# Production - balanced security
config = SecurityConfig.production()

# Strict - maximum security
config = SecurityConfig.strict()

# From environment variables
config = SecurityConfig.from_env()
```

---

## DownstreamConfig

Controls how incoming requests are validated.

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `validate_schema` | `bool` | `True` | Validate A2A message schema |
| `verify_signatures` | `bool` | `True` | Verify request signatures |
| `require_signatures` | `bool` | `False` | Reject unsigned requests |
| `check_protocol_compliance` | `bool` | `True` | Check A2A protocol compliance |
| `enable_rate_limiting` | `bool` | `True` | Enable rate limiting |
| `rate_limit_requests_per_minute` | `int` | `60` | Rate limit threshold |

### Example

```python
from capiscio_sdk import DownstreamConfig

downstream = DownstreamConfig(
    validate_schema=True,
    verify_signatures=True,
    require_signatures=True,  # Strict: reject unsigned
    enable_rate_limiting=True,
    rate_limit_requests_per_minute=100,
)
```

---

## UpstreamConfig

Controls how outgoing requests to other agents are handled.

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `validate_agent_cards` | `bool` | `True` | Validate upstream agent cards |
| `verify_signatures` | `bool` | `True` | Verify response signatures |
| `require_signatures` | `bool` | `False` | Reject unsigned responses |
| `test_endpoints` | `bool` | `False` | Test endpoint availability (slow) |
| `cache_validation` | `bool` | `True` | Cache validation results |
| `cache_timeout` | `int` | `3600` | Cache TTL in seconds |

### Example

```python
from capiscio_sdk import UpstreamConfig

upstream = UpstreamConfig(
    validate_agent_cards=True,
    verify_signatures=True,
    require_signatures=False,
    cache_validation=True,
    cache_timeout=1800,  # 30 minutes
)
```

---

## Environment Variables

`SecurityConfig.from_env()` reads these environment variables:

| Variable | Type | Default | Maps To |
|----------|------|---------|---------|
| `CAPISCIO_VALIDATE_SCHEMA` | `bool` | `true` | `downstream.validate_schema` |
| `CAPISCIO_VERIFY_SIGNATURES` | `bool` | `true` | `downstream.verify_signatures` |
| `CAPISCIO_REQUIRE_SIGNATURES` | `bool` | `false` | `downstream.require_signatures` |
| `CAPISCIO_RATE_LIMITING` | `bool` | `true` | `downstream.enable_rate_limiting` |
| `CAPISCIO_RATE_LIMIT_RPM` | `int` | `60` | `downstream.rate_limit_requests_per_minute` |
| `CAPISCIO_VALIDATE_UPSTREAM` | `bool` | `true` | `upstream.validate_agent_cards` |
| `CAPISCIO_VERIFY_UPSTREAM_SIGNATURES` | `bool` | `true` | `upstream.verify_signatures` |
| `CAPISCIO_CACHE_VALIDATION` | `bool` | `true` | `upstream.cache_validation` |
| `CAPISCIO_FAIL_MODE` | `string` | `block` | `fail_mode` |
| `CAPISCIO_TIMEOUT_MS` | `int` | `5000` | `timeout_ms` |

### Example

```bash
# Production environment
export CAPISCIO_REQUIRE_SIGNATURES=true
export CAPISCIO_FAIL_MODE=block
export CAPISCIO_RATE_LIMIT_RPM=100
```

```python
from capiscio_sdk import SecurityConfig

config = SecurityConfig.from_env()
```

---

## Complete Example

```python
from capiscio_sdk import (
    SimpleGuard,
    CapiscioSecurityExecutor,
    SecurityConfig,
    DownstreamConfig,
    UpstreamConfig,
)

# SimpleGuard for signing/verification
guard = SimpleGuard(dev_mode=True)

# Custom security config
config = SecurityConfig(
    downstream=DownstreamConfig(
        validate_schema=True,
        require_signatures=True,
        rate_limit_requests_per_minute=100,
    ),
    upstream=UpstreamConfig(
        validate_agent_cards=True,
        cache_timeout=1800,
    ),
    fail_mode="block",
)

# Wrap your agent
executor = CapiscioSecurityExecutor(
    delegate=my_agent,
    config=config,
)
```

---

## See Also

- [SDK Reference](./sdk-python/index.md) - Auto-generated API docs
- [SimpleGuard Guide](./sdk-python/simple-guard.md) - Detailed SimpleGuard usage
- [Security Quickstart](../quickstarts/secure/1-intro.md) - Getting started
