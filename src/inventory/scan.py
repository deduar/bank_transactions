from pathlib import Path
import re
from typing import Dict, List, Optional

from ingest.pdf_loader import extract_lines
from inventory.patterns import (
    BANESCO_HEADER_PATTERN,
    BANESCO_ROW_PATTERN,
    BDV_HEADER_PATTERN,
    BDV_ROW_PATTERN,
    PROVINCIAL_HEADER_PATTERNS,
    PROVINCIAL_ROW_PATTERNS,
    SKIP_LINE_PATTERNS,
)


def _should_skip(line: str) -> bool:
    return any(pattern.search(line) for pattern in SKIP_LINE_PATTERNS)


_DATE_END_PATTERN = re.compile(r"\d{2}[-/]\d{2}[-/]\d{4}$")
_AMOUNT_ONLY_PATTERN = re.compile(r"^[\d,.]+\d{2,3}$")
_DATE_ANY_PATTERN = re.compile(r"\d{2}[-/]\d{2}[-/]\d{4}")


def _merge_amount_continuations(lines: List[str]) -> List[str]:
    merged: List[str] = []
    for line in lines:
        if (
            merged
            and _DATE_END_PATTERN.search(merged[-1])
            and _AMOUNT_ONLY_PATTERN.match(line)
        ):
            merged[-1] = f"{merged[-1]} {line}"
        else:
            merged.append(line)
    return merged


def _detect_bank(lines: List[str]) -> Optional[str]:
    if any(
        pattern.search(line)
        for pattern in PROVINCIAL_HEADER_PATTERNS
        for line in lines
    ) or any(
        pattern.match(line)
        for pattern in PROVINCIAL_ROW_PATTERNS
        for line in lines
    ):
        return "provincial"
    if any(BDV_HEADER_PATTERN.search(line) for line in lines) or any(
        BDV_ROW_PATTERN.match(line) for line in lines
    ):
        return "bdv"
    if any(BANESCO_HEADER_PATTERN.search(line) for line in lines) or any(
        BANESCO_ROW_PATTERN.match(line) for line in lines
    ):
        return "banesco"
    return None


def _collect_samples(lines: List[str], row_pattern, sample_limit: int) -> Dict[str, object]:
    samples: List[str] = []
    match_count = 0

    for line in lines:
        if _should_skip(line):
            continue
        if row_pattern.match(line):
            match_count += 1
            if len(samples) < sample_limit:
                samples.append(line)

    return {"match_count": match_count, "samples": samples}


def _collect_line_samples(lines: List[str], limit: int = 5) -> List[str]:
    samples: List[str] = []
    for line in lines:
        if _should_skip(line):
            continue
        if _DATE_ANY_PATTERN.search(line) or line[:1].isdigit():
            samples.append(line)
        if len(samples) >= limit:
            break
    if not samples:
        samples = lines[:limit]
    return samples


def scan_pdf(pdf_path: Path, sample_limit: int = 5) -> Dict[str, object]:
    lines = _merge_amount_continuations(extract_lines(pdf_path))
    bank = _detect_bank(lines)

    if bank == "provincial":
        samples = {"match_count": 0, "samples": []}
        for pattern in PROVINCIAL_ROW_PATTERNS:
            candidate = _collect_samples(lines, pattern, sample_limit)
            if candidate["match_count"] > samples["match_count"]:
                samples = candidate
        headers = [
            line
            for line in lines
            if any(pat.search(line) for pat in PROVINCIAL_HEADER_PATTERNS)
        ]
    elif bank == "bdv":
        samples = _collect_samples(lines, BDV_ROW_PATTERN, sample_limit)
        headers = [line for line in lines if BDV_HEADER_PATTERN.search(line)]
    elif bank == "banesco":
        samples = _collect_samples(lines, BANESCO_ROW_PATTERN, sample_limit)
        headers = [line for line in lines if BANESCO_HEADER_PATTERN.search(line)]
    else:
        samples = {"match_count": 0, "samples": []}
        headers = []

    report = {
        "file": pdf_path.name,
        "bank": bank,
        "header_matches": headers[:3],
        "row_match_count": samples["match_count"],
        "sample_rows": samples["samples"],
    }
    if bank is None:
        report["line_samples"] = _collect_line_samples(lines)
    return report


def inventory_pdfs(input_dir: Path, sample_limit: int = 5) -> Dict[str, object]:
    pdf_files = sorted(input_dir.glob("*.pdf"))
    reports = [scan_pdf(pdf_file, sample_limit=sample_limit) for pdf_file in pdf_files]
    return {
        "input_dir": str(input_dir),
        "count": len(pdf_files),
        "reports": reports,
    }
