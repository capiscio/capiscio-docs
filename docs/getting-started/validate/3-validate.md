---
title: "Step 3: Your First Validation"
description: Run your first agent card validation
---

# Step 3: Your First Validation

Now let's validate an agent card and see the results.

---

## Download a Sample Agent Card

First, grab our sample agent card:

<div class="grid" markdown>

```json title="agent-card.json" linenums="1"
{
  "name": "My First Agent",
  "description": "A helpful AI assistant",
  "url": "https://my-agent.example.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "general-assistant",
      "name": "General Assistant",
      "description": "Answers questions and helps with tasks",
      "tags": ["general", "assistant"]
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"]
}
```

[:material-download: Download agent-card.json](../../assets/samples/agent-card.json){ .md-button .md-button--primary }

</div>

---

## Run Your First Validation

=== "Command"

    ```bash
    capiscio validate agent-card.json
    ```

=== "Response"

    ```ansi
    [32m✅ A2A AGENT VALIDATION PASSED[0m

    [1mScore: 85/100[0m
    Version: 1.0.0
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    [33m⚠[0m  WARNINGS (2)
    
    [33m⚠[0m  [MISSING_PROVIDER] Missing recommended 'provider' field
       → Add provider info for better discoverability
    
    [33m⚠[0m  [NO_AUTH] No authentication configured
       → Consider adding authentication for production
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    [32m✓[0m Schema valid
    [32m✓[0m Required fields present
    [32m✓[0m Skills properly defined
    [33m○[0m Endpoint not tested (use --test-live)
    ```

!!! success "It worked!"
    Your agent card is valid! The warnings are just suggestions for improvement.

---

## Try Different Outputs

### JSON Output (for CI/CD)

=== "Command"

    ```bash
    capiscio validate agent-card.json --json
    ```

=== "Response"

    ```json
    {
      "valid": true,
      "score": 85,
      "version": "1.0.0",
      "status": "PASSED",
      "checks": [
        {
          "name": "schema",
          "passed": true,
          "message": "Schema validation passed"
        },
        {
          "name": "required_fields",
          "passed": true,
          "message": "All required fields present"
        },
        {
          "name": "skills",
          "passed": true,
          "message": "Skills properly defined"
        }
      ],
      "warnings": [
        {
          "code": "MISSING_PROVIDER",
          "message": "Missing recommended 'provider' field"
        },
        {
          "code": "NO_AUTH",
          "message": "No authentication configured"
        }
      ],
      "errors": []
    }
    ```

### Strict Mode (for Production)

=== "Command"

    ```bash
    capiscio validate agent-card.json --strict
    ```

=== "Response"

    ```ansi
    [31m❌ A2A AGENT VALIDATION FAILED[0m

    [1mScore: 85/100[0m (minimum required: 90)
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    [31m✗[0m  ERRORS (2) - Warnings promoted to errors in strict mode
    
    [31m✗[0m  [MISSING_PROVIDER] Missing 'provider' field
    [31m✗[0m  [NO_AUTH] No authentication configured
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Tip: Fix errors above or use default mode for development
    ```

---

## Validate an Invalid Card

Let's see what happens with an invalid agent card:

=== "Command"

    ```bash
    # Create an invalid card
    echo '{"name": "", "url": "not-a-url"}' > invalid.json
    
    capiscio validate invalid.json
    ```

=== "Response"

    ```ansi
    [31m❌ A2A AGENT VALIDATION FAILED[0m

    [1mScore: 15/100[0m
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    [31m✗[0m  ERRORS (5)
    
    [31m✗[0m  [EMPTY_NAME] 'name' field cannot be empty
       → Provide a descriptive name for your agent
    
    [31m✗[0m  [INVALID_URL] 'url' must be a valid HTTPS URL
       → Use format: https://your-agent.example.com
    
    [31m✗[0m  [MISSING_REQUIRED] Missing required field 'description'
    
    [31m✗[0m  [MISSING_REQUIRED] Missing required field 'capabilities'
    
    [31m✗[0m  [MISSING_REQUIRED] Missing required field 'skills'
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```

---

## Validation Modes Comparison

| Mode | Command | Best For | Warnings |
|------|---------|----------|----------|
| **Default** | `capiscio validate agent-card.json` | Development | Show but pass |
| **Strict** | `capiscio validate agent-card.json --strict` | Production | Fail on warnings |
| **Schema Only** | `capiscio validate agent-card.json --schema-only` | Quick checks | Schema only |

---

## Common Flags Reference

```bash
# Output formats
capiscio validate agent-card.json --json          # JSON output
capiscio validate agent-card.json --errors-only   # Quiet mode

# Validation modes  
capiscio validate agent-card.json --strict        # Production mode
capiscio validate agent-card.json --schema-only   # Fast schema check

# Live testing
capiscio validate https://agent.com/.well-known/agent-card.json --test-live

# Timeouts
capiscio validate agent-card.json --timeout 30s   # 30 second timeout
```

---

## What's Next?

You've learned how to:

- [x] Download and validate an agent card
- [x] Interpret validation output
- [x] Use JSON output for automation
- [x] Understand strict vs default mode

Next, let's understand the detailed validation report!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](2-install.md){ .md-button }
[Continue :material-arrow-right:](4-reports.md){ .md-button .md-button--primary }
</div>
