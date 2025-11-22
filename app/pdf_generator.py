from pathlib import Path
from typing import Dict

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter

from .models import BudgetData


def create_overlay(budget_data: BudgetData, positions: Dict[str, Dict[str, int]], output_path: Path) -> None:
    c = canvas.Canvas(str(output_path), pagesize=letter)
    flat = budget_data.to_flat_dict()
    for field, value in flat.items():
        if field not in positions:
            continue
        coords = positions[field]
        x = coords.get("x", 0)
        y = coords.get("y", 0)
        font_size = coords.get("font_size", 12)
        c.setFont("Helvetica", font_size)
        c.drawString(x, y, value)
    c.showPage()
    c.save()


def merge_with_template(template_pdf: Path, overlay_pdf: Path, output_pdf: Path) -> None:
    template_reader = PdfReader(str(template_pdf))
    overlay_reader = PdfReader(str(overlay_pdf))
    writer = PdfWriter()

    template_page = template_reader.pages[0]
    overlay_page = overlay_reader.pages[0]
    template_page.merge_page(overlay_page)
    writer.add_page(template_page)

    with output_pdf.open("wb") as f:
        writer.write(f)


def generate_budget_pdf(
    budget_data: BudgetData,
    positions: Dict[str, Dict[str, int]],
    template_pdf: Path,
    output_pdf: Path,
) -> Path:
    overlay_pdf = output_pdf.with_name("_overlay_tmp.pdf")
    create_overlay(budget_data, positions, overlay_pdf)
    merge_with_template(template_pdf, overlay_pdf, output_pdf)
    overlay_pdf.unlink(missing_ok=True)
    return output_pdf
