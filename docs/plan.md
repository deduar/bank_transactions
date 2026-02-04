---
name: PDF transactions extraction
overview: Design a Python ETL-style pipeline to extract only bank transactions from PDF statements, normalize fields (dates, numbers), and output them as JSON using reference/ref as the transaction index while ignoring customer/bank metadata.
todos:
  - id: pdf-inventory
    content: Review PDFs and map transaction table formats
    status: pending
  - id: schema-define
    content: Define normalized transaction JSON schema
    status: pending
  - id: parser-impl
    content: Implement bank-specific parsers + common utils
    status: pending
  - id: cli-batch
    content: Build CLI for batch processing to JSON
    status: pending
  - id: validate-output
    content: Validate outputs and spot-check samples
    status: pending
isProject: false
---

# PDF Transactions Extraction Plan

## Scope and assumptions

- PDFs are currently in the repo root (e.g., `Banesco_cteMDEzNDAzNDgxODM0ODEwODc0NTc=-MDQyMDI1.pdf`, `provincial dl abril.pdf`), while `/home/tech/Viko/src/bank_transactions/data` is empty.
- We will extract only transactions and ignore bank/customer metadata except what is needed to parse.
- We will add a normalization/transformation layer to standardize dates, numeric formats, currency, and description text.
- Each transaction will include a `ref` (reference) field used as the primary index in outputs.
- Output format: JSON files.

## Plan

1. **Inventory sample PDFs and transaction table patterns**
  - Read each sample PDF to identify the transactions section, column headers (date, description/concept, ref, debit/credit, balance), and any per-bank layout differences.
  - Document per-bank patterns and edge cases (multi-line descriptions, missing refs, date formats).
2. **Define a normalized transaction schema**
  - Create a JSON schema for a transaction with fields like `ref`, `date`, `description`, `amount`, `currency`, `type` (debit/credit), `balance`, and `source_file`.
  - Define a stable output structure: one JSON file per input PDF (e.g., `output/<pdf_name>.json`).
3. **Add an ETL normalization/transformation layer**
  - Implement normalization functions for date parsing (multiple formats), numeric parsing (comma/decimal variations), currency inference, and description cleanup.
  - Map raw extracted fields into the normalized schema before output.
4. **Build the PDF parsing pipeline in Python**
  - Use `pdfplumber` for text extraction; add `camelot` or `tabula` if tables require structured extraction.
  - Implement bank-specific parsers (Banesco, BDV, Provincial) with a common interface and fallbacks.
  - Use regex rules to locate transaction rows and extract `ref` reliably.
5. **Add validation and de-duplication**
  - Validate required fields; skip non-transaction rows (headers, totals).
  - Use `ref` as the primary key; handle duplicates by keeping first/last occurrence per file (document rule).
6. **CLI and batch processing**
  - Create a CLI script to process a folder of PDFs and write JSON outputs.
  - Include flags for input directory and output directory.
7. **Testing and sample outputs**
  - Run the parser on the provided PDFs and store outputs under `output/`.
  - Spot-check a few transactions per bank to ensure accuracy.

## Key files to create

- `parser/` (new module)
  - `parser/base.py` (common interfaces)
  - `parser/banesco.py`, `parser/bdv.py`, `parser/provincial.py` (bank-specific rules)
  - `parser/utils.py` (regex helpers)
  - `parser/normalize.py` (ETL normalization/transformation)
- `cli.py` (entry point for batch processing)
- `output/` (generated JSON files)

## Notes

- If you later want to ingest PDFs from `/data`, we can redirect the CLI input path accordingly.
- If any bank statements lack a `ref`, we will define a fallback key (hash of date+description+amount) but still include `ref` when present.
