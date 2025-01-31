from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def generate_pdf(results: list, task_id: str) -> str:
    """Generate PDF report from processing results"""
    filename = f"reports/{task_id}.pdf"
    os.makedirs("reports", exist_ok=True)
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title = Paragraph("Medical Imaging Report", styles['Title'])
    elements.append(title)
    
    # Report Date
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generated: {date_str}", styles['Normal']))
    elements.append(Spacer(1, 24))
    
    # Results Table
    data = [["Image #", "Quality", "Classification", "Grade", "Confidence"]]
    for i, result in enumerate(results):
        row = [
            str(i+1),
            f"{result.get('quality', 0)*100:.1f}%",
            "Positive" if result.get('classification', 0) >= 0.5 else "Negative",
            str(result.get('grade', 'N/A')),
            f"{result.get('confidence', 0)*100:.1f}%" if 'confidence' in result else 'N/A'
        ]
        data.append(row)
    
    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    elements.append(table)
    
    doc.build(elements)
    return filename