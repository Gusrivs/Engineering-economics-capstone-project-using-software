from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "financiera.db"


def connect():
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dui TEXT NOT NULL UNIQUE,
            nit TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            monthly_income INTEGER NOT NULL CHECK(monthly_income >= 0),
            credit_profile TEXT NOT NULL DEFAULT 'En evaluación',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL REFERENCES clients(id),
            principal INTEGER NOT NULL CHECK(principal > 0),
            annual_rate REAL NOT NULL CHECK(annual_rate >= 0),
            months INTEGER NOT NULL CHECK(months > 0),
            method TEXT NOT NULL CHECK(method IN ('Frances', 'Aleman')),
            start_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Activo',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS installments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_id INTEGER NOT NULL REFERENCES loans(id) ON DELETE CASCADE,
            number INTEGER NOT NULL,
            due_date TEXT NOT NULL,
            principal_due INTEGER NOT NULL,
            interest_due INTEGER NOT NULL,
            principal_paid INTEGER NOT NULL DEFAULT 0,
            interest_paid INTEGER NOT NULL DEFAULT 0,
            fee_paid INTEGER NOT NULL DEFAULT 0,
            UNIQUE(loan_id, number)
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number TEXT NOT NULL UNIQUE,
            installment_id INTEGER NOT NULL REFERENCES installments(id),
            amount INTEGER NOT NULL,
            principal_amount INTEGER NOT NULL,
            interest_amount INTEGER NOT NULL,
            fee_amount INTEGER NOT NULL,
            paid_at TEXT NOT NULL,
            balance_after INTEGER NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_loans_client ON loans(client_id);
        CREATE INDEX IF NOT EXISTS idx_installments_loan ON installments(loan_id, number);
        CREATE INDEX IF NOT EXISTS idx_payments_date ON payments(paid_at);
        """)
        seed_demo_clients(conn)


def seed_demo_clients(conn):
    count = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    if count:
        return
    clients = [
        ("María Fernanda López", "12345678-9", "0614-230590-101-2", "7000-1001", "Santa Ana", 65000, "Bueno"),
        ("Carlos Eduardo Pérez", "23456789-0", "0614-140285-102-3", "7000-1002", "El Congo, Santa Ana", 52000, "En evaluación"),
        ("Ana Gabriela Martínez", "34567890-1", "0614-091192-103-4", "7000-1003", "Chalchuapa, Santa Ana", 78000, "Bueno"),
        ("José Alberto Hernández", "45678901-2", "0614-020778-104-5", "7000-1004", "Ahuachapán", 43000, "En evaluación"),
        ("Sofía Alejandra Rivera", "56789012-3", "0614-180699-105-6", "7000-1005", "Metapán, Santa Ana", 90000, "Bueno"),
    ]
    conn.executemany("""INSERT INTO clients(full_name,dui,nit,phone,address,monthly_income,credit_profile,created_at)
        VALUES(?,?,?,?,?,?,?,?)""", [(*c, date.today().isoformat()) for c in clients])


def create_client(data):
    with connect() as conn:
        conn.execute("""INSERT INTO clients(full_name,dui,nit,phone,address,monthly_income,credit_profile,created_at)
            VALUES(:full_name,:dui,:nit,:phone,:address,:monthly_income,:credit_profile,:created_at)""", data)


def list_clients(search=""):
    with connect() as conn:
        return conn.execute("""SELECT * FROM clients WHERE full_name LIKE ? OR dui LIKE ? ORDER BY full_name""",
                            (f"%{search}%", f"%{search}%")).fetchall()


def update_client(client_id, data):
    with connect() as conn:
        conn.execute("""UPDATE clients SET full_name=:full_name,dui=:dui,nit=:nit,phone=:phone,
            address=:address,monthly_income=:monthly_income,credit_profile=:credit_profile WHERE id=:id""",
            {**data, "id": client_id})


def create_loan(client_id, principal, annual_rate, months, method, start_date, schedule):
    with connect() as conn:
        cursor = conn.execute("""INSERT INTO loans(client_id,principal,annual_rate,months,method,start_date,created_at)
            VALUES(?,?,?,?,?,?,?)""", (client_id, principal, annual_rate, months, method, start_date,
                                         date.today().isoformat()))
        loan_id = cursor.lastrowid
        conn.executemany("""INSERT INTO installments(loan_id,number,due_date,principal_due,interest_due)
            VALUES(?,?,?,?,?)""", [(loan_id, r["number"], r["due_date"], r["principal"], r["interest"])
                                      for r in schedule])
        return loan_id


def list_loans(client_id=None):
    query = """SELECT l.*, c.full_name, c.dui,
      COALESCE((SELECT SUM(i.principal_due-i.principal_paid) FROM installments i WHERE i.loan_id=l.id), l.principal) AS balance
      FROM loans l JOIN clients c ON c.id=l.client_id"""
    params = ()
    if client_id:
        query += " WHERE l.client_id=?"
        params = (client_id,)
    query += " ORDER BY l.created_at DESC, l.id DESC"
    with connect() as conn:
        return conn.execute(query, params).fetchall()


def list_installments(loan_id):
    with connect() as conn:
        return conn.execute("""SELECT i.*, (i.principal_due-i.principal_paid) AS principal_remaining,
          (i.interest_due-i.interest_paid) AS interest_remaining,
          (i.principal_due-i.principal_paid+i.interest_due-i.interest_paid) AS due_remaining
          FROM installments i WHERE loan_id=? ORDER BY number""", (loan_id,)).fetchall()


def register_payment(installment_id, received, fee, paid_at):
    with connect() as conn:
        row = conn.execute("""SELECT i.*,l.id AS loan_id FROM installments i JOIN loans l ON l.id=i.loan_id
            WHERE i.id=?""", (installment_id,)).fetchone()
        if not row:
            raise ValueError("No se encontró la cuota seleccionada.")
        principal_left = row["principal_due"] - row["principal_paid"]
        interest_left = row["interest_due"] - row["interest_paid"]
        if received <= 0 or fee < 0 or fee > received:
            raise ValueError("El pago debe ser positivo y el cargo no puede superar el monto recibido.")
        if received > fee + interest_left + principal_left:
            raise ValueError("El monto supera el saldo de la cuota seleccionada. Registre el excedente en otra cuota.")
        # Orden de aplicación: cargo manual, interés pendiente y capital pendiente.
        fee_amount = min(fee, received)
        remaining = received - fee_amount
        interest_amount = min(interest_left, remaining)
        remaining -= interest_amount
        principal_amount = min(principal_left, remaining)
        applied = fee_amount + interest_amount + principal_amount
        if applied <= 0:
            raise ValueError("La cuota seleccionada ya está pagada o el importe no cubre ningún saldo pendiente.")
        conn.execute("""UPDATE installments SET principal_paid=principal_paid+?, interest_paid=interest_paid+?,
            fee_paid=fee_paid+? WHERE id=?""", (principal_amount, interest_amount, fee_amount, installment_id))
        balance = conn.execute("""SELECT COALESCE(SUM(principal_due-principal_paid),0) FROM installments WHERE loan_id=?""",
                               (row["loan_id"],)).fetchone()[0]
        receipt = f"REC-{date.today():%Y%m%d}-{conn.execute('SELECT COALESCE(MAX(id),0)+1 FROM payments').fetchone()[0]:05d}"
        cur = conn.execute("""INSERT INTO payments(receipt_number,installment_id,amount,principal_amount,
            interest_amount,fee_amount,paid_at,balance_after) VALUES(?,?,?,?,?,?,?,?)""",
            (receipt, installment_id, applied, principal_amount, interest_amount, fee_amount, paid_at, balance))
        outstanding = conn.execute("""SELECT COALESCE(SUM((principal_due-principal_paid)+(interest_due-interest_paid)),0)
            FROM installments WHERE loan_id=?""", (row["loan_id"],)).fetchone()[0]
        conn.execute("""UPDATE loans SET status=CASE WHEN ?=0 THEN 'Cancelado' ELSE 'Activo' END WHERE id=?""",
                     (outstanding, row["loan_id"]))
        return cur.lastrowid, receipt


def list_payments():
    with connect() as conn:
        return conn.execute("""SELECT p.*, c.full_name, c.dui, l.id AS loan_id, i.number AS installment_number
          FROM payments p JOIN installments i ON i.id=p.installment_id JOIN loans l ON l.id=i.loan_id
          JOIN clients c ON c.id=l.client_id ORDER BY p.id DESC""").fetchall()


def payment_detail(payment_id):
    with connect() as conn:
        return conn.execute("""SELECT p.*,c.full_name,c.dui,c.nit,c.address,l.id AS loan_id,
          i.number AS installment_number FROM payments p JOIN installments i ON i.id=p.installment_id
          JOIN loans l ON l.id=i.loan_id JOIN clients c ON c.id=l.client_id WHERE p.id=?""",
          (payment_id,)).fetchone()


def dashboard_metrics():
    with connect() as conn:
        return {
            "clients": conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0],
            "active_loans": conn.execute("SELECT COUNT(*) FROM loans WHERE status='Activo'").fetchone()[0],
            "portfolio": conn.execute("SELECT COALESCE(SUM(principal_due-principal_paid),0) FROM installments").fetchone()[0],
            "payments": conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0],
        }
