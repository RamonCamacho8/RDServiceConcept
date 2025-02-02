import os
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from tasks import process_images
from celery.result import AsyncResult
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # URL del cliente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para subir imágenes e iniciar el pipeline.
@app.post("/upload")
async def upload_images(files: List[UploadFile] = File(...)):
    job_id = str(uuid.uuid4())
    job_dir = os.path.join("uploads", job_id)
    os.makedirs(job_dir, exist_ok=True)
    file_paths = []
    for file in files:
        file_path = os.path.join(job_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        file_paths.append(file_path)
    # Establecer el job_id generado como el task_id de la tarea Celery
    task = process_images.apply_async(args=[job_id, file_paths], task_id=job_id)
    return {"job_id": job_id}


# Endpoint para consultar el estado del pipeline.
@app.get("/status/{job_id}")
def get_status(job_id: str):
    task = AsyncResult(job_id, app=process_images.app)
    # Por defecto, se toma el estado interno de Celery.
    result_status = task.state
    # Si la tarea finalizó exitosamente pero incluye un custom_status, se utiliza este.
    if task.state == "SUCCESS" and isinstance(task.info, dict) and task.info.get("custom_status"):
        result_status = task.info.get("custom_status")
    return {"status": result_status, "info": task.info}

# Endpoint para recuperar el PDF generado.
@app.get("/pdf/{job_id}")
def get_pdf(job_id: str):
    pdf_path = os.path.join("reports", f"{job_id}.pdf")
    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename={job_id}.pdf"}
        )
    return {"error": "PDF not found"}

