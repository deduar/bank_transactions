# Step 1 - PDF Inventory and Transaction Patterns

This document summarizes the transaction table patterns found in the sample PDFs
under `data/`. It is the reference for building per-bank parsers and the ETL
normalization layer.

## Provincial
Files:
- `data/provincial dl abril.pdf`
- `data/EstadoDeCuenta (13).pdf`

Primary header (most pages):
- `REF. CONCEPTO CARGOS ABONOS F. VALOR F. OPER.`

Typical row format:
- `4419 TPBW J0009508722 . TELESERVICIOS 02-04-2025 30,550.26 02-04-2025 30,651.63`

Inferred columns:
- `ref`: first numeric token
- `concept`: text between `ref` and first date
- `f_valor`: first date (DD-MM-YYYY)
- `amount`: single amount column (cargo or abono)
- `f_oper`: second date (DD-MM-YYYY)
- `saldo`: last amount on the row

Continuation page variation (seen in `EstadoDeCuenta (13).pdf`):
- Header order can change to: `CARGOS REF. ABONOS F. VALOR F. OPER. CONCEPTO SALDO`
- Parser must tolerate reordered columns.

Number format:
- Thousands separator `,` and decimal `.`, e.g. `30,550.26`

Rows to skip:
- `SALDO ANTERIOR`
- Footer lines like `Saldo a su favor`

## BDV (Banco de Venezuela)
Files:
- `data/Movimientos Venezuela.pdf`
- `data/persona_bdv_cuenta_0227.pdf`

Header:
- `Referencia Descripción Fecha Mov Débito Crédito Saldo`

Typical row format:
- `0677292001467 OPERACION PAGOMOVIL BDV 02/05/2025 NC 0,00 5.250,00 7.352,30`

Inferred columns:
- `ref`: first numeric token
- `description`: text until date
- `date`: DD/MM/YYYY
- `mov`: `ND` or `NC`
- `debit`, `credit`, `balance`

Number format:
- Thousands separator `.` and decimal `,`, e.g. `5.250,00`

Rows to skip:
- `SALDO INICIAL`
- Repeated headers on each page

## Banesco
File:
- `data/Banesco_cteMDEzNDAzNDgxODM0ODEwODc0NTc=-MDQyMDI1.pdf`

Header:
- `DIA REF. CONCEPTO CARGOS ABONOS SALDOS`

Typical row format:
- `01 09119003772 COMPRA POS CTA/CTE 1.046,07 1.395.843,17`

Inferred columns:
- `day`: two-digit day in month
- `ref`: numeric reference
- `concept`: text until amount
- `amount`: single amount column (cargo or abono)
- `saldo`: last amount on the row

Date handling:
- Only `day` appears per row; month and year are in the statement period
  (example: `Período: 04-2025`).

Number format:
- Thousands separator `.` and decimal `,`, e.g. `1.395.843,17`

Rows to skip:
- `SALDO MES ANTERIOR`
- Section headers like `DETALLE DE MOVIMIENTOS (continuación)`
