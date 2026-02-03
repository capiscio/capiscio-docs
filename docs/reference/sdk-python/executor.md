---
title: CapiscioSecurityExecutor
description: Full-featured security wrapper for A2A agents
---

# CapiscioSecurityExecutor

Full-featured security wrapper that wraps an A2A agent executor with protection.

---

## Overview

`CapiscioSecurityExecutor` provides:

- **Request validation** - Validates incoming requests
- **Signature verification** - Verifies JWS signatures on requests
- **Agent card validation** - Validates caller's agent card
- **Response signing** - Signs all outgoing responses
- **Rate limiting** - Optional rate limiting
- **Audit logging** - Logs all security events

---

## Basic Usage

```python
from capiscio_sdk import CapiscioSecurityExecutor, SecurityConfig

# Wrap your existing executor
secured_executor = CapiscioSecurityExecutor(
    delegate=my_agent_executor,  # Must implement AgentExecutor interface
    config=SecurityConfig.production()
)

# Use it like your original executor
result = await secured_executor.execute(context, event_queue)
```

---

## Wrapper Functions

### secure()

Minimal pattern for wrapping an agent:

```python
from capiscio_sdk import secure, SecurityConfig

secured = secure(my_agent, config=SecurityConfig.production())
```

### secure_agent()

Decorator pattern:

```python
from capiscio_sdk import secure_agent, SecurityConfig

@secure_agent(config=SecurityConfig.production())
class MyAgent:
    def execute(self, context, event_queue):
        pass
```

---

## API Reference

::: capiscio_sdk.executor.CapiscioSecurityExecutor
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true

---

## Functions

::: capiscio_sdk.executor.secure
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3

::: capiscio_sdk.executor.secure_agent
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
