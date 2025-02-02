import os
import time
from celery import Celery
from pipeline import quality_check, dr_classification, dr_grading, generate_pdf_report

# Configure Celery with Redis as broker and backend.
app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task(bind=True)
def process_images(self, job_id, file_paths):
    results = []

    # STEP 1: Quality Check
    self.update_state(state="QUALITY_CHECK", meta={"message": "Evaluating image quality"})
    quality_results = []
    for path in file_paths:
        quality = quality_check(path)
        quality_results.append(quality)
        results.append({
            "filename": os.path.basename(path),
            "quality": quality
        })
        time.sleep(15)  # Simulate processing time

    if not any(quality_results):
        self.update_state(state="FAILED", meta={"message": "All images are of poor quality"})
        return {"message": "All images are of poor quality"}

    # STEP 2: DR Classification
    self.update_state(state="DR_CLASSIFICATION", meta={"message": "Classifying for DR"})
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

    if not dr_detected_any:
        self.update_state(state="FAILED", meta={"message": "No images with DR detected"})
        return {"message": "No images with DR detected"}

    # STEP 3: DR Grading
    self.update_state(state="DR_GRADING", meta={"message": "Grading DR severity"})
    for result, path in zip(results, file_paths):
        if result.get("dr_detected"):
            grade = dr_grading(path)
            result["dr_grade"] = grade
            time.sleep(13)
        else:
            result["dr_grade"] = None

    # STEP 4: Generate PDF Report
    self.update_state(state="GENERATING_PDF", meta={"message": "Generating PDF report"})
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    pdf_path = os.path.join(reports_dir, f"{job_id}.pdf")
    generate_pdf_report(results, pdf_path)
    self.update_state(state="COMPLETED", meta={
        "message": "Process completed",
        "pdf_path": pdf_path,
        "results": results
    })
    return {"message": "Process completed", "pdf_path": pdf_path, "results": results}
