---
title: "Step 2: Installation"
description: Install the CapiscIO CLI
---

# Step 2: Installation

The CapiscIO CLI is available for Node.js and Python. Choose your preferred platform.

---

## Install the CLI

=== "npm (Node.js)"

    ```bash
    npm install -g capiscio
    ```

    Verify the installation:

    ```bash
    capiscio --version
    ```

    Expected output:
    ```
    capiscio/2.1.x (darwin-arm64)
    ```

=== "pip (Python)"

    ```bash
    pip install capiscio
    ```

    Verify the installation:

    ```bash
    capiscio --version
    ```

    Expected output:
    ```
    capiscio/2.1.x (darwin-arm64)
    ```

=== "Go (Direct)"

    If you have Go installed, you can install the core binary directly:

    ```bash
    go install github.com/capiscio/capiscio-core/cmd/capiscio@latest
    ```

    Verify the installation:

    ```bash
    capiscio --version
    ```

!!! info "How It Works"
    The npm and pip packages are thin wrappers around the `capiscio-core` Go binary. On first run, they automatically download the correct binary for your platform. This ensures consistent behavior across all languages.

---

## First Run

The first time you run `capiscio`, it will download the core binary:

```bash
capiscio --help
```

You should see:

```
The core engine for the CapiscIO ecosystem.
Validates Agent Cards, verifies signatures, and scores agent trust and availability.

Usage:
  capiscio [command]

Available Commands:
  badge       Manage Trust Badges
  gateway     Start the CapiscIO Gateway
  help        Help about any command
  key         Manage Cryptographic Keys
  validate    Validate an Agent Card

Flags:
  -h, --help      help for capiscio
  -v, --version   version for capiscio

Use "capiscio [command] --help" for more information about a command.
```

---

## Troubleshooting

??? question "Permission denied on npm install"
    
    If you get a permission error, try:
    
    ```bash
    npm install -g capiscio --unsafe-perm
    ```
    
    Or use a Node version manager like `nvm` to avoid permission issues.

??? question "Binary download fails"
    
    The CLI downloads the binary from GitHub releases. If you're behind a corporate firewall:
    
    1. Download the binary manually from [GitHub Releases](https://github.com/capiscio/capiscio-core/releases)
    2. Place it in `~/.capiscio/bin/`
    3. Make it executable: `chmod +x ~/.capiscio/bin/capiscio`

??? question "Command not found after install"
    
    Ensure your PATH includes the npm/pip global bin directory:
    
    ```bash
    # For npm
    export PATH="$PATH:$(npm config get prefix)/bin"
    
    # For pip
    export PATH="$PATH:$(python -m site --user-base)/bin"
    ```

---

## Create a Sample Agent Card

Before we validate, let's create a sample agent card to work with:

```bash
cat > agent-card.json << 'EOF'
{
  "name": "My First Agent",
  "description": "A sample A2A agent for learning CapiscIO",
  "url": "https://example.com/agent",
  "version": "1.0.0",
  "protocolVersion": "0.2.0",
  "provider": {
    "organization": "My Company"
  },
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "greeting",
      "name": "Greeting", 
      "description": "Returns a friendly greeting"
    }
  ]
}
EOF
```

Verify the file was created:

```bash
cat agent-card.json
```

---

## What's Next?

You now have:

- [x] CapiscIO CLI installed
- [x] A sample agent-card.json file

Let's run your first validation!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](1-intro.md){ .md-button }
[Continue :material-arrow-right:](3-validate.md){ .md-button .md-button--primary }
</div>
