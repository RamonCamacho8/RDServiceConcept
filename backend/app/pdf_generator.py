from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(report_path: str, quality_results: dict, classification_results: dict, grading_results: dict):
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Reporte de Procesamiento de Imágenes")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Resultados de Calidad:")
    y -= 20
    for image, quality in quality_results.items():
        text = f"{image}: {'Buena' if quality else 'Mala'}"
        c.drawString(70, y, text)
        y -= 15

    y -= 10
    c.drawString(50, y, "Resultados de Clasificación (RD):")
    y -= 20
    for image, has_rd in classification_results.items():
        text = f"{image}: {'Con RD' if has_rd else 'Sin RD'}"
        c.drawString(70, y, text)
        y -= 15

    y -= 10
    c.drawString(50, y, "Resultados de Graduación (Grado RD):")
    y -= 20
    for image, grade in grading_results.items():
        text = f"{image}: Grado {grade}"
        c.drawString(70, y, text)
        y -= 15

    c.save()
