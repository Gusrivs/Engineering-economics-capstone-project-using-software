from __future__ import annotations

import calendar
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")
METHODS = ("Frances", "Aleman")


# ---------------------------------------------------------------- utilidades
def _dec(value, name="valor") -> Decimal:
    """Convierte a Decimal rechazando texto, NaN e infinito con un error legible."""
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{name} no es un número válido.")
    if not d.is_finite():
        raise ValueError(f"{name} no es un número válido.")
    return d


def _int_periods(value, name="El número de períodos") -> int:
    d = _dec(value, name)
    if d != d.to_integral_value() or d <= 0:
        raise ValueError(f"{name} debe ser un entero mayor que cero.")
    return int(d)


def money(value) -> Decimal:
    return _dec(value, "El monto").quantize(CENT, rounding=ROUND_HALF_UP)


def _check_common(principal, annual_rate_percent, periods_per_year):
    p = money(principal)
    r = _dec(annual_rate_percent, "La tasa")
    ppy = _int_periods(periods_per_year, "Los períodos por año")
    if p <= 0:
        raise ValueError("El capital debe ser mayor que cero.")
    if r < 0:
        raise ValueError("La tasa no puede ser negativa.")
    return p, r / 100, ppy


# ------------------------------------------------------------ interés
def simple_interest(principal, annual_rate_percent, periods, periods_per_year=12):
    """I = P * i * n, con i = tasa anual / períodos por año."""
    p, r, ppy = _check_common(principal, annual_rate_percent, periods_per_year)
    n = _dec(periods, "El número de períodos")
    if n <= 0:
        raise ValueError("El número de períodos debe ser mayor que cero.")
    interest = money(p * r * n / Decimal(ppy))
    return {"principal": p, "interest": interest, "total": money(p + interest)}


def compound_interest(principal, annual_rate_percent, periods, periods_per_year=12):
    """F = P * (1 + i)^n, con i = tasa anual / períodos por año (capitalización por período)."""
    p, r, ppy = _check_common(principal, annual_rate_percent, periods_per_year)
    n = _int_periods(periods)
    rate = r / Decimal(ppy)
    total = money(p * ((Decimal("1") + rate) ** n))
    return {"principal": p, "interest": money(total - p), "total": total}


# ------------------------------------------------------------ amortización
def amortization_schedule(principal, annual_rate_percent, months, method="Frances"):
    if method not in METHODS:
        raise ValueError("Sistema de amortización no válido (use Frances o Aleman).")
    principal = money(principal)
    months = _int_periods(months, "El plazo")
    annual = _dec(annual_rate_percent, "La tasa")
    if principal <= 0:
        raise ValueError("El monto y el plazo deben ser mayores que cero.")
    if annual < 0:
        raise ValueError("La tasa no puede ser negativa.")

    rate = annual / 100 / 12
    balance = principal
    payment = constant_principal = None
    if method == "Frances":
        if rate:
            payment = money(principal * rate / (1 - (1 + rate) ** (-months)))
        else:
            payment = money(principal / months)
    else:
        constant_principal = money(principal / months)

    rows = []
    for number in range(1, months + 1):
        interest = money(balance * rate)
        if method == "Frances":
            capital = money(payment - interest)
        else:
            capital = constant_principal
        # La última cuota cancela el saldo exacto (absorbe el residuo de redondeo).
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
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


# ------------------------------------------------------------ documentos
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


def dui_check_digit(first8: str) -> int:
    """Dígito verificador del DUI: módulo 10 con pesos 9..2 sobre los 8 primeros dígitos."""
    total = sum(int(d) * w for d, w in zip(first8, range(9, 1, -1)))
    return (10 - total % 10) % 10


def valid_dui(value: str) -> bool:
    if not _valid_document_input(value, (8, 1)):
        return False
    digits = normalize_document(value)
    if digits[:8] == "0" * 8:
        return False
    return int(digits[8]) == dui_check_digit(digits[:8])


def valid_nit(value: str) -> bool:
    """14 dígitos (municipio 4 + fecha DDMMAA 6 + correlativo 3 + verificador 1); la fecha debe existir."""
    if not _valid_document_input(value, (4, 6, 3, 1)):
        return False
    digits = normalize_document(value)
    try:
        datetime.strptime(digits[4:10], "%d%m%y")
    except ValueError:
        return False
    return True


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