# Getting Help

Need help with CapiscIO? Here are the best ways to get support.

## Documentation

Start with the documentation for your specific product:

- **[A2A Security Documentation](../a2a-security/index.md)** - Security middleware guides and API reference
- **[CapiscIO CLI Documentation](../capiscio-cli/README.md)** - Command-line tools and validation

## Quick Links

### Getting Started

- [A2A Security Quick Start](../a2a-security/getting-started/quickstart.md)
- [CapiscIO CLI Getting Started](../capiscio-cli/README.md)
- [A2A Protocol Specification](https://github.com/a2aproject/A2A){:target="_blank"}

### Common Tasks

**For A2A Security:**

- [Installation & Setup](../a2a-security/getting-started/installation.md)
- [Configuration Guide](../a2a-security/guides/configuration.md)
- [Core Concepts](../a2a-security/getting-started/concepts.md)

**For CapiscIO CLI:**

- [Validation Process](../capiscio-cli/validation-process.md)
- [Scoring System](../capiscio-cli/scoring-system.md)
- [Architecture](../capiscio-cli/architecture.md)

## GitHub Resources

### Issues & Bug Reports

Report bugs or request features in the relevant repository:

- [A2A Security Issues](https://github.com/capiscio/a2a-security/issues){:target="_blank"}
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

### Python (A2A Security)

- **PyPI**: [a2a-security package](https://pypi.org/project/a2a-security.md)
- **Installation**: `pip install a2a-security`
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
- [Code of Conduct](https://github.com/capiscio/a2a-security/blob/main/CODE_OF_CONDUCT.md)
- [Security Policy](https://github.com/capiscio/a2a-security/blob/main/SECURITY.md)

### Stay Updated

- **GitHub**: Watch the repositories for updates
  - [capiscio/a2a-security](https://github.com/capiscio/a2a-security)
  - [capiscio/capiscio-cli](https://github.com/capiscio/capiscio-cli)
- **Releases**: Check [Releases](https://github.com/capiscio/a2a-security/releases) for changelogs

## Security Issues

Found a security vulnerability? Please report it responsibly:

- **Do not** open a public issue
- See [Security Policy](https://github.com/capiscio/a2a-security/blob/main/SECURITY.md) for reporting process
- Security issues are handled with priority

## Frequently Asked Questions

!!! question "Common Questions"
    Can't find what you're looking for? Check these frequently asked questions or open an issue on GitHub.

### Installation Issues

**Q: `pip install capiscio-a2a-security` fails**

A: Ensure you have Python 3.10 or higher:
```bash
python --version
pip install --upgrade pip
pip install a2a-security
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
from a2a_security import validate_message

result = validate_message(message_data)
```

**Q: Where can I find example agent cards?**

A: Check the [CLI repository examples](https://github.com/capiscio/capiscio-cli/tree/main/examples)

### Development Questions

**Q: How do I run tests locally?**

A: Each repository has its own test suite:

**A2A Security**:
```bash
cd a2a-security
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

1. Search existing [GitHub Issues](https://github.com/capiscio/a2a-security/issues)
2. Check the [A2A Specification](https://github.com/a2aproject/A2A)
3. Open a new issue with details about your problem

We're here to help! 🤝
