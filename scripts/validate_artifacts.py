#!/usr/bin/env python3
"""Validate verbatim quotes, cross-artifact coverage, and rebuttal length."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


ID_RE = re.compile(r"\b(?:R\d+|MR)-(?:P|Q)\d+\b", re.IGNORECASE)
HEADING_ID_RE = re.compile(
    r"^#{2,6}\s+((?:R\d+|MR)-(?:P|Q)\d+)\b", re.IGNORECASE
)
CHECKLIST_RE = re.compile(
    r"^-\s*\[[ xX]\]\s*((?:R\d+|MR)-Q\d+)\s*(?:→|->)", re.IGNORECASE
)
AUDIT_START = "<!-- AUDIT START -->"


def normalize_ws(text: str) -> str:
    """Normalize extraction-only whitespace without changing punctuation or words."""
    return re.sub(r"\s+", " ", text).strip()


def read_docx(path: Path) -> str:
    parts: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = ["word/document.xml"]
        names += sorted(
            name
            for name in archive.namelist()
            if re.fullmatch(r"word/(?:comments|footnotes|endnotes)\.xml", name)
        )
        for name in names:
            if name not in archive.namelist():
                continue
            root = ET.fromstring(archive.read(name))
            # Concatenate text runs inside each paragraph. Word often splits one
            # visible token across several w:t nodes, so adding spaces per run
            # would make faithful quotations fail.
            for paragraph in (node for node in root.iter() if node.tag.endswith("}p")):
                paragraph_parts: list[str] = []
                for element in paragraph.iter():
                    if element.tag.endswith("}t") and element.text:
                        paragraph_parts.append(element.text)
                    elif element.tag.endswith(("}tab", "}br", "}cr")):
                        paragraph_parts.append(" ")
                text = "".join(paragraph_parts)
                if text:
                    parts.append(text)
    return " ".join(parts)


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "PDF validation requires pypdf; use the workspace Python runtime or "
            "manually verify the quotes."
        ) from exc
    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)


def read_source(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".pdf":
        return read_pdf(path)
    if suffix in {".md", ".txt", ".rst", ".csv", ".tsv"}:
        return path.read_text(encoding="utf-8")
    raise RuntimeError(f"Unsupported source format: {path}")


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_id_quotes(markdown: str) -> tuple[dict[str, str], list[str]]:
    """Return stable-ID blockquotes and structural errors from a Markdown artifact."""
    lines = markdown.splitlines()
    entries: dict[str, str] = {}
    errors: list[str] = []
    current_id: str | None = None
    quote_lines: list[str] = []

    def finish() -> None:
        nonlocal current_id, quote_lines
        if current_id is None:
            return
        quote = normalize_ws(" ".join(quote_lines))
        if not quote:
            errors.append(f"{current_id}: missing blockquote")
        elif current_id in entries:
            errors.append(f"{current_id}: duplicate primary quote entry")
        else:
            entries[current_id] = quote
        current_id = None
        quote_lines = []

    for line in lines:
        match = HEADING_ID_RE.match(line.strip())
        if match:
            finish()
            current_id = match.group(1).upper()
            continue
        if current_id is not None and line.lstrip().startswith(">"):
            quote_lines.append(re.sub(r"^\s*>\s?", "", line))
    finish()
    return entries, errors


def has_placeholder(text: str) -> bool:
    return bool(re.search(r"\[(?:EXACT|COPY THE EXACT|FILENAME)", text, re.IGNORECASE))


def validate_quotes(sources: list[Path], artifact: Path) -> list[str]:
    source_texts = [normalize_ws(read_source(path)) for path in sources]
    artifact_text = read_markdown(artifact)
    quotes, errors = extract_id_quotes(artifact_text)
    if not quotes:
        errors.append("No stable-ID blockquotes found in digest")
        return errors
    for stable_id, quote in quotes.items():
        if has_placeholder(quote):
            errors.append(f"{stable_id}: unresolved template placeholder")
        elif not any(quote in source_text for source_text in source_texts):
            errors.append(
                f"{stable_id}: quote is not an exact contiguous source substring "
                "after whitespace normalization"
            )
    return errors


def validate_grouping(digest: Path, grouped: Path) -> list[str]:
    digest_text = read_markdown(digest)
    grouped_text = read_markdown(grouped)
    digest_quotes, errors = extract_id_quotes(digest_text)
    grouped_quotes, grouped_errors = extract_id_quotes(grouped_text)
    errors.extend(grouped_errors)

    actionable = {key for key in digest_quotes if "-Q" in key}
    praise = {key for key in digest_quotes if "-P" in key}

    for stable_id, quote in grouped_quotes.items():
        if stable_id not in digest_quotes:
            errors.append(f"{stable_id}: grouped ID does not exist in digest")
        elif quote != digest_quotes[stable_id]:
            errors.append(f"{stable_id}: grouped quote differs from digest")

    missing = sorted(actionable - set(grouped_quotes))
    if missing:
        errors.append("Actionable IDs missing from grouped primary entries: " + ", ".join(missing))

    unexpected_praise = sorted(set(grouped_quotes) & praise)
    if unexpected_praise:
        errors.append(
            "Praise IDs should not be primary concern entries: " + ", ".join(unexpected_praise)
        )

    checklist_ids = [
        match.group(1).upper()
        for line in grouped_text.splitlines()
        if (match := CHECKLIST_RE.match(line.strip()))
    ]
    counts = Counter(checklist_ids)
    for stable_id in sorted(actionable):
        if counts[stable_id] == 0:
            errors.append(f"{stable_id}: missing from coverage checklist")
        elif counts[stable_id] > 1:
            errors.append(f"{stable_id}: appears multiple times in coverage checklist")
    unknown = sorted(set(checklist_ids) - actionable)
    if unknown:
        errors.append("Unknown/non-actionable coverage IDs: " + ", ".join(unknown))
    return errors


def rebuttal_body(markdown: str) -> str:
    body = markdown.split(AUDIT_START, 1)[0]
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = re.sub(r"^#\s+.*$", " ", body, count=1, flags=re.MULTILINE)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"`([^`]*)`", r"\1", body)
    body = re.sub(r"!?(?:\[([^\]]*)\])\([^)]*\)", r"\1", body)
    body = re.sub(r"[*_>#]", " ", body)
    return body


def count_words(markdown: str) -> int:
    # Count English-style word/number tokens; punctuation and Markdown are excluded.
    return len(re.findall(r"[A-Za-z0-9]+(?:['’.-][A-Za-z0-9]+)*", rebuttal_body(markdown)))


def validate_count(artifact: Path, minimum: int, maximum: int) -> tuple[int, list[str]]:
    text = read_markdown(artifact)
    count = count_words(text)
    errors: list[str] = []
    if count < minimum or count > maximum:
        errors.append(f"Rebuttal word count {count} is outside [{minimum}, {maximum}]")
    if re.search(r"\[(?:RESULT|SETTING|MANUSCRIPT LOCATION|AUTHOR CONFIRMATION) NEEDED\]", text):
        errors.append("Rebuttal contains unresolved evidence/confirmation placeholders")
    return count, errors


def print_result(errors: list[str], extra: str | None = None) -> int:
    if extra:
        print(extra)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


def add_sources(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--source", type=Path, action="append", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    quotes = sub.add_parser("quotes", help="Check digest quotes against source files")
    add_sources(quotes)
    quotes.add_argument("--artifact", type=Path, required=True)

    grouping = sub.add_parser("grouping", help="Check exact quote transfer and coverage")
    grouping.add_argument("--digest", type=Path, required=True)
    grouping.add_argument("--grouped", type=Path, required=True)

    count = sub.add_parser("count", help="Count and gate rebuttal body words")
    count.add_argument("--artifact", type=Path, required=True)
    count.add_argument("--min", type=int, default=900)
    count.add_argument("--max", type=int, default=1100)

    all_checks = sub.add_parser("all", help="Run quote, grouping, and count checks")
    add_sources(all_checks)
    all_checks.add_argument("--digest", type=Path, required=True)
    all_checks.add_argument("--grouped", type=Path, required=True)
    all_checks.add_argument("--rebuttal", type=Path, required=True)
    all_checks.add_argument("--min", type=int, default=900)
    all_checks.add_argument("--max", type=int, default=1100)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "quotes":
            return print_result(validate_quotes(args.source, args.artifact))
        if args.command == "grouping":
            return print_result(validate_grouping(args.digest, args.grouped))
        if args.command == "count":
            count, errors = validate_count(args.artifact, args.min, args.max)
            return print_result(errors, f"Word count: {count}")
        errors = validate_quotes(args.source, args.digest)
        errors.extend(validate_grouping(args.digest, args.grouped))
        count, count_errors = validate_count(args.rebuttal, args.min, args.max)
        errors.extend(count_errors)
        return print_result(errors, f"Word count: {count}")
    except (OSError, RuntimeError, zipfile.BadZipFile, ET.ParseError) as exc:
        return print_result([str(exc)])


if __name__ == "__main__":
    sys.exit(main())
