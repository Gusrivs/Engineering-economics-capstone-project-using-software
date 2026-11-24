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

def valid_dui(value: str) -> bool:
    return len(normalize_document(value)) == 9

def valid_nit(value: str) -> bool:
    return len(normalize_document(value)) == 14

def format_dui(value: str) -> str:
    digits = normalize_document(value)
    return f"{digits[:8]}-{digits[8:]}" if len(digits) == 9 else value.strip()

def format_nit(value: str) -> str:
    digits = normalize_document(value)
    return f"{digits[:4]}-{digits[4:10]}-{digits[10:13]}-{digits[13:]}" if len(digits) == 14 else value.strip()
