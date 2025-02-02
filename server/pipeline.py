import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Mock quality check: randomly return True (good quality) or False.
def quality_check(image_path):
    return random.choice([True, True, False])  # More likely to be good quality

# Mock DR classification: randomly decide if DR is detected.
def dr_classification(image_path):
    return random.choice([True, False])

# Mock DR grading: randomly assign a grade between 1 and 4.
def dr_grading(image_path):
    return random.choice([1, 2, 3, 4])

# Generate a simple PDF report using ReportLab.
def generate_pdf_report(results, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)
    for result in results:
        line = (
            f"{result['filename']}: Quality: {result['quality']}, "
            f"DR Detected: {result.get('dr_detected', False)}, "
            f"DR Grade: {result.get('dr_grade', 'N/A')}"
        )
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
