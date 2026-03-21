---
title: PIP Types
description: Policy Information Point request/response types for PDP integration
---

# PIP Types

Policy Information Point (PIP) types for building PDP integration requests and interpreting responses. Implements RFC-005: Policy Definition, Distribution and Enforcement.

!!! info "RFC-005 Implementation"
    This API implements the PIP request/response format from RFC-005 §5–§7.

---

## Quick Start

```python
from capiscio_sdk.pip import (
    PIPRequest, PIPResponse,
    SubjectAttributes, ActionAttributes,
    ResourceAttributes, ContextAttributes,
    EnforcementMode, Obligation,
)

# Build a policy decision request
request = PIPRequest(
    subject=SubjectAttributes(
        did="did:web:example.com:agents:bot",
        badge_jti="badge-session-id",
        ial="1",
        trust_level="DV",
    ),
    action=ActionAttributes(operation="POST /api/v1/badges"),
    resource=ResourceAttributes(identifier="/api/v1/badges"),
    context=ContextAttributes(
        txn_id="txn-uuid",
        enforcement_mode=EnforcementMode.GUARD,
    ),
)

# Serialize to dict for your PDP client
payload = request.to_dict()

# Parse PDP response
response = PIPResponse.from_dict({
    "decision": "ALLOW",
    "decision_id": "eval-uuid",
    "obligations": [],
    "ttl": 300,
})

if response.is_allow:
    print("Access granted")
```

---

## EnforcementMode

::: capiscio_sdk.pip.EnforcementMode
    options:
      show_root_heading: true
      members_order: source

---

## Request Types

### PIPRequest

::: capiscio_sdk.pip.PIPRequest
    options:
      show_root_heading: true
      members_order: source

### SubjectAttributes

::: capiscio_sdk.pip.SubjectAttributes
    options:
      show_root_heading: true
      members_order: source

### ActionAttributes

::: capiscio_sdk.pip.ActionAttributes
    options:
      show_root_heading: true
      members_order: source

### ResourceAttributes

::: capiscio_sdk.pip.ResourceAttributes
    options:
      show_root_heading: true
      members_order: source

### ContextAttributes

::: capiscio_sdk.pip.ContextAttributes
    options:
      show_root_heading: true
      members_order: source

### EnvironmentAttributes

::: capiscio_sdk.pip.EnvironmentAttributes
    options:
      show_root_heading: true
      members_order: source

---

## Response Types

### PIPResponse

::: capiscio_sdk.pip.PIPResponse
    options:
      show_root_heading: true
      members_order: source

### Obligation

::: capiscio_sdk.pip.Obligation
    options:
      show_root_heading: true
      members_order: source

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `PIP_VERSION` | `"capiscio.pip.v1"` | Protocol version string |
| `DECISION_ALLOW` | `"ALLOW"` | PDP authorized the request |
| `DECISION_DENY` | `"DENY"` | PDP rejected the request |
| `DECISION_OBSERVE` | `"ALLOW_OBSERVE"` | PEP-only: PDP unavailable in EM-OBSERVE mode |
