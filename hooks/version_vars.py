"""MkDocs hook: replace version placeholders in markdown content.

Replaces {{ capiscio_version }} and {{ protocol_version }} with values
defined in mkdocs.yml extra: config. This avoids the macros plugin which
conflicts with GitHub Actions {{ }} syntax in code examples.
"""

VERSION_KEYS = {"capiscio_version", "protocol_version"}


def on_page_markdown(markdown, page, config, files):
    """Replace version placeholders before markdown rendering."""
    extra = config.get("extra", {})
    for key in VERSION_KEYS:
        value = extra.get(key)
        if value:
            markdown = markdown.replace("{{ " + key + " }}", str(value))
    return markdown
