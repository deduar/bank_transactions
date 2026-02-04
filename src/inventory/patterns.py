import re

PROVINCIAL_HEADER_PATTERNS = [
    re.compile(
        r"REF\.?\s+CONCEPTO\s+CARGOS\s+ABONOS\s+F\.?\s+VALOR\s+F\.?\s+OPER\.?",
        re.IGNORECASE,
    ),
    re.compile(
        r"CARGOS\s+REF\.?\s+ABONOS\s+F\.?\s+VALOR\s+F\.?\s+OPER\.?\s+CONCEPTO\s+SALDO",
        re.IGNORECASE,
    ),
    re.compile(
        r"F\.?\s+OPER\.?\s+REF\.?\s+CONCEPTO\s+CARGOS\s+ABONOS\s+F\.?\s+VALOR",
        re.IGNORECASE,
    ),
]

PROVINCIAL_ROW_PATTERNS = [
    re.compile(
        r"^(?P<ref>\d{4,})\s+"
        r"(?P<concept>.+?)\s+"
        r"(?P<f_valor>\d{2}-\d{2}-\d{4})\s+"
        r"(?P<amount>[\d,]+\.\d{2})\s+"
        r"(?P<f_oper>\d{2}-\d{2}-\d{4})\s+"
        r"(?P<saldo>[\d,]+\.\d{2})$"
    ),
    re.compile(
        r"^(?P<f_oper>\d{2}-\d{2}-\d{4})\s+"
        r"(?P<ref>\d{4,})\s+"
        r"(?P<concept>.+?)\s+"
        r"(?P<f_valor>\d{2}-\d{2}-\d{4})\s+"
        r"(?P<amount>[\d,]+\.\d{2})\s+"
        r"(?P<saldo>[\d,]+\.\d{2})$"
    ),
]

BDV_HEADER_PATTERN = re.compile(
    r"Referencia\s+Descripci[oó]n\s+Fecha\s+Mov\s+Débito\s+Cr[eé]dito\s+Saldo",
    re.IGNORECASE,
)

BDV_ROW_PATTERN = re.compile(
    r"^(?P<ref>\d{10,})\s+"
    r"(?P<description>.+?)\s+"
    r"(?P<date>\d{2}/\d{2}/\d{4})\s+"
    r"(?P<mov>ND|NC)\s+"
    r"(?P<debit>-?[\d\.]+,\d{2})\s+"
    r"(?P<credit>[\d\.]+,\d{2})\s+"
    r"(?P<balance>[\d\.]+,\d{2})$"
)

BANESCO_HEADER_PATTERN = re.compile(
    r"DIA\s+REF\.\s+CONCEPTO\s+CARGOS\s+ABONOS\s+SALDOS",
    re.IGNORECASE,
)

BANESCO_ROW_PATTERN = re.compile(
    r"^(?P<day>\d{2})\s+"
    r"(?P<ref>\d{5,})\s+"
    r"(?P<concept>.+?)\s+"
    r"(?P<amount>[\d\.]+,\d{2})\s+"
    r"(?P<saldo>[\d\.]+,\d{2})$"
)

SKIP_LINE_PATTERNS = [
    re.compile(r"^SALDO\s+ANTERIOR", re.IGNORECASE),
    re.compile(r"^SALDO\s+MES\s+ANTERIOR", re.IGNORECASE),
    re.compile(r"^SALDO\s+INICIAL", re.IGNORECASE),
    re.compile(r"DETALLE\s+DE\s+MOVIMIENTOS\s+\(continuaci[oó]n\)", re.IGNORECASE),
    re.compile(r"^Saldo\s+a\s+su\s+favor", re.IGNORECASE),
]
