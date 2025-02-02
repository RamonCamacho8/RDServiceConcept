from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from celery.result import AsyncResult
from .schemas import JobStatus
from .tasks import process_images_task

app = FastAPI()

@app.post("/jobs/")
async def create_job(files: list[UploadFile] = File(...)):
    job = process_images_task.delay([file.file.read() for file in files])
    return {"job_id": job.id}

@app.get("/jobs/{job_id}/status")
async def get_status(job_id: str):
    task = AsyncResult(job_id)
    return {"status": task.status, "result": task.result}

@app.get("/jobs/{job_id}/report")
async def get_report(job_id: str):
    # Lógica para servir el PDF
    return FileResponse(f"reports/{job_id}.pdf")