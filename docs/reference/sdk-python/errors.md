---
title: Errors
description: Exception classes for error handling
---

# Errors

Exception classes raised by the CapiscIO SDK.

---

## Exception Hierarchy

```
CapiscioSecurityError (base)
├── CapiscioValidationError
├── CapiscioSignatureError
├── CapiscioRateLimitError
└── CapiscioUpstreamError
```

---

## Handling Errors

```python
from capiscio_sdk import (
    CapiscioSecurityError,
    CapiscioValidationError,
    CapiscioSignatureError,
)

try:
    claims = guard.verify_inbound(jws_token, body)
except CapiscioSignatureError as e:
    # Invalid or missing signature
    return {"error": "Authentication failed"}, 401
except CapiscioValidationError as e:
    # Request validation failed
    return {"error": f"Invalid request: {e}"}, 400
except CapiscioSecurityError as e:
    # Other security error
    return {"error": "Security error"}, 500
```

---

## API Reference

::: capiscio_sdk.errors.CapiscioSecurityError
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

::: capiscio_sdk.errors.CapiscioValidationError
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

::: capiscio_sdk.errors.CapiscioSignatureError
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

::: capiscio_sdk.errors.CapiscioRateLimitError
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

::: capiscio_sdk.errors.CapiscioUpstreamError
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
