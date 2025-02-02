from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from .schemas import JobStatus
from .tasks import process_images_task

app = FastAPI()

origins = [
    "http://localhost:4173",  # O puedes usar "*" para todos los orígenes (aunque no es recomendado en producción)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/jobs/")
async def create_job(images: list[UploadFile] = File(...)):
    file_contents = [await image.read() for image in images]
    job = process_images_task.delay(file_contents)
    return {"job_id": job.id}

@app.get("/jobs/{job_id}/status")
async def get_status(job_id: str):
    task = AsyncResult(job_id)
    return {"status": task.status, "result": task.result}

@app.get("/jobs/{job_id}/report")
async def get_report(job_id: str):
    from fastapi.responses import FileResponse
    return FileResponse(f"reports/{job_id}.pdf")
