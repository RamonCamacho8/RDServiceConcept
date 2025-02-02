from celery import Celery
from .core.models import MockAIModels
from .core.report_generator import generate_pdf_report

celery = Celery(
    __name__,
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'  # Se configura el result backend
)

@celery.task
def process_images_task(images):
    pipeline = MockAIModels()
    results = pipeline.run(images)
    filename = f"/app/reports/{process_images_task.request.id}.pdf"
    pdf_path = generate_pdf_report(results, filename)
    return {"status": "completed", "pdf_path": pdf_path}
