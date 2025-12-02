---
title: SimpleGuard
description: Zero-config security for A2A agents
---

# SimpleGuard

Zero-configuration security for signing and verifying A2A requests.

---

## Overview

`SimpleGuard` is the recommended way to add security to your A2A agent. It handles:

- **Signing outbound requests** with JWS (JSON Web Signature)
- **Verifying inbound requests** against a trust store
- **Key management** with file-based storage

---

## Basic Usage

```python
from capiscio_sdk.simple_guard import SimpleGuard

# Initialize - uses convention over configuration
# Looks for capiscio_keys/ and agent-card.json in project root
guard = SimpleGuard(dev_mode=True)  # Auto-generates keys for development

# Sign a request
body = b'{"method": "tasks/send", "params": {}}'
jws = guard.sign_outbound({}, body=body)

# Verify an incoming request
claims = guard.verify_inbound(jws, body=body)
```

## Convention Over Configuration

SimpleGuard automatically finds keys based on directory structure:

```
your-project/
├── agent-card.json           # Agent identity
└── capiscio_keys/
    ├── private.pem           # Signing key
    ├── public.pem            # Public key
    └── trusted/              # Trust store
        └── {kid}.pem         # Trusted keys (filename = key ID)
```

In `dev_mode=True`, all files are auto-generated if missing.

---

## API Reference

::: capiscio_sdk.simple_guard.SimpleGuard
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy
