# Node.js Wrapper (npm)

> **Install CapiscIO CLI via npm**

The `capiscio` npm package provides an npm-installable wrapper for the CapiscIO CLI.

---

## Installation

### Global Installation (Recommended)

```bash
npm install -g capiscio
```

### Local Installation

```bash
npm install capiscio
```

With local installation, run via npx:

```bash
npx capiscio validate agent-card.json
```

---

## How It Works

When you run `npm install capiscio`:

1. **Detects** your OS (Linux, macOS, Windows) and architecture (x64, ARM64)
2. **Downloads** the correct `capiscio-core` binary via postinstall script
3. **Creates** a `capiscio` command that proxies to the binary

---

## Usage

After installation, use `capiscio` directly from your terminal:

```bash
# Validate an agent card
capiscio validate agent-card.json

# Validate with JSON output
capiscio validate agent-card.json --json

# Test live endpoint
capiscio validate https://agent.example.com --test-live

# Strict validation mode
capiscio validate agent-card.json --strict

# Issue a self-signed badge (development)
capiscio badge issue --self-sign --sub did:web:example.com:agents:my-agent

# Verify a badge offline (uses trust store)
capiscio badge verify "eyJhbGciOiJFZERTQSJ9..." --offline
```

All CLI flags are identical to the core binary. See [:octicons-arrow-right-24: CLI Reference](../cli/index.md) for the complete command reference.

### Wrapper-Specific Commands

The Node.js wrapper provides additional maintenance commands:

| Command | Description |
|---------|-------------|
| `capiscio --wrapper-version` | Display the wrapper package version |
| `capiscio --wrapper-clean` | Remove cached binary (forces re-download) |

---

## Package Scripts Integration

Add validation to your `package.json`:

```json
{
  "scripts": {
    "validate": "capiscio validate agent-card.json",
    "validate:strict": "capiscio validate agent-card.json --strict",
    "validate:json": "capiscio validate agent-card.json --json"
  },
  "devDependencies": {
    "capiscio": "^0.3.0"
  }
}
```

Then run:

```bash
npm run validate
```

---

## CI/CD Usage

### GitHub Actions

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'

- name: Install CapiscIO
  run: npm install -g capiscio

- name: Validate Agent
  run: capiscio validate agent-card.json --strict
```

### GitLab CI

```yaml
validate:
  image: node:20
  script:
    - npm install -g capiscio
    - capiscio validate agent-card.json --strict
```

---

## Programmatic Usage

!!! warning "CLI Wrapper Only"
    The npm package is a **CLI wrapper only**. It does not expose a TypeScript/JavaScript API for programmatic validation.

For programmatic validation in Node.js, spawn the CLI as a child process:

```typescript
import { execSync } from 'child_process';

interface ValidationResult {
  success: boolean;
  scoringResult: {
    complianceScore: number;
    trustScore: number;
  };
}

function validateAgentCard(path: string): ValidationResult {
  const result = execSync(`npx capiscio validate ${path} --json`, {
    encoding: 'utf-8',
  });
  return JSON.parse(result);
}

// Usage
const result = validateAgentCard('./agent-card.json');
console.log('Compliance:', result.scoringResult.complianceScore);
```

A full Node.js SDK (`@capiscio/sdk`) is planned for future releases.

---

## Troubleshooting

### Binary Download Fails

If the postinstall script fails:

```bash
# Remove and reinstall
npm uninstall capiscio
npm install capiscio
```

### Permission Errors (Global Install)

If you get EACCES errors:

```bash
# Option 1: Use npx instead
npx capiscio validate agent-card.json

# Option 2: Fix npm permissions
# See: https://docs.npmjs.com/resolving-eacces-permissions-errors
```

### Platform Not Supported

The wrapper supports:
- **Linux**: x64, ARM64
- **macOS**: x64 (Intel), ARM64 (Apple Silicon)
- **Windows**: x64

---

## See Also

- [:octicons-arrow-right-24: CLI Reference](../cli/index.md) — Complete command reference
- [:octicons-arrow-right-24: Python Wrapper](python.md) — pip installation option
- [:octicons-arrow-right-24: GitHub Action](github-action.md) — CI/CD native integration
