from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import sys

out = sys.argv[1] if len(sys.argv) > 1 else "reportlab-sample.pdf"
doc = SimpleDocTemplate(
    out,
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=20 * mm,
)
styles = getSampleStyleSheet()
story = [
    Paragraph("PDF Smoke Test — ReportLab", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Tertiary pipeline: Python ReportLab for tabular/data PDFs.", styles["Normal"]),
    Spacer(1, 12),
    Table(
        [["Pipeline", "Tier"], ["Playwright", "Primary"], ["Pandoc", "Secondary"], ["ReportLab", "Tertiary"]],
        colWidths=[80 * mm, 40 * mm],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        ),
    ),
    PageBreak(),
    Paragraph("Page Two", styles["Heading1"]),
    Paragraph("Multi-page A4 test.", styles["Normal"]),
]
doc.build(story)
print("Wrote", out)
