"""Check bilingual coverage, metadata, links, image provenance, and wiki output."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(!?\[[^\]]*\])\(([^)\n]+)\)")


def local_link_errors(path: Path, wiki: bool = False) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.S)
    for label, target in LINK.findall(text):
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        dest = path.parent / unquote(parsed.path)
        if wiki and not dest.suffix and not dest.exists():
            dest = dest.with_suffix(".md")
        if not dest.exists():
            errors.append(f"{path.name}: broken link {target}")
        if label.startswith("![") and not label[2:-1].strip():
            errors.append(f"{path.name}: image lacks alternate text: {target}")
    return errors


def validate(root: Path = ROOT, wiki: Path | None = None) -> tuple[list[str], dict[str, int]]:
    errors = []
    files = [root / "README.md", *sorted((root / "docs").rglob("*.md"))]
    en = {p.name for p in (root / "docs/en").glob("*.md")}
    fr = {p.name for p in (root / "docs/fr").glob("*.md")}
    if en != fr:
        errors.append(f"Bilingual page mismatch: EN-only {sorted(en-fr)}, FR-only {sorted(fr-en)}")
    required = {"index.md", "validation.md", "evidence.md", "platform-changes.md", "troubleshooting.md"}
    required |= {f"lab-{lab}.md" for lab in ("00", "01", "02", "03", "04", "05", "05-1", "06")}
    if not required <= en:
        errors.append(f"Missing required guides: {sorted(required-en)}")
    for path in files:
        text = path.read_text(encoding="utf-8")
        metadata = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        if not metadata:
            errors.append(f"{path}: missing YAML frontmatter")
        else:
            for field in ("title", "description", "ms.date"):
                if not re.search(rf"^{re.escape(field)}:\s*\S", metadata.group(1), re.M):
                    errors.append(f"{path}: missing {field}")
        if not text.endswith("\n") or text.endswith("\n\n"):
            errors.append(f"{path}: expected exactly one final newline")
        if re.search(r"^# ", text, re.M):
            errors.append(f"{path}: H1 duplicates frontmatter title")
        errors.extend(local_link_errors(path))
    for name in sorted(en & fr):
        en_text = (root / "docs/en" / name).read_text(encoding="utf-8")
        fr_text = (root / "docs/fr" / name).read_text(encoding="utf-8")
        en_images = set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", en_text))
        fr_images = set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", fr_text))
        if en_images != fr_images:
            errors.append(f"{name}: screenshots differ between languages")
        if len(fr_text.split()) < len(en_text.split()) * 0.65:
            errors.append(f"{name}: French content is unexpectedly short; inspect translation parity")
    manifest_path = root / "docs/assets/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    listed = set()
    for item in manifest:
        path = root / item["file"]
        if not path.is_file():
            errors.append(f"Missing manifested screenshot: {item['file']}")
        if not item.get("source") or not item.get("kind"):
            errors.append(f"Missing provenance: {item['file']}")
        listed.add(path.resolve())
    for path in (root / "docs/assets").rglob("*.png"):
        if path.resolve() not in listed:
            errors.append(f"Screenshot lacks provenance: {path}")
    wiki_files = []
    if wiki:
        wiki_files = sorted(wiki.glob("*.md"))
        if len(wiki_files) < len(files) + 2:
            errors.append("Wiki export is missing Markdown pages")
        for path in wiki_files:
            errors.extend(local_link_errors(path, wiki=True))
    counts = {"markdown_files": len(files), "bilingual_pairs": len(en & fr),
              "screenshots": len(manifest), "wiki_markdown_files": len(wiki_files)}
    return errors, counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    errors, counts = validate(wiki=args.wiki)
    report = {"checks": counts, "errors": errors, "passed": not errors}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
