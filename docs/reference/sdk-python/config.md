---
title: Configuration
description: Security configuration options
---

# Configuration

Configure security behavior with presets or custom settings.

---

## Quick Start

```python
from capiscio_sdk import SecurityConfig

# Production defaults (recommended)
config = SecurityConfig.production()

# Strict mode (fail on any issue)
config = SecurityConfig.strict()

# Custom configuration
config = SecurityConfig(
    validate_inbound=True,
    validate_outbound=True,
    require_signature=True,
    log_level="INFO"
)
```

---

## Presets

### Production

```python
config = SecurityConfig.production()
```

Recommended for production deployments:
- Signature verification enabled
- Validation enabled
- Reasonable timeouts
- Standard logging

### Strict

```python
config = SecurityConfig.strict()
```

Maximum security:
- All validations enabled
- Fail on any warning
- Verbose logging
- No fallbacks

### From Environment Variables

```python
config = SecurityConfig.from_env()
```

Reads configuration from environment variables:

| Variable | Description | Default |
|----------|-------------|--------|
| `CAPISCIO_REQUIRE_SIGNATURES` | Require badge on requests | `true` |
| `CAPISCIO_FAIL_MODE` | `block`, `monitor`, or `log` | `block` |
| `CAPISCIO_MIN_TRUST_LEVEL` | Minimum trust level (0-4) | `0` |
| `CAPISCIO_RATE_LIMIT_RPM` | Rate limit (requests/min) | `1000` |

**Example `.env` file:**

```bash
CAPISCIO_REQUIRE_SIGNATURES=true
CAPISCIO_FAIL_MODE=block
CAPISCIO_MIN_TRUST_LEVEL=0
```

---

## API Reference

::: capiscio_sdk.config.SecurityConfig
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true

---

## Related Configuration

::: capiscio_sdk.config.DownstreamConfig
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

::: capiscio_sdk.config.UpstreamConfig
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
