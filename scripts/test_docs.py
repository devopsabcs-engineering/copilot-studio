"""Offline regression tests for documentation export and link validation."""
from pathlib import Path
import tempfile
import unittest

from build_wiki import export, page_name, rewrite_links
from validate_docs import local_link_errors, validate


class WikiTests(unittest.TestCase):
    def test_page_names(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(page_name(root / "README.md"), "Home")
        self.assertEqual(page_name(root / "docs/fr/lab-05-1.md"), "FR-lab-05-1")

    def test_relative_links_and_images(self):
        root = Path(__file__).resolve().parents[1]
        source = root / "docs/en/lab-01.md"
        text = "[FR](../fr/lab-01.md) ![Image](../assets/lab-01/image2.png) [Web](https://example.org/a)"
        result = rewrite_links(text, source)
        self.assertIn("[FR](FR-lab-01)", result)
        self.assertIn("![Image](assets/lab-01/image2.png)", result)
        self.assertIn("[Web](https://example.org/a)", result)

    def test_fragment_is_preserved(self):
        root = Path(__file__).resolve().parents[1]
        result = rewrite_links("[Guide](index.md#start-here)", root / "docs/en/lab-01.md")
        self.assertEqual(result, "[Guide](EN-index#start-here)")

    def test_export_does_not_overwrite_sources(self):
        root = Path(__file__).resolve().parents[1]
        with self.assertRaises(ValueError):
            export(root / "docs/en")
        with self.assertRaises(ValueError):
            export(root)

    def test_broken_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "page.md"
            path.write_text("[Missing](missing.md)\n", encoding="utf-8")
            self.assertEqual(len(local_link_errors(path)), 1)

    def test_export_and_repository_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            export(Path(directory))
            errors, counts = validate(wiki=Path(directory))
            self.assertEqual(errors, [])
            self.assertGreaterEqual(counts["bilingual_pairs"], 13)
            self.assertGreaterEqual(counts["screenshots"], 29)


if __name__ == "__main__":
    unittest.main()
