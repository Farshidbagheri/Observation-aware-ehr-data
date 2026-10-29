"""Check GitHub-facing research material against tracked files, without network access."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def local_references(markdown: Path):
    text = markdown.read_text(encoding="utf-8")
    for raw in LINK.findall(text):
        url = raw.split(" ", 1)[0].strip("<>")
        if not url or url.startswith(("#", "mailto:", "data:")):
            continue
        parts = urlparse(url)
        if parts.scheme or parts.netloc:
            continue
        target = unquote(parts.path)
        if target:
            yield url, (markdown.parent / target).resolve()


def test_all_repo_markdown_file_links_exist():
    missing = []
    for doc in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")),
                *sorted((ROOT / "evidence").glob("*.md"))]:
        for url, target in local_references(doc):
            if not target.is_relative_to(ROOT) or not target.exists():
                missing.append((str(doc.relative_to(ROOT)), url))
    assert not missing, "Broken research Markdown references: " + repr(missing)


def test_readme_is_mobile_friendly_and_has_attribution():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Farshid Bagheri Saravi" in readme
    assert "CITATION.cff" in readme
    assert "evidence/publication_atlas/figures/01_observation_atlas.png" in readme
    assert "badge.svg" not in readme
    assert "[![" not in readme
    assert "| ![" not in readme  # image tables become unreadable on phones


def test_figures_and_source_audit_are_committed():
    figures = ROOT / "evidence" / "publication_atlas" / "figures"
    assert len(list(figures.glob("*.png"))) == 7
    assert len(list(figures.glob("*.svg"))) == 7
    for path in figures.glob("*.png"):
        assert path.with_suffix(".svg").exists()
    assert (ROOT / "evidence/publication_atlas/aggregate_results.json").exists()
    assert (ROOT / "evidence/publication_atlas/all_source_schema_inventory.json").exists()
