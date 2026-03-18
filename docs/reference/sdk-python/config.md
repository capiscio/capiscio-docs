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
from capiscio_sdk.config import DownstreamConfig, UpstreamConfig

config = SecurityConfig(
    downstream=DownstreamConfig(require_signatures=True),
    upstream=UpstreamConfig(validate_agent_cards=True),
    strict_mode=True,
    fail_mode="block",
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
