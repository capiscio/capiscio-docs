# API Reference

Complete reference documentation for all CapiscIO APIs, CLIs, and configuration options.

## Quick Links

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **CLI Reference**

    ---

    Command-line interface for validation, key management, badges, and gateway.

    [:octicons-arrow-right-24: CLI Commands](cli/index.md)

-   :material-language-python:{ .lg .middle } **Python SDK**

    ---

    Security middleware for Python applications with SimpleGuard and Executor.

    [:octicons-arrow-right-24: SDK Reference](sdk-python/index.md)

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    All configuration options for CLI, SDK, and environment variables.

    [:octicons-arrow-right-24: Configuration](configuration.md)

-   :material-code-json:{ .lg .middle } **Agent Card Schema**

    ---

    JSON Schema reference for the A2A Agent Card specification.

    [:octicons-arrow-right-24: Schema Reference](agent-card-schema.md)

</div>

---

## Package Installation

=== "npm"

    ```bash
    npm install capiscio
    ```

=== "pip"

    ```bash
    pip install capiscio
    ```

=== "pip (SDK)"

    ```bash
    pip install capiscio-sdk
    ```

=== "Docker"

    ```bash
    docker pull ghcr.io/capiscio/capiscio-core:latest
    ```

---

## Version Compatibility

| Package | Version | Node.js | Python | Go |
|---------|---------|---------|--------|----|
| `capiscio` (npm) | 1.0.x | ≥18.0 | - | - |
| `capiscio` (pip) | 1.0.x | - | ≥3.10 | - |
| `capiscio-sdk` | 0.3.x | - | ≥3.10 | - |
| `capiscio-core` | 1.0.x | - | - | ≥1.21 |

