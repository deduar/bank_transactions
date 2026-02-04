## Usage Guide (Incremental)

This document is updated as each pipeline step is implemented.

### Step 1 — PDF inventory

Purpose: scan PDFs and extract transaction table patterns + sample rows.

#### Run in container

1. Start container (idle):
   - `docker compose up -d --build`
2. Execute inventory:
   - `docker exec -it bank-transactions python -m inventory --input data`
   - Optional: override output path with `--output out/step1-inventory.json`
   - Optional: override sample count with `--sample-limit 5`
   - Full example (all args):
     `docker exec -it bank-transactions python -m inventory --input data --output out/step1-inventory.json --sample-limit 5`

#### Run locally (no Docker)

- `PYTHONPATH=src python -m inventory --input data --output out/step1-inventory.json`

#### Output

- Default output file: `out/step1-inventory.json`
- Result: `out/step1-inventory.json` (overwritten on each run)

#### Notes

- Warnings like `Could not get FontBBox...` are common PDF parsing warnings and
  do not stop the output generation.
