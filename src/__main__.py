import argparse
import json
from pathlib import Path

from inventory.scan import inventory_pdfs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bank transaction PDF utilities."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory_parser = subparsers.add_parser(
        "inventory", help="Scan PDFs and collect transaction patterns."
    )
    inventory_parser.add_argument(
        "--input",
        type=Path,
        default=Path("data"),
        help="Directory containing PDF files.",
    )
    inventory_parser.add_argument(
        "--output",
        type=Path,
        default=Path("out/step1-inventory.json"),
        help="Path to write the JSON report.",
    )
    inventory_parser.add_argument(
        "--sample-limit",
        type=int,
        default=5,
        help="Maximum number of sample rows per file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "inventory":
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

    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
