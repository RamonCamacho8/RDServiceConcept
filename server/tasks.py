import os
import time
from celery import Celery
from pipeline import quality_check, dr_classification, dr_grading, generate_pdf_report

# Configuración de Celery con Redis como broker y backend.
app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task(bind=True)
def process_images(self, job_id, file_paths):
    results = []
    
    # STEP 1: Quality Check
    self.update_state(state="QUALITY_CHECK", meta={"message": "Evaluando la calidad de las imágenes"})
    quality_results = []
    for path in file_paths:
        quality = quality_check(path)
        quality_results.append(quality)
        results.append({
            "filename": os.path.basename(path),
            "quality": quality
        })
        time.sleep(15)  # Simulación del tiempo de procesamiento

    # Si ninguna imagen tiene buena calidad, se genera el PDF y se marca como COMPLETED.
    if not any(quality_results):
        self.update_state(state="COMPLETED", meta={"message": "Todas las imágenes tienen baja calidad. Proceso completado.", "custom_status": "COMPLETED"})
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        pdf_path = os.path.join(reports_dir, f"{job_id}.pdf")
        generate_pdf_report(results, pdf_path)
        return {
            "message": "Todas las imágenes tienen baja calidad. Proceso completado.",
            "pdf_path": pdf_path,
            "results": results,
            "custom_status": "COMPLETED"
        }

    # STEP 2: DR Classification
    self.update_state(state="DR_CLASSIFICATION", meta={"message": "Clasificando para DR"})
    dr_detected_any = False
    for result, path in zip(results, file_paths):
        if result["quality"]:
            dr_detected = dr_classification(path)
            result["dr_detected"] = dr_detected
            if dr_detected:
                dr_detected_any = True
            time.sleep(10)
        else:
            result["dr_detected"] = False

    # Si no se detecta DR en ninguna imagen, se genera el PDF y se marca como COMPLETED.
    if not dr_detected_any:
        self.update_state(state="COMPLETED", meta={"message": "No se detectó DR en ninguna imagen. Proceso completado.", "custom_status": "COMPLETED"})
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        pdf_path = os.path.join(reports_dir, f"{job_id}.pdf")
        generate_pdf_report(results, pdf_path)
        return {
            "message": "No se detectó DR en ninguna imagen. Proceso completado.",
            "pdf_path": pdf_path,
            "results": results,
            "custom_status": "COMPLETED"
        }

    # STEP 3: DR Grading
    self.update_state(state="DR_GRADING", meta={"message": "Calificando la severidad de DR"})
    for result, path in zip(results, file_paths):
        if result.get("dr_detected"):
            grade = dr_grading(path)
            result["dr_grade"] = grade
            time.sleep(13)
        else:
            result["dr_grade"] = None

    # STEP 4: Generación del Reporte PDF
    self.update_state(state="GENERATING_PDF", meta={"message": "Generando reporte PDF"})
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    pdf_path = os.path.join(reports_dir, f"{job_id}.pdf")
    generate_pdf_report(results, pdf_path)
    
    self.update_state(state="COMPLETED", meta={
        "message": "Proceso completado",
        "pdf_path": pdf_path,
        "results": results,
        "custom_status": "COMPLETED"
    })
    return {
        "message": "Proceso completado",
        "pdf_path": pdf_path,
        "results": results,
        "custom_status": "COMPLETED"
    }