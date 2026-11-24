from datetime import date
from decimal import Decimal
import sqlite3

import streamlit as st

import db
from finance import (add_months, amortization_schedule, compound_interest, format_dui,
                     format_nit, format_phone, money, simple_interest, valid_dui,
                     valid_nit, valid_phone)
from receipts import make_receipt_pdf, money_text

st.set_page_config(page_title="CrediGestión | Sistema financiero", page_icon="◈", layout="wide")
db.init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#152b2b; --muted:#6d7d7c; --green:#176b58; --pale:#eaf4ef; --line:#e5ece9; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
[data-testid="stAppViewContainer"] { background:#f7f9f8; }
[data-testid="stSidebar"] { background:#102e2a; }
[data-testid="stSidebar"] * { color:#edf7f2 !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:5px 0; }
h1,h2,h3 { font-family:'Manrope',sans-serif; letter-spacing:-.03em; }
h1 { font-size:2rem; }
.block-container { padding-top:5rem; max-width:1440px; }
[data-testid="stMetric"] { background:white; padding:18px 20px; border:1px solid var(--line); border-radius:14px; }
[data-testid="stMetricLabel"] { color:var(--muted); }
[data-testid="stMetricValue"] { color:var(--ink); }
.stButton button, .stDownloadButton button { border-radius:9px; font-weight:600; }
.stButton button[kind="primary"] { background:#176b58; border-color:#176b58; }
hr { border-color:var(--line); }
.eyebrow { color:#176b58; text-transform:uppercase; letter-spacing:.12em; font-weight:700; font-size:.75rem; }
.subtle { color:#6d7d7c; }
[data-testid="stSidebar"] code { color:#f4faf7 !important; background:#21443e !important; padding:3px 6px; border-radius:4px; }
[data-theme="dark"] [data-testid="stAppViewContainer"], [data-theme="dark"] .main,
[data-theme="dark"] .block-container, body[data-theme="dark"] .stApp,
html[data-theme="dark"] .stApp,
[data-theme="dark"] [data-testid="stMain"],
[data-theme="dark"] [data-testid="stMainBlockContainer"],
[data-theme="dark"] [data-testid="stAppViewBlockContainer"],
[data-theme="dark"] .stAppViewContainer,
body[data-theme="dark"] [data-testid="stAppViewContainer"] { background:#000 !important; }
[data-theme="dark"] [data-testid="stAppViewContainer"],
[data-theme="dark"] [data-testid="stMain"],
[data-theme="dark"] [data-testid="stMainBlockContainer"],
[data-theme="dark"] [data-testid="stAppViewContainer"] p,
[data-theme="dark"] [data-testid="stAppViewContainer"] li,
[data-theme="dark"] [data-testid="stAppViewContainer"] h1,
[data-theme="dark"] [data-testid="stAppViewContainer"] h2,
[data-theme="dark"] [data-testid="stAppViewContainer"] h3 { color:#f5f7f6 !important; }
[data-theme="dark"] [data-testid="stMarkdownContainer"] p,
[data-theme="dark"] [data-testid="stMarkdownContainer"] li,
[data-theme="dark"] [data-testid="stMarkdownContainer"] strong { color:#f1f3f2 !important; }
[data-theme="dark"] .subtle { color:#d5ddda !important; }
[data-theme="dark"] .eyebrow { color:#75d6b2 !important; }
[data-theme="dark"] [data-testid="stMetric"] { background:#151515 !important; border-color:#353535 !important; }
[data-theme="dark"] [data-testid="stAlert"],
[data-theme="dark"] [data-testid="stNotificationContent"] { background:#171717 !important; color:#f5f7f6 !important; }
[data-theme="dark"] [data-testid="stMarkdownContainer"] h1,
[data-theme="dark"] [data-testid="stMarkdownContainer"] h2,
[data-theme="dark"] [data-testid="stMarkdownContainer"] h3 { color:#fff !important; }
[data-theme="dark"] [data-testid="stMetricLabel"], [data-theme="dark"] [data-testid="stMetricValue"],
[data-theme="dark"] [data-testid="stMetricLabel"] *, [data-theme="dark"] [data-testid="stMetricValue"] * { color:#f5f7f6 !important; }
[data-theme="dark"] [data-testid="stSidebar"] code { color:#f4faf7 !important; background:#21443e !important; }
</style>
""", unsafe_allow_html=True)


def dollars(cents):
    return f"${Decimal(int(cents or 0)) / 100:,.2f}"


def cents(value):
    return int(money(value) * 100)


def format_digit_groups(digits, groups):
    parts = []
    offset = 0
    for size in groups:
        parts.append(digits[offset:offset + size])
        offset += size
    return "-".join(parts)


def sanitize_numeric_text(key, max_digits, groups):
    """Keep only the allowed digits, cap their count, and insert the standard hyphens."""
    raw = st.session_state.get(key, "")
    digits = "".join(ch for ch in str(raw) if ch.isdigit())[:max_digits]
    st.session_state[key] = format_digit_groups(digits, groups)


def page_header(eyebrow, title, subtitle):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p class="subtle">{subtitle}</p>', unsafe_allow_html=True)


def client_label(row):
    return f"{row['full_name']} · {row['dui']}"

with st.sidebar:
    st.markdown("## ◈ CrediGestión")
    st.caption("Sistema de gestión crediticia")
    st.divider()
    page = st.radio("NAVEGACIÓN", ["Inicio", "Clientes", "Calculadora", "Créditos", "Registrar pago", "Recibos"],
                    label_visibility="visible")
    st.divider()
    st.caption("Universidad de El Salvador · Proyecto integrador")
    st.caption("Almacenamiento local")
    st.markdown(f"<small style='color:#b8cac4'>Los datos se guardan en el archivo<br><code>{db.DB_PATH.name}</code></small>", unsafe_allow_html=True)

if page == "Inicio":
    page_header("Resumen operativo", "Panel financiero", "Vista rápida de clientes, cartera y actividad registrada.")
    m = db.dashboard_metrics()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clientes registrados", m["clients"])
    c2.metric("Créditos activos", m["active_loans"])
    c3.metric("Saldo de cartera", dollars(m["portfolio"]))
    c4.metric("Pagos registrados", m["payments"])
    st.markdown("### Flujo para la simulación en aula")
    st.markdown("1. Registre un cliente desde **Clientes** o use uno de los cinco registros ficticios precargados.\n"
                "2. Cree un crédito y revise su cronograma de cuotas en **Créditos**.\n"
                "3. Registre un pago parcial o completo; el saldo y las cuotas se actualizan en SQLite.\n"
                "4. Consulte el comprobante y descargue el recibo PDF en **Recibos**.")
    st.info("Los datos permanecen guardados en `financiera.db`, incluso después de cerrar la aplicación.")

elif page == "Clientes":
    page_header("Cartera de personas", "Clientes", "Alta, búsqueda y actualización de información del cliente.")
    tab_new, tab_list = st.tabs(["＋ Nuevo cliente", "Directorio"])
    with tab_new:
        with st.container(border=True):
            st.session_state.setdefault("new_dui", "")
            st.session_state.setdefault("new_nit", "")
            st.session_state.setdefault("new_phone", "")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nombre completo *", key="new_name")
                dui = st.text_input("DUI *", placeholder="12345678-9", max_chars=10,
                                    help="10 caracteres contando el guion: 9 dígitos. No se admiten letras.", key="new_dui",
                                    on_change=sanitize_numeric_text, args=("new_dui", 9, (8, 1)))
                phone = st.text_input("Teléfono *", placeholder="7000-0000", max_chars=9,
                                      help="9 caracteres contando el guion: 8 dígitos. No se admiten letras.", key="new_phone",
                                      on_change=sanitize_numeric_text, args=("new_phone", 8, (4, 4)))
                income = st.number_input("Ingresos mensuales (USD) *", min_value=0.0, step=1.0, key="new_income")
            with col2:
                nit = st.text_input("NIT *", placeholder="0614-000000-000-0", max_chars=17,
                                    help="17 caracteres contando los guiones: 14 dígitos. No se admiten letras.", key="new_nit",
                                    on_change=sanitize_numeric_text, args=("new_nit", 14, (4, 6, 3, 1)))
                address = st.text_input("Dirección *", key="new_address")
                profile = st.selectbox("Perfil crediticio", ["En evaluación", "Bueno", "Riesgo medio", "Riesgo alto"],
                                       key="new_profile")
            submitted = st.button("Guardar cliente", type="primary", key="submit_new_client")
        if submitted:
            if not all([name.strip(), dui.strip(), nit.strip(), phone.strip(), address.strip()]):
                st.error("Complete todos los campos obligatorios.")
            elif len(dui) != 10 or not valid_dui(dui):
                st.error("El DUI debe tener exactamente 10 caracteres, incluyendo el guion (9 dígitos).")
            elif len(nit) != 17 or not valid_nit(nit):
                st.error("El NIT debe tener exactamente 17 caracteres, incluyendo los guiones (14 dígitos).")
            elif len(phone) != 9 or not valid_phone(phone):
                st.error("El teléfono debe tener exactamente 9 caracteres, incluyendo el guion (8 dígitos).")
            else:
                try:
                    db.create_client({"full_name": name.strip(), "dui": format_dui(dui), "nit": format_nit(nit),
                        "phone": format_phone(phone), "address": address.strip(), "monthly_income": cents(income),
                        "credit_profile": profile, "created_at": date.today().isoformat()})
                    st.success("Cliente guardado correctamente.")
                except sqlite3.IntegrityError:
                    st.error("Ya existe un cliente con ese DUI o NIT.")
                except sqlite3.Error as exc:
                    st.error(f"No se pudo guardar el cliente: {exc}")
    with tab_list:
        search = st.text_input("Buscar por nombre o DUI", key="client_search")
        clients = db.list_clients(search)
        if clients:
            st.dataframe([{"Nombre": x["full_name"], "DUI": x["dui"], "NIT": x["nit"], "Teléfono": x["phone"],
                           "Dirección": x["address"], "Ingresos mensuales": dollars(x["monthly_income"]),
                           "Perfil": x["credit_profile"]} for x in clients], use_container_width=True, hide_index=True)
            client_by_id = {x["id"]: x for x in clients}
            chosen_id = st.selectbox("Editar registro", list(client_by_id),
                format_func=lambda key: client_label(client_by_id[key]), key="edit_client_select")
            chosen = client_by_id[chosen_id]
            with st.expander("Editar datos del cliente"):
                edit_dui_key = f"edit_dui_{chosen_id}"
                edit_nit_key = f"edit_nit_{chosen_id}"
                edit_phone_key = f"edit_phone_{chosen_id}"
                edit_dui_default = format_dui(chosen["dui"])
                edit_nit_default = format_nit(chosen["nit"])
                edit_phone_default = format_phone(chosen["phone"])
                st.session_state.setdefault(edit_dui_key, edit_dui_default)
                st.session_state.setdefault(edit_nit_key, edit_nit_default)
                st.session_state.setdefault(edit_phone_key, edit_phone_default)
                a,b = st.columns(2)
                with a:
                    edit_name = st.text_input("Nombre completo", value=chosen["full_name"], key=f"edit_name_{chosen_id}")
                    edit_dui = st.text_input("DUI", placeholder="12345678-9", max_chars=10,
                        help="10 caracteres contando el guion: 9 dígitos. No se admiten letras.", key=edit_dui_key,
                        on_change=sanitize_numeric_text, args=(edit_dui_key, 9, (8, 1)))
                    edit_phone = st.text_input("Teléfono", placeholder="7000-0000", max_chars=9,
                        help="9 caracteres contando el guion: 8 dígitos. No se admiten letras.", key=edit_phone_key,
                        on_change=sanitize_numeric_text, args=(edit_phone_key, 8, (4, 4)))
                    edit_income = st.number_input("Ingresos mensuales (USD)", min_value=0.0,
                        value=chosen["monthly_income"] / 100, step=1.0, key=f"edit_income_{chosen_id}")
                with b:
                    edit_nit = st.text_input("NIT", placeholder="0614-000000-000-0", max_chars=17,
                        help="17 caracteres contando los guiones: 14 dígitos. No se admiten letras.", key=edit_nit_key,
                        on_change=sanitize_numeric_text, args=(edit_nit_key, 14, (4, 6, 3, 1)))
                    edit_address = st.text_input("Dirección", value=chosen["address"], key=f"edit_address_{chosen_id}")
                    profiles = ["En evaluación", "Bueno", "Riesgo medio", "Riesgo alto"]
                    edit_profile = st.selectbox("Perfil crediticio", profiles,
                        index=profiles.index(chosen["credit_profile"]) if chosen["credit_profile"] in profiles else 0,
                        key=f"edit_profile_{chosen_id}")
                save_edit = st.button("Actualizar cliente", type="primary", key=f"save_edit_{chosen_id}")
                if save_edit:
                    if (not edit_name.strip() or not edit_address.strip()
                            or len(edit_dui) != 10 or not valid_dui(edit_dui)
                            or len(edit_nit) != 17 or not valid_nit(edit_nit)
                            or len(edit_phone) != 9 or not valid_phone(edit_phone)):
                        st.error("Revise los campos: DUI (10 caracteres con guion), NIT (17 con guiones) y teléfono (9 con guion).")
                    else:
                        try:
                            db.update_client(chosen["id"], {"full_name": edit_name.strip(), "dui": format_dui(edit_dui),
                                "nit": format_nit(edit_nit), "phone": format_phone(edit_phone), "address": edit_address.strip(),
                                "monthly_income": cents(edit_income), "credit_profile": edit_profile})
                            st.success("Datos actualizados.")
                        except sqlite3.IntegrityError:
                            st.error("El DUI o NIT ya pertenece a otro cliente.")
                        except sqlite3.Error as exc:
                            st.error(f"No se pudieron actualizar los datos: {exc}")
        else:
            st.info("No hay clientes que coincidan con la búsqueda.")

elif page == "Calculadora":
    page_header("Herramientas financieras", "Calculadora", "Interés simple, interés compuesto y amortización de créditos.")
    tab_interest, tab_amort = st.tabs(["Intereses", "Amortización"])
    with tab_interest:
        with st.form("interest_calc"):
            a,b,c,d = st.columns(4)
            principal = a.number_input("Capital (USD)", min_value=0.01, value=1000.0, step=100.0)
            annual = b.number_input("Tasa anual (%)", min_value=0.0, value=12.0, step=0.5)
            periods = c.number_input("Número de períodos", min_value=1, value=12, step=1)
            frequency = d.selectbox("Período", ["Mensual", "Anual"])
            run_calc = st.form_submit_button("Calcular", type="primary")
        if run_calc:
            periods_per_year = 12 if frequency == "Mensual" else 1
            simple = simple_interest(principal, annual, periods, periods_per_year)
            compound = compound_interest(principal, annual, periods, periods_per_year)
            a,b = st.columns(2)
            with a:
                st.markdown("#### Interés simple")
                st.metric("Interés generado", f"${simple['interest']:,.2f}")
                st.write(f"Capital: **${simple['principal']:,.2f}** · Monto final: **${simple['total']:,.2f}**")
            with b:
                st.markdown("#### Interés compuesto")
                st.metric("Interés generado", f"${compound['interest']:,.2f}")
                st.write(f"Capital: **${compound['principal']:,.2f}** · Monto final: **${compound['total']:,.2f}**")
    with tab_amort:
        a,b,c,d = st.columns(4)
        amount = a.number_input("Capital (USD)", min_value=1.0, value=5000.0, step=250.0, key="am_cap")
        rate = b.number_input("Tasa anual (%)", min_value=0.0, value=12.0, step=0.5, key="am_rate")
        months = c.number_input("Plazo en meses", min_value=1, max_value=360, value=12, key="am_months")
        method = d.selectbox("Sistema", ["Frances", "Aleman"], format_func=lambda x: "Francés · cuota fija" if x == "Frances" else "Alemán · capital constante", key="am_method")
        schedule = amortization_schedule(amount, rate, months, method)
        st.dataframe([{"Cuota": x["number"], "Capital": f"${x['principal']:,.2f}", "Interés": f"${x['interest']:,.2f}",
                       "Pago": f"${x['payment']:,.2f}", "Saldo": f"${x['balance']:,.2f}"} for x in schedule],
                     use_container_width=True, hide_index=True)
        st.caption(f"Total estimado de pagos: ${sum(x['payment'] for x in schedule):,.2f}")

elif page == "Créditos":
    page_header("Originación", "Créditos", "Cree créditos con cronograma de pagos y consulte los saldos registrados.")
    clients = db.list_clients()
    if not clients:
        st.warning("Registre un cliente antes de crear un crédito.")
    else:
        with st.form("new_loan"):
            a,b,c = st.columns(3)
            client_by_id = {x["id"]: x for x in clients}
            client_id = a.selectbox("Cliente", list(client_by_id),
                format_func=lambda key: client_label(client_by_id[key]))
            principal = b.number_input("Monto del crédito (USD)", min_value=1.0, value=1000.0, step=100.0)
            annual_rate = c.number_input("Tasa nominal anual (%)", min_value=0.0, value=12.0, step=0.5)
            d,e,f = st.columns(3)
            months = d.number_input("Plazo en meses", min_value=1, max_value=360, value=12)
            method = e.selectbox("Sistema de amortización", ["Frances", "Aleman"],
                                 format_func=lambda x: "Francés · cuota fija" if x == "Frances" else "Alemán · capital constante")
            start = f.date_input("Fecha de desembolso", value=date.today())
            submit_loan = st.form_submit_button("Crear crédito", type="primary")
        schedule = amortization_schedule(principal, annual_rate, months, method)
        st.markdown("#### Vista previa del cronograma")
        st.dataframe([{"Cuota": x["number"], "Vencimiento": add_months(start, x["number"]).isoformat(),
            "Capital": f"${x['principal']:,.2f}", "Interés": f"${x['interest']:,.2f}",
            "Cuota total": f"${x['payment']:,.2f}", "Saldo": f"${x['balance']:,.2f}"} for x in schedule],
            use_container_width=True, hide_index=True)
        if submit_loan:
            try:
                rows = [{**x, "due_date": add_months(start, x["number"]).isoformat()} for x in schedule]
                loan_id = db.create_loan(client_id, cents(principal), annual_rate, months, method, start.isoformat(), rows)
                st.success(f"Crédito CR-{loan_id:05d} creado y guardado con {months} cuotas.")
            except sqlite3.IntegrityError as exc:
                st.error(f"No se pudo guardar el crédito: {exc}")
    loans = db.list_loans()
    st.markdown("#### Cartera de créditos")
    if loans:
        st.dataframe([{"Crédito": f"CR-{x['id']:05d}", "Cliente": x["full_name"], "DUI": x["dui"],
            "Método": "Francés" if x["method"] == "Frances" else "Alemán", "Plazo": f"{x['months']} meses",
            "Saldo insoluto": dollars(x["balance"]), "Estado": x["status"]} for x in loans],
            use_container_width=True, hide_index=True)
    else:
        st.info("Aún no se han registrado créditos.")

elif page == "Registrar pago":
    page_header("Caja", "Registrar pago", "Aplique un pago a una cuota y actualice el saldo del crédito al instante.")
    loans = [x for x in db.list_loans() if x["status"] == "Activo"]
    if not loans:
        st.info("No hay créditos activos. Cree un crédito primero en la sección **Créditos**.")
    else:
        loan_by_id = {x["id"]: x for x in loans}
        loan_id = st.selectbox("Crédito", list(loan_by_id),
            format_func=lambda key: f"CR-{key:05d} · {loan_by_id[key]['full_name']} · saldo {dollars(loan_by_id[key]['balance'])}")
        loan = loan_by_id[loan_id]
        installments = [x for x in db.list_installments(loan["id"]) if x["due_remaining"] > 0]
        if installments:
            installment_by_id = {x["id"]: x for x in installments}
            installment_id = st.selectbox("Cuota a pagar", list(installment_by_id), format_func=lambda key:
                f"Cuota {installment_by_id[key]['number']} · vence {installment_by_id[key]['due_date']} · pendiente {dollars(installment_by_id[key]['due_remaining'])}")
            installment = installment_by_id[installment_id]
            st.caption(f"Capital pendiente: {dollars(installment['principal_remaining'])} · Interés pendiente: {dollars(installment['interest_remaining'])}")
            with st.form("payment_form"):
                a,b,c = st.columns(3)
                received = a.number_input("Monto recibido (USD)", min_value=0.01,
                    value=max(0.01, installment["due_remaining"] / 100), step=10.0)
                fee = b.number_input("Mora / comisión incluida (USD)", min_value=0.0, value=0.0, step=1.0)
                paid_at = c.date_input("Fecha de pago", value=date.today())
                submit_payment = st.form_submit_button("Registrar pago y emitir recibo", type="primary")
            if submit_payment:
                try:
                    if cents(fee) > cents(received):
                        st.error("La mora/comisión no puede superar el monto recibido.")
                    else:
                        payment_id, receipt = db.register_payment(installment["id"], cents(received), cents(fee), paid_at.isoformat())
                        st.session_state["last_payment_id"] = payment_id
                        st.success(f"Pago aplicado. Recibo {receipt} emitido.")
                        detail = db.payment_detail(payment_id)
                        st.download_button("Descargar recibo PDF", make_receipt_pdf(detail),
                            file_name=f"{receipt}.pdf", mime="application/pdf", key=f"pay_pdf_{payment_id}")
                except ValueError as exc:
                    st.error(str(exc))
        else:
            st.success("Todas las cuotas de este crédito están pagadas.")

elif page == "Recibos":
    page_header("Comprobantes", "Recibos de pago", "Consulte los pagos registrados y descargue su comprobante en PDF.")
    payments = db.list_payments()
    if not payments:
        st.info("Todavía no hay pagos. Registre uno en la sección **Registrar pago**.")
    else:
        st.dataframe([{"Recibo": x["receipt_number"], "Fecha": x["paid_at"], "Cliente": x["full_name"],
            "DUI": x["dui"], "Crédito": f"CR-{x['loan_id']:05d}", "Cuota": x["installment_number"],
            "Total": dollars(x["amount"]), "Saldo restante": dollars(x["balance_after"])} for x in payments],
            use_container_width=True, hide_index=True)
        payment_by_id = {x["id"]: x for x in payments}
        selected_payment_id = st.selectbox("Seleccionar recibo", list(payment_by_id),
            format_func=lambda key: f"{payment_by_id[key]['receipt_number']} · {payment_by_id[key]['full_name']} · {payment_by_id[key]['paid_at']}")
        detail = db.payment_detail(selected_payment_id)
        a,b,c = st.columns(3)
        a.metric("Capital", dollars(detail["principal_amount"]))
        b.metric("Interés", dollars(detail["interest_amount"]))
        c.metric("Mora / comisión", dollars(detail["fee_amount"]))
        st.markdown(f"**Total recibido:** {dollars(detail['amount'])}　 ·　 **Saldo insoluto:** {dollars(detail['balance_after'])}")
        st.download_button("Descargar recibo PDF", make_receipt_pdf(detail),
            file_name=f"{detail['receipt_number']}.pdf", mime="application/pdf")
