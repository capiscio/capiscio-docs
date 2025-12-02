# Getting Help

Need help with CapiscIO? Here are the best ways to get support.

## Documentation

Start with the documentation for your specific product:

- **[Python SDK Documentation](../reference/sdk-python/index.md)** - Security middleware guides and API reference
- **[CLI Documentation](../reference/cli/index.md)** - Command-line tools and validation

## Quick Links

### Getting Started

- [Python SDK Quick Start](../quickstarts/secure/1-intro.md)
- [CLI Getting Started](../reference/cli/index.md)
- [A2A Protocol Specification](https://github.com/a2aproject/A2A){:target="_blank"}

### Common Tasks

**For Python SDK:**

- [Installation & Setup](../quickstarts/secure/2-sdk.md)
- [Configuration Guide](../reference/configuration.md)
- [Core Concepts](../concepts/validation.md)

**For Node.js CLI:**

- [Validation Process](../concepts/validation.md)
- [Scoring System](../concepts/scoring.md)
- [CLI Reference](../reference/cli/index.md)

## GitHub Resources

### Issues & Bug Reports

Report bugs or request features in the relevant repository:

- [Python SDK Issues](https://github.com/capiscio/capiscio-sdk-python/issues){:target="_blank"}
- [CapiscIO CLI Issues](https://github.com/capiscio/capiscio-cli/issues){:target="_blank"}
- [Documentation Issues](https://github.com/capiscio/capiscio-docs/issues){:target="_blank"}

When reporting issues, please include:

- Product version
- Operating system
- Clear steps to reproduce
- Expected vs actual behavior
- Relevant error messages or logs

### Pull Requests

Want to contribute? See our [Contributing Guide](contributing.md) for details on:

- Setting up your development environment
- Making changes locally
- Testing your contributions
- Submitting pull requests

## Package Resources

### Python (SDK)

- **PyPI**: [capiscio-sdk-python package](https://pypi.org/project/capiscio-sdk-python/)
- **Installation**: `pip install capiscio-sdk-python`
- **Requirements**: Python 3.10+

### Node.js (CapiscIO CLI)

- **npm**: [capiscio-cli package](https://www.npmjs.com/package/capiscio-cli){:target="_blank"}
- **Installation**: `npm install -g capiscio-cli`
- **Requirements**: Node.js 18+

## A2A Protocol

CapiscIO implements the Agent-to-Agent (A2A) Protocol. Learn more:

- [A2A Specification](https://github.com/a2aproject/A2A){:target="_blank"} - Official protocol specification
- [A2A Inspector](https://github.com/a2aproject/a2a-inspector){:target="_blank"} - Interactive protocol explorer
- [Online Validator](https://capisc.io/validator){:target="_blank"} - Web-based agent card validator

## Community

### Contributing

We welcome contributions! Check out:

- [Contributing Guidelines](contributing.md)
- [Code of Conduct](https://github.com/capiscio/capiscio-sdk-python/blob/main/CODE_OF_CONDUCT.md)
- [Security Policy](https://github.com/capiscio/capiscio-sdk-python/blob/main/SECURITY.md)

### Stay Updated

- **GitHub**: Watch the repositories for updates
  - [capiscio/capiscio-sdk-python](https://github.com/capiscio/capiscio-sdk-python)
  - [capiscio/capiscio-node](https://github.com/capiscio/capiscio-node)
- **Releases**: Check [Releases](https://github.com/capiscio/capiscio-sdk-python/releases) for changelogs

## Security Issues

Found a security vulnerability? Please report it responsibly:

- **Do not** open a public issue
- See [Security Policy](https://github.com/capiscio/capiscio-sdk-python/blob/main/SECURITY.md) for reporting process
- Security issues are handled with priority

## Frequently Asked Questions

!!! question "Common Questions"
    Can't find what you're looking for? Check these frequently asked questions or open an issue on GitHub.

### Installation Issues

**Q: `pip install capiscio-sdk-python` fails**

A: Ensure you have Python 3.10 or higher:
```bash
python --version
pip install --upgrade pip
pip install capiscio-sdk-python
```

**Q: CLI command not found after installation**

A: Make sure npm global bin directory is in your PATH:
```bash
npm config get prefix
# Add <prefix>/bin to your PATH
```

### Usage Questions

**Q: How do I validate agent cards?**

A: Use capiscio-cli:
```bash
capiscio validate path/to/agent-card.json
```

Or programmatically with Python:
```python
from capiscio_sdk import validate_message

result = validate_message(message_data)
```

**Q: Where can I find example agent cards?**

A: Check the [CLI repository examples](https://github.com/capiscio/capiscio-cli/tree/main/examples)

### Development Questions

**Q: How do I run tests locally?**

A: Each repository has its own test suite:

**Python SDK**:
```bash
cd capiscio-sdk-python
pip install -e ".[dev]"
pytest
```

**CLI**:
```bash
cd capiscio-cli
npm install
npm test
```

**Q: How do I preview documentation changes?**

A: Use MkDocs serve:
```bash
pip install -r requirements-docs.txt
mkdocs serve
# Visit http://localhost:8000
```

## Still Need Help?

If you can't find what you're looking for:

1. Search existing [GitHub Issues](https://github.com/capiscio/capiscio-sdk-python/issues)
2. [Ask in Discussions](https://github.com/orgs/capiscio/discussions) - Community Q&A
3. Check the [A2A Specification](https://github.com/a2aproject/A2A)
4. Open a new issue with details about your problem

We're here to help! 🤝
