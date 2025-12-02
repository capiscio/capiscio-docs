# Python Wrapper (pip)

> **Install CapiscIO CLI via pip**

The `capiscio` Python package provides a pip-installable wrapper for the CapiscIO CLI.

---

## Installation

```bash
pip install capiscio
```

Or with a specific version:

```bash
pip install capiscio==0.3.0
```

---

## How It Works

When you run `pip install capiscio`:

1. **Detects** your OS (Linux, macOS, Windows) and architecture (x64, ARM64)
2. **Downloads** the correct `capiscio-core` binary from GitHub releases
3. **Installs** the binary to your Python environment's bin directory
4. **Creates** a `capiscio` command that proxies to the binary

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
```

All CLI flags are identical to the core binary. See [:octicons-arrow-right-24: CLI Reference](../cli/index.md) for the complete command reference.

---

## Wrapper-Specific Options

The Python wrapper adds two utility flags:

| Flag | Description |
|------|-------------|
| `--wrapper-version` | Show the pip package version (not the core binary version) |
| `--wrapper-clean` | Remove downloaded binary and re-download on next run |

```bash
# Check wrapper package version
capiscio --wrapper-version

# Force re-download of binary
capiscio --wrapper-clean
```

---

## Virtual Environments

The wrapper works correctly in virtual environments:

```bash
# Create and activate venv
python -m venv .venv
source .venv/bin/activate

# Install in venv
pip install capiscio

# Binary is installed to .venv/bin/capiscio
which capiscio
# → /path/to/project/.venv/bin/capiscio
```

---

## CI/CD Usage

### GitHub Actions

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'

- name: Install CapiscIO
  run: pip install capiscio

- name: Validate Agent
  run: capiscio validate agent-card.json --strict
```

### GitLab CI

```yaml
validate:
  image: python:3.11
  script:
    - pip install capiscio
    - capiscio validate agent-card.json --strict
```

---

## Troubleshooting

### Binary Download Fails

If the binary download fails, check your network connection and try:

```bash
# Clean and reinstall
pip uninstall capiscio
pip install capiscio
```

### Permission Errors

On Unix systems, ensure the binary is executable:

```bash
chmod +x $(python -c "import capiscio; print(capiscio.BINARY_PATH)")
```

### Platform Not Supported

The wrapper supports:
- **Linux**: x64, ARM64
- **macOS**: x64 (Intel), ARM64 (Apple Silicon)
- **Windows**: x64

If your platform isn't supported, [build from source](https://github.com/capiscio/capiscio-core).

---

## See Also

- [:octicons-arrow-right-24: CLI Reference](../cli/index.md) — Complete command reference
- [:octicons-arrow-right-24: Node.js Wrapper](node.md) — npm installation option
- [:octicons-arrow-right-24: GitHub Action](github-action.md) — CI/CD native integration
