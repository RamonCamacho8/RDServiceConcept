from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def generate_pdf_report(results, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Reporte de Análisis de Retinopatía Diabética")
    
    # Tabla de resultados
    data = [["Imagen", "Calidad", "RD Detectado", "Grado"]]
    for idx, result in enumerate(results['final_results']):
        data.append([
            f"Imagen {idx + 1}",
            result.get('quality', 'N/A'),
            result.get('rd_present', 'N/A'),
            result.get('grade', 'N/A')
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    table.wrapOn(c, width - 100, height)
    table.drawOn(c, 50, height - 200)
    
    c.save()
    return filename