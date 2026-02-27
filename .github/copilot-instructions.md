# capiscio-docs - GitHub Copilot Instructions

## ABSOLUTE RULES - NO EXCEPTIONS

### 1. ALL WORK VIA PULL REQUESTS
- **NEVER commit directly to `main`.** All changes MUST go through PRs.

### 2. RFCs ARE READ-ONLY
- **DO NOT modify RFCs** — they live in `capiscio-rfcs/`, not here.

### 3. NO WATCH/BLOCKING COMMANDS
- **NEVER run blocking commands** without timeout

---

## CRITICAL: Read First

**Before starting work, read the workspace context files:**
1. `../../.context/CURRENT_SPRINT.md` - Sprint goals and priorities
2. `../../.context/ACTIVE_TASKS.md` - Active tasks

---

## Repository Purpose

**capiscio-docs** is the unified public documentation site for CapiscIO, published via MkDocs at docs.capisc.io.

It aggregates docs from multiple repos into a single site.

**Technology Stack**: MkDocs (Material theme), Python, Markdown

**Default Branch:** `main`

## Structure

```
capiscio-docs/
├── mkdocs.yml               # MkDocs configuration (nav, theme, plugins)
├── requirements-docs.txt    # Python deps (mkdocs, material, plugins)
├── docs/
│   ├── index.md             # Landing page
│   ├── getting-started/     # Quickstart, installation
│   ├── how-to/              # Task-oriented guides (integrations, middleware)
│   ├── reference/           # API reference (SDK, CLI, server)
│   ├── concepts/            # Architecture, trust model, DID
│   └── rfcs/                # RFC summaries (detail in capiscio-rfcs)
├── scripts/                 # Build/sync scripts
└── site/                    # Generated output (gitignored)
```

## Quick Commands

```bash
pip install -r requirements-docs.txt   # Install deps
mkdocs serve                           # Dev server (localhost:8000)
mkdocs build                           # Build static site
make serve                             # Alias for mkdocs serve
```

## Documentation Standards

- **Diataxis framework**: tutorials → how-to → reference → concepts
- **Cross-repo accuracy**: Docs must match actual SDK/server/core APIs
- Use `admonitions` for warnings/notes: `!!! warning`, `!!! note`
- Code examples must be tested or derived from actual working code
- When documenting SDK APIs, verify against `capiscio-sdk-python` source
- When documenting server APIs, verify against `capiscio-server` swagger
- Internal docs go in `internal-docs/` (workspace root), NOT here
