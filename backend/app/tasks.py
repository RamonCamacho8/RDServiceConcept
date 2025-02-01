import time
import random
import os
from celery import current_task
from app.celery_worker import celery_app
from app.pdf_generator import generate_pdf_report

# Funciones mock para simular los modelos de IA

def mock_quality_check(image_path: str) -> bool:
    time.sleep(0.5)  # Simula tiempo de procesamiento
    # Se asume que la imagen es de buena calidad el 80% de las veces
    return random.random() < 0.8

def mock_classification(image_path: str) -> bool:
    time.sleep(0.5)
    # Se simula la detección de RD con 30% de probabilidad
    return random.random() < 0.3

def mock_grading(image_path: str) -> int:
    time.sleep(0.5)
    # Se asigna un grado entre 1 y 4
    return random.randint(1, 4)

@celery_app.task(bind=True)
def process_images_task(self, task_id: str, image_paths: list):
    results = {}
    self.update_state(state="PROCESSING", meta={"step": "Calidad", "detail": "Evaluando calidad de imágenes"})
    
    quality_results = {}
    for image in image_paths:
        quality = mock_quality_check(image)
        quality_results[image] = quality

    # Si todas las imágenes son de mala calidad, finaliza el proceso
    if not any(quality_results.values()):
        results['error'] = "Todas las imágenes tienen mala calidad."
        self.update_state(state="FAILED", meta={"results": results})
        return results

    self.update_state(state="PROCESSING", meta={"step": "Clasificación", "detail": "Clasificando imágenes"})
    classification_results = {}
    for image, quality in quality_results.items():
        if quality:
            has_rd = mock_classification(image)
            classification_results[image] = has_rd

    # Si ninguna imagen presenta RD, finaliza el proceso
    if not any(classification_results.values()):
        results['error'] = "Ninguna imagen presenta signos de Retinopatía Diabética."
        self.update_state(state="FAILED", meta={"results": results})
        return results

    self.update_state(state="PROCESSING", meta={"step": "Graduación", "detail": "Graduando imágenes con RD"})
    grading_results = {}
    for image, has_rd in classification_results.items():
        if has_rd:
            grade = mock_grading(image)
            grading_results[image] = grade

    # Generar el reporte PDF
    self.update_state(state="PROCESSING", meta={"step": "Generando PDF", "detail": "Creando reporte PDF"})
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{task_id}.pdf")
    generate_pdf_report(report_path, quality_results, classification_results, grading_results)

    results['report'] = report_path
    self.update_state(state="SUCCESS", meta={"results": results})
    return results
