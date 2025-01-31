from celery import Celery
from .models.model_pipeline import process_pipeline
from .pdf_generator import generate_pdf

celery = Celery(__name__, broker="redis://redis:6379/0")

@celery.task(bind=True)
def process_image_task(self, images):
    total_steps = len(images) * 3 + 1  # 3 steps per image + PDF generation
    results = []
    
    for i, img in enumerate(images):
        self.update_state(
            task_id=self.request.id,
            state='PROGRESS',
            meta={
                'progress': (i * 3 / total_steps) * 100,
                'stage': f"Processing image {i+1}/ Quality Check"
            }
        )
        
        result = process_pipeline(img)
        results.append(result)
        
        self.update_state(
            task_id=self.request.id,
            state='PROGRESS',
            meta={
                'progress': ((i * 3 + 1) / total_steps) * 100,
                'stage': f"Processing image {i+1}/ Classification"
            }
        )
        
        # ... actual processing steps

    self.update_state(
        task_id=self.request.id,
        state='PROGRESS',
        meta={
            'progress': 95,
            'stage': "Generating PDF Report"
        }
    )
    
    generate_pdf(results, self.request.id)
    
    return {
        'progress': 100,
        'stage': "Complete",
        'result': 'success'
    }