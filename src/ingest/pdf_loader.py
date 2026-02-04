from pathlib import Path
import re
from typing import List


def _import_pdfplumber():
    try:
        import pdfplumber  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment-specific
        raise ImportError(
            "Missing dependency: pdfplumber. "
            "Install it with `pip install pdfplumber`."
        ) from exc
    return pdfplumber


_DATE_PATTERN = r"\d{2}[-/]\d{2}[-/]\d{4}"


def _normalize_line(raw_line: str) -> str:
    line = " ".join(raw_line.split())
    if not line:
        return ""
    # Fix common PDF extraction concatenations like "TELESERVICIOS02-06-2025".
    line = re.sub(rf"([A-Za-z])({_DATE_PATTERN})", r"\1 \2", line)
    # Fix amount + date concatenation like "7,860.0002-06-2025".
    line = re.sub(rf"([\d\.,]+\d{{2}})({_DATE_PATTERN})", r"\1 \2", line)
    # Fix amount + date where amount has 3 decimals.
    line = re.sub(rf"([\d\.,]+\d{{3}})({_DATE_PATTERN})", r"\1 \2", line)
    return line


def extract_lines(pdf_path: Path) -> List[str]:
    """Extract normalized text lines from a PDF."""
    pdfplumber = _import_pdfplumber()
    lines: List[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for raw_line in text.splitlines():
                line = _normalize_line(raw_line)
                if line:
                    lines.append(line)
    return lines
