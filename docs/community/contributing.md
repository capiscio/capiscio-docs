# Contributing to CapiscIO

We welcome contributions from developers of all skill levels. Whether you're fixing a typo, improving documentation, or adding new features, your help makes CapiscIO better for everyone.

---

## Ways to Contribute

| Contribution Type | Description |
|-------------------|-------------|
| **Bug Reports** | Report issues with clear reproduction steps |
| **Feature Requests** | Suggest improvements or new capabilities |
| **Documentation** | Fix typos, clarify explanations, add examples |
| **Code** | Submit bug fixes, features, or optimizations |
| **Tests** | Improve test coverage and add edge cases |

---

## Project Repositories

CapiscIO is organized across multiple repositories:

| Repository | Description |
|------------|-------------|
| [capiscio-sdk-python](https://github.com/capiscio/capiscio-sdk-python) | Python middleware for A2A security |
| [capiscio-node](https://github.com/capiscio/capiscio-node) | Node.js CLI for validation and testing |
| [capiscio-python](https://github.com/capiscio/capiscio-python) | Python wrapper for the CLI |
| [capiscio-docs](https://github.com/capiscio/capiscio-docs) | This unified documentation site |

---

## Reporting Issues

Open an issue in the relevant repository with:

1. **Clear description** of the problem or suggestion
2. **Steps to reproduce** (for bugs)
3. **Expected vs actual behavior**
4. **Version information** (CLI version, Python version, OS)
5. **Logs or screenshots** if applicable

**Issue trackers:**

- [Python SDK Issues](https://github.com/capiscio/capiscio-sdk-python/issues)
- [Node.js CLI Issues](https://github.com/capiscio/capiscio-node/issues)
- [Documentation Issues](https://github.com/capiscio/capiscio-docs/issues)

---

## Contributing Code

Each repository has its own contributing guidelines:

- [Python SDK CONTRIBUTING.md](https://github.com/capiscio/capiscio-sdk-python/blob/main/CONTRIBUTING.md)
- [Node.js CLI CONTRIBUTING.md](https://github.com/capiscio/capiscio-node/blob/main/CONTRIBUTING.md)

### General Workflow

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your changes
4. **Make changes** and commit with clear messages
5. **Test** your changes thoroughly
6. **Push** to your fork
7. **Open a pull request** with a clear description

---

## Contributing Documentation

Documentation improvements are always welcome.

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/capiscio-docs
cd capiscio-docs

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements-docs.txt

# Preview locally
mkdocs serve
```

### Before Submitting

Verify your changes:

- Preview renders correctly at `http://localhost:8000`
- All links work (no broken references)
- Code examples are correct and tested
- Content displays properly in both light and dark themes

### Documentation Structure

```
capiscio-docs/
├── docs/
│   ├── index.md
│   ├── quickstarts/
│   ├── concepts/
│   ├── recipes/
│   ├── reference/
│   └── community/
├── mkdocs.yml
└── requirements-docs.txt
```

---

## Style Guidelines

### Writing

- **Be concise** — developers want quick answers
- **Use examples** — show, don't just tell
- **Link related topics** — help readers navigate
- **Test code samples** — ensure examples work

### Formatting

- Use sentence case for headings
- Include language specifiers in code blocks
- Show expected output for examples
- Use tables for structured information

**Example code block:**

```python
from capiscio_sdk import SimpleGuard

guard = SimpleGuard()
result = guard.verify_request(request)
# Returns: VerificationResult with success=True/False
```

---

## Code of Conduct

All contributors are expected to:

- Be respectful and inclusive
- Provide constructive feedback
- Follow project guidelines
- Help others learn and grow

See our [community standards](https://github.com/capiscio/.github) for details.

---

## Getting Help

- **[Support page](support.md)** — FAQs and troubleshooting
- **[GitHub Discussions](https://github.com/orgs/capiscio/discussions)** — Ask questions and share ideas
- **Issue trackers** — Report bugs in the relevant repository
