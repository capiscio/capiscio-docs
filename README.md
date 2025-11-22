# CapiscIO Documentation Hub

This repository contains the landing page for CapiscIO documentation at [docs.capisc.io](https://docs.capisc.io).

## Overview

The landing page serves as a navigation hub for all CapiscIO product documentation:

- **Python SDK** (`/capiscio-sdk-python`) - Runtime security middleware
- **CLI Tool** (`/cli`) - Command-line utilities (coming soon)

## Local Development

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# Install dependencies
pip install mkdocs-material

# Serve locally
mkdocs serve

# Build
mkdocs build
```

The site will be available at `http://localhost:8000`.

## Deployment

Documentation is automatically deployed to Cloudflare Pages when changes are pushed to the `main` branch.

**Deployment Target**: Root of `docs.capisc.io`

## Structure

```
capiscio-docs/
├── docs/
│   ├── index.md              # Landing page
│   └── stylesheets/
│       └── landing.css       # Custom styles for product cards
├── mkdocs.yml                # MkDocs configuration
├── .github/workflows/
│   └── deploy.yml            # GitHub Actions deployment
└── README.md
```

## Adding New Products

To add a new product to the landing page:

1. Edit `docs/index.md`
2. Add a new product card in the "Products" section
3. Link to the product's documentation subdirectory (e.g., `/new-product`)
4. Deploy the product's documentation to its subdirectory in Cloudflare Pages

## Theme

The landing page uses Material for MkDocs with the same color scheme as the product documentation:

- **Primary**: Blue Grey
- **Accent**: Cyan
- **Font**: Roboto / Roboto Mono

## Contributing

For changes to the landing page, please open a PR against this repository.

For product-specific documentation changes, please contribute to the respective product repository.

## License

MIT License - see individual product repositories for their licenses.
