from .mock_models import quality_model, classification_model, grading_model
from typing import Dict, Any

def process_pipeline(image: bytes) -> Dict[str, Any]:
    """Full processing pipeline for a single image"""
    results = {}
    
    # Stage 1: Quality Check
    quality_score = quality_model(image)
    results['quality'] = round(quality_score, 2)
    if quality_score < 0.5:
        return {'status': 'rejected', **results}
    
    # Stage 2: Classification
    class_score = classification_model(image)
    results['classification'] = round(class_score, 2)
    if class_score < 0.5:
        return {'status': 'negative', **results}
    
    # Stage 3: Grading
    grade_results = grading_model(image)
    return {'status': 'positive', **results, **grade_results}