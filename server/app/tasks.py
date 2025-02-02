from celery import Celery
from .core.models import MockAIModels
from .core.report_generator import generate_pdf_report

celery = Celery(__name__, broker='redis://redis:6379/0')

@celery.task
def process_images_task(images):
    pipeline = MockAIModels()
    results = pipeline.run(images)
    pdf_path = generate_pdf_report(results)
    return {"status": "completed", "pdf_path": pdf_path}