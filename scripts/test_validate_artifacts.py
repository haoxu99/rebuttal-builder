#!/usr/bin/env python3
"""Regression tests for validate_artifacts.py."""

from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

import validate_artifacts as validator


class ArtifactValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write(self, name: str, text: str) -> Path:
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_exact_quotes_pass_and_paraphrase_fails(self) -> None:
        source = self.write(
            "reviews.txt",
            "The idea is promising. Please compare against Baseline X.",
        )
        exact = self.write(
            "digest.md",
            "## R1-P01\n\n> The idea is promising.\n\n"
            "## R1-Q01\n\n> Please compare against Baseline X.\n",
        )
        self.assertEqual(validator.validate_quotes([source], exact), [])
        paraphrased = self.write(
            "bad.md",
            "## R1-Q01\n\n> Please compare with Baseline X.\n",
        )
        self.assertTrue(validator.validate_quotes([source], paraphrased))

    def test_docx_split_runs_remain_contiguous(self) -> None:
        source = self.root / "reviews.docx"
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:body><w:p><w:r><w:t>Base</w:t></w:r>'
            '<w:r><w:t>line X</w:t></w:r></w:p></w:body></w:document>'
        )
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("word/document.xml", xml)
        digest = self.write("digest.md", "## R1-Q01\n\n> Baseline X\n")
        self.assertEqual(validator.validate_quotes([source], digest), [])

    def test_grouping_requires_exact_transfer_and_complete_coverage(self) -> None:
        digest = self.write(
            "digest.md",
            "## R1-Q01\n\n> Question one.\n\n"
            "## R2-Q01\n\n> Question two.\n",
        )
        grouped = self.write(
            "grouped.md",
            "## R1-Q01 — Reviewer R1\n\n> Question one.\n\n"
            "## R2-Q01 — Reviewer R2\n\n> Question two.\n\n"
            "- [ ] R1-Q01 → P0\n- [ ] R2-Q01 → P1\n",
        )
        self.assertEqual(validator.validate_grouping(digest, grouped), [])
        missing = self.write(
            "missing.md",
            "## R1-Q01 — Reviewer R1\n\n> Question one.\n\n"
            "- [ ] R1-Q01 → P0\n",
        )
        self.assertTrue(validator.validate_grouping(digest, missing))

    def test_word_count_ignores_title_and_audit_metadata(self) -> None:
        text = "# Rebuttal\n\n" + "word " * 1000
        text += "\n<!-- AUDIT START -->\nWord count: 1000\n<!-- AUDIT END -->\n"
        rebuttal = self.write("rebuttal.md", text)
        count, errors = validator.validate_count(rebuttal, 900, 1100)
        self.assertEqual(count, 1000)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
