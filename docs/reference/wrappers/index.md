# Language Wrappers

> **Install the CapiscIO CLI via your preferred package manager**

CapiscIO provides language-specific wrapper packages that automatically download and manage the `capiscio-core` binary for your platform.

---

## Available Wrappers

<div class="grid cards" markdown>

-   :simple-python: **Python (pip)**

    ---

    Install via pip for Python projects.

    ```bash
    pip install capiscio
    ```

    [:octicons-arrow-right-24: Python Wrapper](python.md)

-   :simple-nodedotjs: **Node.js (npm)**

    ---

    Install via npm for JavaScript/TypeScript projects.

    ```bash
    npm install -g capiscio
    ```

    [:octicons-arrow-right-24: Node.js Wrapper](node.md)

</div>

---

## What Are Wrappers?

These packages are **thin wrappers** around the core `capiscio-core` Go binary. They:

1. **Download** the correct binary for your OS and architecture
2. **Manage** binary installation in a language-appropriate location
3. **Proxy** all CLI commands to the underlying binary

All wrappers expose the **same CLI** with identical flags and behavior.

---

## Choosing a Wrapper

| Use Case | Recommended |
|----------|-------------|
| Python project with existing pip dependencies | **pip** (`capiscio`) |
| Node.js project with existing npm dependencies | **npm** (`capiscio`) |
| CI/CD pipeline (GitHub Actions) | **GitHub Action** (`validate-a2a`) |
| Direct binary installation | **Homebrew/Manual** (see [CLI Reference](../cli/index.md)) |

---

## Common Commands

Once installed via any wrapper, the CLI is identical:

```bash
# Validate an agent card
capiscio validate agent-card.json

# Validate with JSON output
capiscio validate agent-card.json --json

# Test live endpoint
capiscio validate https://agent.example.com --test-live

# Strict mode
capiscio validate agent-card.json --strict
```

For the complete CLI reference, see [:octicons-arrow-right-24: CLI Reference](../cli/index.md).
