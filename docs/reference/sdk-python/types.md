---
title: Types
description: Data structures and type definitions
---

# Types

Data structures used throughout the CapiscIO SDK.

---

## Validation Types

### ValidationResult

```python
from capiscio_sdk import ValidationResult

result: ValidationResult = await executor.validate_agent_card(url)

print(result.valid)       # bool
print(result.score)       # int (0-100)
print(result.issues)      # List[ValidationIssue]
```

### ValidationIssue

```python
from capiscio_sdk import ValidationIssue, ValidationSeverity

for issue in result.issues:
    print(issue.message)    # str
    print(issue.severity)   # ValidationSeverity
    print(issue.path)       # Optional[str] - JSON path to issue
```

### ValidationSeverity

```python
from capiscio_sdk import ValidationSeverity

# Enumeration values
ValidationSeverity.ERROR    # Blocks validation
ValidationSeverity.WARNING  # Advisory, doesn't block
ValidationSeverity.INFO     # Informational only
```

---

## API Reference

::: capiscio_sdk.types.ValidationResult
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      members_order: source

::: capiscio_sdk.types.ValidationIssue
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      members_order: source

::: capiscio_sdk.types.ValidationSeverity
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
