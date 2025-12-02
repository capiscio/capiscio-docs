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

# Configuration
from capiscio_sdk import SecurityConfig, DownstreamConfig, UpstreamConfig

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
```

---

## SimpleGuard

The recommended way to add security to your agent. Zero-config with convention-over-configuration.

::: capiscio_sdk.simple_guard.SimpleGuard
    options:
      show_root_heading: false
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy
      filters:
        - "!^_"  # Exclude private methods

---

## CapiscioSecurityExecutor

Full-featured security wrapper for production agents using the A2A SDK.

::: capiscio_sdk.executor.CapiscioSecurityExecutor
    options:
      show_root_heading: false
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      filters:
        - "!^_"

---

## Helper Functions

### secure()

::: capiscio_sdk.executor.secure
    options:
      show_root_heading: false
      heading_level: 4

### secure_agent()

::: capiscio_sdk.executor.secure_agent
    options:
      show_root_heading: false
      heading_level: 4

---

## Configuration

### SecurityConfig

::: capiscio_sdk.config.SecurityConfig
    options:
      show_root_heading: false
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      members_order: source

### DownstreamConfig

::: capiscio_sdk.config.DownstreamConfig
    options:
      show_root_heading: false
      show_source: false
      heading_level: 3

### UpstreamConfig

::: capiscio_sdk.config.UpstreamConfig
    options:
      show_root_heading: false
      show_source: false
      heading_level: 3

---

## Errors

All errors inherit from `CapiscioSecurityError`.

### ConfigurationError

::: capiscio_sdk.errors.ConfigurationError
    options:
      show_root_heading: false
      heading_level: 4
      show_source: false

### VerificationError

::: capiscio_sdk.errors.VerificationError
    options:
      show_root_heading: false
      heading_level: 4
      show_source: false

### CapiscioValidationError

::: capiscio_sdk.errors.CapiscioValidationError
    options:
      show_root_heading: false
      heading_level: 4
      show_source: false

### CapiscioSignatureError

::: capiscio_sdk.errors.CapiscioSignatureError
    options:
      show_root_heading: false
      heading_level: 4
      show_source: false

### CapiscioRateLimitError

::: capiscio_sdk.errors.CapiscioRateLimitError
    options:
      show_root_heading: false
      heading_level: 4
      show_source: false

---

## Types

### ValidationResult

::: capiscio_sdk.types.ValidationResult
    options:
      show_root_heading: false
      heading_level: 3
      show_source: false

### ValidationIssue

::: capiscio_sdk.types.ValidationIssue
    options:
      show_root_heading: false
      heading_level: 3
      show_source: false

### ValidationSeverity

::: capiscio_sdk.types.ValidationSeverity
    options:
      show_root_heading: false
      heading_level: 3
      show_source: false

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

## Header Convention

| Header | Description |
|--------|-------------|
| `X-Capiscio-JWS` | JWS token from `make_headers()` |
| `Authorization: Bearer <jws>` | Alternative header format |

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `MAX_TOKEN_AGE` | 60 seconds | Token expiration time |
| `CLOCK_SKEW_LEEWAY` | 5 seconds | Allowed clock drift |

---

## See Also

- [Quickstart: Secure Your Agent](../../quickstarts/secure/1-intro.md)
- [SimpleGuard Deep Dive](./simple-guard.md)
- [Configuration Guide](../configuration.md)
