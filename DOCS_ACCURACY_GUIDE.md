# Documentation Accuracy Guide

**Purpose:** Best practices for ensuring CapiscIO documentation remains accurate and in sync with actual implementations.

---

## Core Principles

### 1. Single Source of Truth Hierarchy

When documentation conflicts with implementation, this is the authoritative order:

1. **RFCs** (`capiscio-rfcs/`) — Protocol specifications are canonical
2. **Source Code** — Actual implementation behavior
3. **API Docs** (Swagger/OpenAPI) — Server auto-generated docs
4. **Reference Docs** — `capiscio-docs/docs/reference/`
5. **How-To Guides** — `capiscio-docs/docs/how-to/`

**⚠️ Never modify RFCs to match documentation. Documentation must conform to RFCs.**

---

## Code Example Verification Strategies

### Strategy 1: Executable Tests (Recommended)

Create pytest tests that execute documentation code examples:

```python
# tests/test_docs_examples.py
import pytest

class TestDocCodeExamples:
    """Test code examples from documentation."""
    
    def test_badge_verification_example(self):
        """Verify the badge verification example from docs/reference/sdk-python/badge.md."""
        from capiscio_sdk import verify_badge
        
        # This should at least not throw ImportError
        # Actual verification would need a real token
        assert callable(verify_badge)
    
    def test_simple_guard_example(self):
        """Verify SimpleGuard example from getting-started/secure/3-guard.md."""
        from capiscio_sdk import SimpleGuard
        
        # Test that dev_mode parameter exists
        guard = SimpleGuard(dev_mode=True)
        assert guard is not None
```

**Run weekly:** `pytest tests/test_docs_examples.py -v`

### Strategy 2: CLI Command Verification

Verify CLI examples actually work:

```bash
#!/bin/bash
# scripts/verify_cli_examples.sh

set -e

echo "Testing CLI examples from documentation..."

# Test from docs/reference/cli/index.md
echo "Testing: capiscio badge issue --self-sign"
capiscio badge issue --self-sign > /dev/null

echo "Testing: capiscio validate --help"
capiscio validate --help | grep -q "Validate an Agent Card"

echo "All CLI examples verified!"
```

### Strategy 3: Import Verification

Verify all documented imports are valid:

```python
# scripts/verify_imports.py
"""Verify all imports documented in SDK reference."""

DOCUMENTED_IMPORTS = [
    "from capiscio_sdk import SimpleGuard",
    "from capiscio_sdk import verify_badge, parse_badge, TrustLevel",
    "from capiscio_sdk import SecurityConfig, DownstreamConfig, UpstreamConfig",
    "from capiscio_sdk.errors import VerificationError, ConfigurationError",
]

def test_imports():
    for import_stmt in DOCUMENTED_IMPORTS:
        try:
            exec(import_stmt)
            print(f"✓ {import_stmt}")
        except ImportError as e:
            print(f"✗ {import_stmt}")
            raise AssertionError(f"Import failed: {import_stmt}") from e

if __name__ == "__main__":
    test_imports()
```

---

## Version Synchronization

### Package Versions

Maintain a central version file:

```yaml
# .versions.yaml (in workspace root)
packages:
  capiscio-core: "2.3.1"
  capiscio-sdk-python: "2.3.1"
  capiscio-node: "2.3.1"
  capiscio-python: "2.3.1"
  capiscio-server: "2.3.1"
```

**Before release:**
```bash
# scripts/sync_doc_versions.sh
VERSION=$(cat .versions.yaml | yq '.packages.capiscio-sdk-python')
find capiscio-docs/docs -name "*.md" -exec \
  sed -i "s/capiscio-sdk==.*/capiscio-sdk==$VERSION/g" {} \;
```

### API Endpoint Synchronization

Generate endpoint docs from OpenAPI:

```bash
# Regenerate server API docs from Swagger
cd capiscio-server
swag init -g cmd/server/main.go
cd ../capiscio-docs
python scripts/sync_api_docs.py ../capiscio-server/docs/swagger.json
```

---

## RFC Compliance Checklist

When writing documentation, verify against these RFCs:

### RFC-002 (Trust Badge) Checklist

- [ ] Trust levels are strings ("0" through "4"), not integers
- [ ] Clock skew tolerance is 60 seconds
- [ ] Badge TTL default is 5 minutes (300 seconds)
- [ ] Header name is `X-Capiscio-Badge` (not X-Capiscio-Signature)
- [ ] Required claims: `jti`, `iss`, `sub`, `iat`, `exp`, `ial`, `key`, `vc`
- [ ] IAL-1 badges require `cnf` claim
- [ ] Level 0 badges must have `ial` = "0" and no `cnf` claim

### RFC-003 (PoP Protocol) Checklist

- [ ] API key header is `X-Capiscio-Registry-Key`
- [ ] Grant token flow documented correctly
- [ ] PoP proof signing documented correctly

### RFC-006/007 (MCP) Checklist

- [ ] Tool authority evidence structure matches spec
- [ ] Server identity discovery URLs are correct
- [ ] Badge scope claims are accurate

---

## Documentation PR Checklist

Before merging any documentation PR:

### Content Verification

- [ ] Code examples execute without error
- [ ] All imports are valid
- [ ] API endpoints exist in actual server
- [ ] CLI flags match `--help` output
- [ ] Version numbers match actual releases

### RFC Alignment

- [ ] No claims that contradict RFCs
- [ ] Terminology matches RFC definitions
- [ ] Security properties are accurately described

### Cross-Reference Check

- [ ] All internal links resolve
- [ ] API references point to correct versions
- [ ] Example code uses correct function signatures

---

## Automated Verification CI

Add to `.github/workflows/docs-verify.yml`:

```yaml
name: Verify Documentation

on:
  pull_request:
    paths:
      - 'capiscio-docs/docs/**'

jobs:
  verify-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install SDK
        run: pip install capiscio-sdk
      
      - name: Verify imports
        run: python capiscio-docs/scripts/verify_imports.py
      
      - name: Run doc tests
        run: pytest capiscio-docs/tests/test_docs_examples.py -v
      
      - name: Verify CLI examples
        run: |
          pip install capiscio
          bash capiscio-docs/scripts/verify_cli_examples.sh

  verify-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check links
        uses: lycheeverse/lychee-action@v1
        with:
          args: --verbose capiscio-docs/docs/**/*.md
```

---

## Common Documentation Errors to Avoid

### 1. Fabricated Parameters

**❌ Wrong:**
```python
guard = SimpleGuard(
    private_key_path="keys/private.pem",  # Doesn't exist
    trust_store_path="keys/trusted/",     # Doesn't exist
)
```

**✅ Correct:**
```python
guard = SimpleGuard(dev_mode=True)  # Only actual parameters
```

### 2. Wrong Header Names

**❌ Wrong:** `X-Capiscio-Signature`
**✅ Correct:** `X-Capiscio-Badge` (RFC-002 §9.1)

### 3. Wrong API Paths

**❌ Wrong:** `/v1/badges/verify`, `/v1/keys`
**✅ Correct:** `/v1/validate`, `/v1/api-keys`

### 4. Wrong Trust Levels

**❌ Wrong:** Levels 1-3 only
**✅ Correct:** Levels 0-4 (0=SS, 1=REG, 2=DV, 3=OV, 4=EV)

### 5. Wrong Clock Tolerance

**❌ Wrong:** 5 seconds
**✅ Correct:** 60 seconds (RFC-002 §8.1)

### 6. Missing IAL Documentation

**❌ Wrong:** Trust levels only
**✅ Correct:** Trust levels AND Identity Assurance Levels (IAL-0, IAL-1)

---

## Quick Reference: Accurate Values

| Concept | Correct Value | Source |
|---------|---------------|--------|
| Clock skew tolerance | 60 seconds | RFC-002 §8.1 |
| Badge TTL default | 5 minutes (300s) | RFC-002 §4.3 |
| Trust levels | "0", "1", "2", "3", "4" | RFC-002 §5 |
| IAL values | "0", "1" | RFC-002 §7.2.1 |
| Badge header | `X-Capiscio-Badge` | RFC-002 §9.1 |
| API key header | `X-Capiscio-Registry-Key` | RFC-003 §3.1 |
| Badge validation endpoint | `/v1/validate` | Server router |
| API keys endpoint | `/v1/api-keys` | Server router |
| SDK version | 2.3.1 | pyproject.toml |
| CLI version | 2.3.1 | capiscio-core |

---

## Monthly Documentation Audit

Schedule monthly audits:

1. **Week 1:** Run all automated verification scripts
2. **Week 2:** Manual review of getting-started guides
3. **Week 3:** Manual review of reference documentation
4. **Week 4:** Cross-reference against latest RFC changes

Track findings in `DOCS_VERIFICATION_TRACKER.md`.
