---
title: Python SDK Reference
description: Complete API reference for capiscio-sdk (auto-generated from source)
---

# Python SDK Reference

Complete API reference for the `capiscio-sdk` Python package.

!!! info "Auto-Generated Documentation"
    This reference is automatically generated from the SDK source code docstrings.
    It is always accurate and up-to-date with the installed SDK version.

## Installation

```bash
pip install capiscio-sdk
```

**Requirements:** Python ≥3.10

---

## Quick Import Reference

```python
# Core security class
from capiscio_sdk import SimpleGuard

# Executor wrapper and decorators
from capiscio_sdk import CapiscioSecurityExecutor, secure, secure_agent

# Trust Badge API
from capiscio_sdk import (
    verify_badge,
    parse_badge,
    request_badge,
    request_badge_sync,
    BadgeClaims,
    VerifyOptions,
    VerifyResult,
    VerifyMode,
    TrustLevel,
)

# Configuration
from capiscio_sdk import SecurityConfig, DownstreamConfig, UpstreamConfig

# Events & Observability
from capiscio_sdk.events import EventEmitter

# Errors
from capiscio_sdk.errors import (
    ConfigurationError,
    VerificationError,
    CapiscioSecurityError,
    CapiscioValidationError,
    CapiscioSignatureError,
    CapiscioRateLimitError,
)

# Types
from capiscio_sdk import ValidationResult, ValidationIssue, ValidationSeverity

# MCP API (Model Context Protocol security)
from capiscio_sdk._rpc.client import CapiscioRPCClient
# Access MCP via: client.mcp.evaluate_tool_access(...)
```

---

## API Reference

<div class="grid cards" markdown>

-   :material-badge-account: **Badge API**

    ---

    Trust Badge verification and management. Verify agent identity,
    parse badge claims, and request new badges from CAs.

    [:octicons-arrow-right-24: Badge API](badge.md)

-   :material-shield-check: **SimpleGuard**

    ---

    Zero-config security middleware. Convention-over-configuration for signing
    and verifying A2A messages.

    [:octicons-arrow-right-24: SimpleGuard API](simple-guard.md)

-   :material-cog: **SecurityConfig**

    ---

    Configuration classes for downstream protection, upstream validation,
    and security presets.

    [:octicons-arrow-right-24: Configuration API](config.md)

-   :material-run-fast: **CapiscioSecurityExecutor**

    ---

    Full-featured security wrapper for production agents using the A2A SDK.
    Includes `secure()` and `secure_agent()` decorators.

    [:octicons-arrow-right-24: Executor API](executor.md)

-   :material-chart-timeline-variant: **Events**

    ---

    Event emission for agent observability. Includes `EventEmitter`
    for manual and automatic (middleware) event reporting.

    [:octicons-arrow-right-24: Events API](../../how-to/integrations/fastapi.md#observability-auto-events)

-   :material-alert-circle: **Errors**

    ---

    Exception classes for security errors, validation failures,
    signature issues, and rate limiting.

    [:octicons-arrow-right-24: Errors API](errors.md)

-   :material-format-list-bulleted-type: **Types**

    ---

    Data types for validation results, issues, and severity levels.

    [:octicons-arrow-right-24: Types API](types.md)

-   :material-server-security: **MCP API**

    ---

    Model Context Protocol security enforcement. Tool access control
    (RFC-006) and server identity verification (RFC-007).

    [:octicons-arrow-right-24: MCP API](mcp.md)

</div>

---

## File Structure Convention

SimpleGuard uses convention-over-configuration. It expects this directory structure:

```
your-project/
├── agent-card.json          # Your agent's identity card
└── capiscio_keys/
    ├── private.pem          # Ed25519 private key
    ├── public.pem           # Ed25519 public key  
    └── trusted/             # Trust store directory
        ├── {kid1}.pem       # Trusted public key (filename = key ID)
        └── {kid2}.pem       # Another trusted key
```

In `dev_mode=True`, SimpleGuard auto-generates all missing files.

---

## Header Convention (RFC-002 §9.1)

| Header | Description |
|--------|-------------|
| `X-Capiscio-Badge` | Trust Badge token from `make_headers()` |
| `Authorization: Badge <token>` | Alternative header format |

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `MAX_TOKEN_AGE` | 300 seconds | Default badge TTL (5 minutes per RFC-002) |
| `CLOCK_SKEW_LEEWAY` | 60 seconds | Allowed clock drift (RFC-002 §8.1) |
| `REVOCATION_CACHE_MAX_STALENESS` | 300 seconds | Max cache staleness (RFC-002 §7.5) |

---

## See Also

- [Getting Started: Secure Your Agent](../../getting-started/secure/1-intro.md)
- [Configuration Guide](../configuration.md)
