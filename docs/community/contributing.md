# Contributing to CapiscIO

> **Help us build better A2A tooling** - Contributions welcome from developers of all skill levels

Thank you for your interest in contributing to CapiscIO! We welcome contributions from the community.

!!! success "Ways to Contribute"
    - 🐛 Report bugs and issues
    - 💡 Suggest new features
    - 📝 Improve documentation
    - 🔧 Submit code improvements
    - 🧪 Add tests and examples
    - 🌍 Help with translations

## 📦 Project Structure

CapiscIO is organized as a monorepo documentation site with multiple products:

- **[A2A Security](https://github.com/capiscio/a2a-security)** - Python middleware for Agent-to-Agent Protocol security
- **[CapiscIO CLI](https://github.com/capiscio/capiscio-cli)** - Command-line tools for A2A validation and testing
- **[Documentation](https://github.com/capiscio/capiscio-docs)** - This unified documentation site

## 🚀 How to Contribute

### 🐛 Reporting Issues

Found a bug or have a feature request? Please open an issue in the relevant repository:

- **[A2A Security Issues](https://github.com/capiscio/a2a-security/issues){:target="_blank"}
- [CapiscIO CLI Issues](https://github.com/capiscio/capiscio-cli/issues){:target="_blank"}
- [Documentation Issues](https://github.com/capiscio/capiscio-docs/issues){:target="_blank"}

!!! tip "Good Bug Reports Include"
    - Clear description of the issue
    - Steps to reproduce
    - Expected vs actual behavior
    - Version information
    - Relevant logs or screenshots

### 💻 Contributing Code

Each product has its own contributing guidelines:

- [A2A Security Contributing Guide](https://github.com/capiscio/a2a-security/blob/main/CONTRIBUTING.md)
- [CLI Contributing Guide](https://github.com/capiscio/capiscio-cli/blob/main/CONTRIBUTING.md)

### 📝 Contributing to Documentation

Documentation contributions are always welcome! Here's how:

!!! info "Documentation Structure"
    Each product maintains its own docs that are aggregated into the unified site. You can edit docs in the product repo and they'll automatically appear in docs.capisc.io.

**1. Fork the relevant repository**
   - For product docs: Fork the product repo (e.g., `a2a-security`)
   - For landing pages: Fork `capiscio-docs`

2. **Make your changes locally**
   ```bash
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/REPO_NAME
   cd REPO_NAME
   
   # Install dependencies
   pip install -r requirements-docs.txt  # or requirements.txt
   
   # Preview your changes
   mkdocs serve
   ```

**3. Test your changes**

!!! warning "Before Submitting"
    Make sure your changes work correctly:
    
    - ✅ Preview locally at http://localhost:8000
    - ✅ Ensure all links work
    - ✅ Check formatting and code examples
    - ✅ Verify diagrams render correctly
    - ✅ Test on both light and dark themes

**4. Submit a pull request**
   - Push to your fork
   - Open a PR against the main repository
   - Describe your changes clearly

## Documentation Structure

### Product Documentation

Each product maintains its own documentation:

```
product-repo/
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   └── ...
├── mkdocs.yml
└── requirements-docs.txt
```

### Unified Build

The unified documentation site aggregates all product docs:

- **Root site**: `capiscio-docs` repository
- **Aggregation**: Uses `mkdocs-monorepo-plugin`
- **Theme**: Standardized Material theme across all products
- **Navigation**: Tabs for each product section

### Local Development

**Test a single product**:
```bash
cd a2a-security  # or capiscio-cli
mkdocs serve
```

**Test unified site** (requires all repos checked out):
```bash
# Directory structure needed:
# parent/
#   ├── capiscio-docs/
#   ├── a2a-security/
#   └── capiscio-cli/

cd capiscio-docs
mkdocs build -f mkdocs-unified.yml
mkdocs serve -f mkdocs-unified.yml
```

## 📐 Style Guidelines

### ✍️ Writing Style

Our documentation uses a confident, helpful voice:

!!! example "Writing Principles"
    - **Be concise**: Developers want quick answers
    - **Use examples**: Show, don't just tell  
    - **Link liberally**: Cross-reference related topics
    - **Test code**: Ensure all code examples work
    - **Problem/Solution**: Frame features as solutions to real problems

### 🎨 🎨 Formatting

- Use sentence case for headings
- Use code blocks with language specifiers
- Add expected output for examples
- Use admonitions for tips, warnings, notes
- Include emojis in key headings for visual hierarchy

**Example:**

```python
from capiscio_a2a_security import secure

# Wrap your agent with security
secured_agent = secure(MyAgentExecutor())

# Output: Agent wrapped with production security settings
```

!!! tip "Pro Tip"
    Always show expected output for code examples. It helps developers verify their implementation.

### 📚 Markdown Extensions

We use Material for MkDocs with these extensions:

- Code blocks with syntax highlighting
- Admonitions (notes, warnings, tips)
- Tables with formatting
- Task lists
- Footnotes
- Math notation (KaTeX)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- [A2A Security Code of Conduct](https://github.com/capiscio/a2a-security/blob/main/CODE_OF_CONDUCT.md)
- [CLI Code of Conduct](https://github.com/capiscio/capiscio-cli/blob/main/CODE_OF_CONDUCT.md)

## Questions?

- Check the [Support](support.md) page for help resources
- Open an issue in the relevant repository
- Join the community discussions on GitHub

---

## See Also

- **[Getting Help](support.md)** - Support resources and FAQs
- **[A2A Security Contributing](https://github.com/capiscio/a2a-security/blob/main/CONTRIBUTING.md){:target="_blank"}** - Product-specific guidelines
- **[CapiscIO CLI Contributing](https://github.com/capiscio/capiscio-cli/blob/main/CONTRIBUTING.md){:target="_blank"}** - CLI contribution guide

Thank you for helping make CapiscIO better! 🚀
