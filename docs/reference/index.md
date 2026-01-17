# API Reference

Complete reference documentation for all CapiscIO products.

## Products

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **CapiscIO Core**

    ---

    CLI and Go library for validation, key management, and badge operations.

    - [CLI Reference](cli/index.md)
    - [Go API](go-api.md)
    - [gRPC Services](grpc.md)

-   :material-language-python:{ .lg .middle } **CapiscIO SDK**

    ---

    Python SDK for runtime security—signing, verification, and trust enforcement.

    - [Overview](sdk-python/index.md)
    - [SimpleGuard](sdk-python/simple-guard.md)
    - [Badge](sdk-python/badge.md)
    - [Types](sdk-python/types.md)

-   :material-shield-check:{ .lg .middle } **MCP Guard**

    ---

    Tool-level authorization for Model Context Protocol servers.

    - [MCP Guard Reference](../mcp-guard/api-reference.md)
    - [Guard Config](sdk-python/mcp.md)

-   :material-server:{ .lg .middle } **Server API**

    ---

    capiscio-server REST API for agent registry and badge CA.

    - [Server Reference](server/index.md)
    - [Badge CA](server/badge-ca.md)
    - [Deployment](server/deployment.md)

</div>

---

## Quick Reference

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    All configuration options for CLI, SDK, and environment variables.

    [:octicons-arrow-right-24: Configuration](configuration.md)

-   :material-code-json:{ .lg .middle } **Agent Card Schema**

    ---

    JSON Schema reference for the A2A Agent Card specification.

    [:octicons-arrow-right-24: Schema Reference](agent-card-schema.md)

-   :material-download:{ .lg .middle } **Installation**

    ---

    Package installation across all platforms and package managers.

    [:octicons-arrow-right-24: Installation Options](wrappers/index.md)

</div>

---

## Package Installation

=== "CapiscIO Core (CLI)"

    ```bash
    npm install -g capiscio    # Node.js wrapper
    # or
    pip install capiscio       # Python wrapper
    ```

=== "CapiscIO SDK"

    ```bash
    pip install capiscio-sdk
    ```

=== "MCP Guard"

    ```bash
    pip install capiscio-mcp          # Standalone
    pip install capiscio-mcp[mcp]     # With MCP SDK integration
    ```

=== "Docker"

    ```bash
    docker pull ghcr.io/capiscio/capiscio-core:latest
    ```

---

## Version Compatibility

| Package | Version | Platform | Requirements |
|---------|---------|----------|--------------|
| `capiscio` (npm) | 2.x | Node.js | ≥18.0 |
| `capiscio` (pip) | 2.x | Python | ≥3.10 |
| `capiscio-sdk` | 0.3.x | Python | ≥3.10 |
| `capiscio-mcp` | 0.1.x | Python | ≥3.10 |
| `capiscio-core` (Go) | 2.x | Go | ≥1.21 |

