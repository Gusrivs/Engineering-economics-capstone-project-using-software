from io import BytesIO
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def money_text(cents):
    return f"${Decimal(cents) / 100:,.2f}"


def make_receipt_pdf(row):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=0.65*inch, leftMargin=0.65*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SmallMuted", parent=styles["Normal"], textColor=colors.HexColor("#64748b")))
    story = [Paragraph("FINANCIERA · COMPROBANTE DE PAGO", styles["Title"]),
             Paragraph("Recibo de pago de crédito", styles["Heading2"]), Spacer(1, 10)]
    details = [
        ["N.º de recibo", row["receipt_number"], "Fecha", row["paid_at"]],
        ["Cliente", row["full_name"], "DUI", row["dui"]],
        ["Crédito", f"CR-{row['loan_id']:05d}", "Cuota", str(row["installment_number"])],
    ]
    table = Table(details, colWidths=[1.05*inch, 2.5*inch, 0.72*inch, 2.05*inch])
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#f1f5f9")),
        ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#475569")),("TEXTCOLOR",(2,0),(2,-1),colors.HexColor("#475569")),
        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
        ("GRID",(0,0),(-1,-1),0.5,colors.white),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
    story.extend([table, Spacer(1, 20)])
    amounts = [["Concepto", "Importe"], ["Abono a capital", money_text(row["principal_amount"])],
               ["Pago de interés", money_text(row["interest_amount"])],
               ["Mora / comisión", money_text(row["fee_amount"])],
               ["Total recibido", money_text(row["amount"])],
               ["Saldo insoluto restante", money_text(row["balance_after"])]]
    at = Table(amounts, colWidths=[4.7*inch, 1.6*inch])
    at.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#123b35")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ALIGN",(1,1),(1,-1),"RIGHT"),("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#dbe3e8")),
        ("BACKGROUND",(0,4),(-1,4),colors.HexColor("#ecfdf5")),
        ("FONTNAME",(0,4),(-1,4),"Helvetica-Bold"),("BACKGROUND",(0,5),(-1,5),colors.HexColor("#f1f5f9")),
        ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
    story.extend([at, Spacer(1, 28), Paragraph("Pago registrado en el sistema de gestión crediticia.", styles["SmallMuted"]),
                  Spacer(1, 28), Paragraph("______________________________<br/>Firma / sello", styles["Normal"])])
    doc.build(story)
    return output.getvalue()
