import argparse
import json
from pathlib import Path

from inventory.scan import inventory_pdfs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory transaction patterns from PDFs."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data"),
        help="Directory containing PDF files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("out/step1-inventory.json"),
        help="Path to write the JSON report.",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=5,
        help="Maximum number of sample rows per file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    report = inventory_pdfs(
        input_dir=args.input, sample_limit=args.sample_limit
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote inventory report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
