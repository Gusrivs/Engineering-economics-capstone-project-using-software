from __future__ import annotations

from datetime import date
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")

def money(value) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)

def simple_interest(principal, annual_rate_percent, periods, periods_per_year=12):
    p, r, n = money(principal), Decimal(str(annual_rate_percent)) / 100, Decimal(str(periods))
    interest = money(p * r * n / Decimal(str(periods_per_year)))
    return {"principal": p, "interest": interest, "total": money(p + interest)}

def compound_interest(principal, annual_rate_percent, periods, periods_per_year=12):
    p = money(principal)
    rate = Decimal(str(annual_rate_percent)) / 100 / Decimal(str(periods_per_year))
    total = money(p * ((Decimal("1") + rate) ** int(periods)))
    return {"principal": p, "interest": money(total - p), "total": total}

def amortization_schedule(principal, annual_rate_percent, months, method="Frances"):
    principal = money(principal)
    months = int(months)
    if principal <= 0 or months <= 0:
        raise ValueError("El monto y el plazo deben ser mayores que cero.")
    rate = Decimal(str(annual_rate_percent)) / 100 / 12
    balance = principal
    if method == "Frances" and rate:
        payment = money(principal * rate / (1 - (1 + rate) ** (-months)))
    elif method == "Frances":
        payment = money(principal / months)
    else:
        constant_principal = money(principal / months)
        payment = None

    rows = []
    for number in range(1, months + 1):
        interest = money(balance * rate)
        if method == "Frances":
            capital = money(payment - interest)
        else:
            capital = constant_principal if number < months else balance
        if number == months or capital > balance:
            capital = balance
        installment = money(capital + interest)
        balance = money(balance - capital)
        rows.append({"number": number, "principal": capital, "interest": interest,
                     "payment": installment, "balance": balance})
    return rows

def add_months(start: date, months: int) -> date:
    month_index = start.month - 1 + months
    year = start.year + month_index // 12
    month = month_index % 12 + 1
    import calendar
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

def normalize_document(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())

def _valid_document_input(value: str, groups: tuple[int, ...]) -> bool:
    """Accept digits and the expected optional hyphens, but never ignore letters."""
    value = value.strip()
    if not value or any(not (ch.isdigit() or ch == "-") for ch in value):
        return False
    digits = normalize_document(value)
    if len(digits) != sum(groups):
        return False
    expected_parts = []
    offset = 0
    for size in groups:
        expected_parts.append(digits[offset:offset + size])
        offset += size
    expected = "-".join(expected_parts)
    # Permit either the plain digits or the canonical hyphenated form.
    return "-" not in value or value == expected

def valid_dui(value: str) -> bool:
    return _valid_document_input(value, (8, 1))

def valid_nit(value: str) -> bool:
    return _valid_document_input(value, (4, 6, 3, 1))

def normalize_phone(value: str) -> str:
    return normalize_document(value)

def valid_phone(value: str) -> bool:
    value = value.strip()
    return (all(ch.isdigit() or ch == "-" for ch in value)
            and len(normalize_phone(value)) == 8
            and ("-" not in value or (len(value) == 9 and value[4] == "-")))

def format_phone(value: str) -> str:
    digits = normalize_phone(value)
    return f"{digits[:4]}-{digits[4:]}" if len(digits) == 8 else value.strip()

def format_dui(value: str) -> str:
    digits = normalize_document(value)
    return f"{digits[:8]}-{digits[8:]}" if len(digits) == 9 else value.strip()

def format_nit(value: str) -> str:
    digits = normalize_document(value)
    return f"{digits[:4]}-{digits[4:10]}-{digits[10:13]}-{digits[13:]}" if len(digits) == 14 else value.strip()
