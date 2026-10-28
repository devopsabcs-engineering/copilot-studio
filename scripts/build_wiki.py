"""Export canonical documentation into GitHub wiki pages without cloud access."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(!?\[[^\]]*\])\(([^)\n]+)\)")


def render_wiki_metadata(text: str) -> str:
    metadata = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not metadata:
        raise ValueError("Canonical documentation must have YAML frontmatter.")
    title = re.search(r"^title:\s*(.+)$", metadata.group(1), re.M)
    if not title:
        raise ValueError("Canonical documentation must have a title.")
    heading = title.group(1).strip().strip("\"'")
    return f"# {heading}\n\n{text[metadata.end():].lstrip()}"


def page_name(path: Path, root: Path = ROOT) -> str:
    relative = path.resolve().relative_to(root.resolve())
    if relative == Path("README.md"):
        return "Home"
    if relative == Path("docs/publishing.md"):
        return "Publishing"
    if len(relative.parts) == 3 and relative.parts[1] in ("en", "fr"):
        return f"{relative.parts[1].upper()}-{relative.stem}"
    raise ValueError(f"No wiki page mapping for {relative}")


def rewrite_links(text: str, source: Path, root: Path = ROOT) -> str:
    def rewrite(match: re.Match[str]) -> str:
        label, target = match.groups()
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match.group(0)
        path = (source.parent / unquote(parsed.path)).resolve()
        relative = path.relative_to(root.resolve())
        fragment = f"#{parsed.fragment}" if parsed.fragment else ""
        if path.suffix == ".md":
            destination = page_name(path, root)
        elif relative.parts[:2] == ("docs", "assets"):
            destination = Path(*relative.parts[1:]).as_posix()
        elif relative.parts[0] == "scripts":
            destination = f"https://github.com/devopsabcs-engineering/copilot-studio/blob/main/{relative.as_posix()}"
        else:
            raise ValueError(f"Unsupported wiki link {target} in {source}")
        return f"{label}({destination}{fragment})"

    return LINK.sub(rewrite, text)


def export(output: Path, root: Path = ROOT) -> int:
    output, root = output.resolve(), root.resolve()
    docs = root / "docs"
    if output == root or output == docs or docs in output.parents:
        raise ValueError("Wiki output must not overwrite the repository root or canonical docs.")
    output.mkdir(parents=True, exist_ok=True)
    sources = [root / "README.md", *sorted(docs.rglob("*.md"))]
    for source in sources:
        content = render_wiki_metadata(rewrite_links(source.read_text(encoding="utf-8"), source, root))
        (output / f"{page_name(source, root)}.md").write_text(content, encoding="utf-8", newline="\n")
    shutil.copytree(docs / "assets", output / "assets", dirs_exist_ok=True)
    sidebar = """## English | Français

* [Home / Accueil](Home)
* [English guides](EN-index)
* [Guides français](FR-index)
* [Validation EN](EN-validation)
* [Validation FR](FR-validation)
* [Completion roadmap](EN-completion-roadmap)
* [Feuille de route](FR-completion-roadmap)
* [Evidence](EN-evidence)
* [Preuves](FR-evidence)
* [Publication](Publishing)
"""
    for language in ("EN", "FR"):
        sidebar += f"\n### {language}\n\n"
        for lab in ("00", "01", "02", "03", "04", "05-1", "05", "06"):
            sidebar += f"* [Lab {lab.replace('05-1', '5.1')}]({language}-lab-{lab})\n"
    (output / "_Sidebar.md").write_text(sidebar, encoding="utf-8", newline="\n")
    (output / "_Footer.md").write_text("""## Evidence / Preuves

Source screenshots are not new executions. Les captures d'origine ne sont pas de nouvelles exécutions.
See [validation](EN-validation) / voir le [registre](FR-validation).
""", encoding="utf-8", newline="\n")
    return len(sources) + 2


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    count = export(args.output)
    print(f"Exported {count} wiki Markdown files and shared assets to {args.output.resolve()}")


if __name__ == "__main__":
    main()
